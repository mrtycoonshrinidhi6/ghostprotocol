"""
Ghost Protocol - Retry Handler
Exponential backoff, rate limiting, and error classification for API calls

Features:
- Exponential backoff with jitter
- Configurable max retries
- Rate limiting per tool
- Error classification
- Timeout protection
- Observability integration (logging, metrics, tracing)
"""

import asyncio
import time
import random
from typing import Callable, Any, Optional, Dict, Type
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict

from config import (
    MAX_RETRIES,
    RETRY_BASE_DELAY,
    RETRY_JITTER,
    API_TIMEOUT,
    RATE_LIMIT_PER_MINUTE,
    LOG_REALTIME_ERRORS,
    EMIT_TOOL_METRICS
)

# Optional observability integration
try:
    from observability import StructuredLogger, MetricsCollector
    _logger = StructuredLogger(service_name="retry-handler")
    _metrics = MetricsCollector()
    OBSERVABILITY_AVAILABLE = True
except ImportError:
    _logger = None
    _metrics = None
    OBSERVABILITY_AVAILABLE = False


# ============================================================================
# ERROR CLASSIFICATION
# ============================================================================

class APIError(Exception):
    """Base class for API errors"""
    pass


class NetworkError(APIError):
    """Network connectivity issues"""
    pass


class HTTPError(APIError):
    """HTTP status code errors"""
    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


class RateLimitError(APIError):
    """API rate limit exceeded"""
    pass


class InvalidKeyError(APIError):
    """Invalid or missing API key"""
    pass


class TimeoutError(APIError):
    """Request timeout"""
    pass


# ============================================================================
# RATE LIMITER
# ============================================================================

class RateLimiter:
    """Simple rate limiter using sliding window"""
    
    def __init__(self, max_requests: int = RATE_LIMIT_PER_MINUTE, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, tool_name: str) -> bool:
        """Check if request is allowed under rate limit"""
        now = time.time()
        
        # Clean old requests outside the window
        self.requests[tool_name] = [
            req_time for req_time in self.requests[tool_name]
            if now - req_time < self.window_seconds
        ]
        
        # Check if under limit
        if len(self.requests[tool_name]) < self.max_requests:
            self.requests[tool_name].append(now)
            return True
        
        return False
    
    def wait_time(self, tool_name: str) -> float:
        """Get wait time until next request is allowed"""
        if not self.requests[tool_name]:
            return 0.0
        
        oldest_request = min(self.requests[tool_name])
        wait_until = oldest_request + self.window_seconds
        return max(0.0, wait_until - time.time())


# Global rate limiter instance
_rate_limiter = RateLimiter()


# ============================================================================
# RETRY DECORATOR
# ============================================================================

def with_retry(
    max_retries: int = MAX_RETRIES,
    base_delay: float = RETRY_BASE_DELAY,
    use_jitter: bool = RETRY_JITTER,
    timeout: float = API_TIMEOUT,
    tool_name: str = "unknown",
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None
):
    """
    Decorator for API calls with exponential backoff, retry logic, and observability
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (doubles each retry)
        use_jitter: Add random jitter to delays
        timeout: Overall timeout for the operation
        tool_name: Name of the tool (for rate limiting and metrics)
        trace_id: Optional trace ID for distributed tracing
        span_id: Optional span ID for tracing
    
    Usage:
        @with_retry(max_retries=3, tool_name="etherscan")
        async def fetch_balance(address):
            # API call here
            pass
    """
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            last_exception = None
            total_retries = 0
            
            # Extract trace context from kwargs if available
            call_trace_id = kwargs.get("trace_id", trace_id)
            call_span_id = kwargs.get("span_id", span_id)
            
            for attempt in range(max_retries + 1):
                # Check timeout
                if time.time() - start_time > timeout:
                    error = TimeoutError(f"Operation timed out after {timeout}s")
                    
                    # Log timeout
                    if OBSERVABILITY_AVAILABLE and _logger:
                        _logger.error(
                            f"Retry timeout: {tool_name}",
                            error=error,
                            trace_id=call_trace_id,
                            span_id=call_span_id,
                            metadata={
                                "tool": tool_name,
                                "timeout_seconds": timeout,
                                "attempts": attempt + 1
                            }
                        )
                    
                    raise error
                
                # Check rate limit
                if not _rate_limiter.is_allowed(tool_name):
                    wait = _rate_limiter.wait_time(tool_name)
                    
                    # Log rate limit
                    if OBSERVABILITY_AVAILABLE and _logger:
                        _logger.warning(
                            f"Rate limit reached: {tool_name}",
                            trace_id=call_trace_id,
                            span_id=call_span_id,
                            metadata={
                                "tool": tool_name,
                                "wait_seconds": wait
                            }
                        )
                    
                    if LOG_REALTIME_ERRORS:
                        print(f"  [RATE LIMIT] {tool_name}: waiting {wait:.1f}s")
                    
                    await asyncio.sleep(wait)
                
                try:
                    # Execute the function
                    result = await func(*args, **kwargs)
                    
                    # Success - record metrics
                    elapsed_ms = (time.time() - start_time) * 1000
                    
                    if OBSERVABILITY_AVAILABLE and _metrics and EMIT_TOOL_METRICS:
                        # Record success
                        _metrics._record_metric(
                            f"tool.{tool_name}.success",
                            1.0,
                            tags={"attempts": str(attempt + 1)}
                        )
                        
                        # Record latency
                        _metrics._record_metric(
                            f"tool.{tool_name}.latency_ms",
                            elapsed_ms,
                            tags={"status": "success"}
                        )
                        
                        # Record retry count
                        if attempt > 0:
                            _metrics._record_metric(
                                f"tool.{tool_name}.retry_count",
                                attempt,
                                tags={"final_status": "success"}
                            )
                    
                    # Log success if retried
                    if attempt > 0:
                        if OBSERVABILITY_AVAILABLE and _logger:
                            _logger.info(
                                f"Retry succeeded: {tool_name}",
                                trace_id=call_trace_id,
                                span_id=call_span_id,
                                metadata={
                                    "tool": tool_name,
                                    "attempt": attempt + 1,
                                    "total_attempts": max_retries + 1,
                                    "latency_ms": elapsed_ms
                                }
                            )
                        
                        if LOG_REALTIME_ERRORS:
                            print(f"  [RETRY SUCCESS] {tool_name}: succeeded on attempt {attempt + 1}/{max_retries + 1}")
                    
                    return result
                
                except Exception as e:
                    last_exception = e
                    total_retries = attempt
                    
                    # Classify error
                    error_type = classify_error(e)
                    
                    # Don't retry certain errors
                    if isinstance(e, (InvalidKeyError,)):
                        # Log non-retryable error
                        if OBSERVABILITY_AVAILABLE and _logger:
                            _logger.error(
                                f"Non-retryable error: {tool_name}",
                                error=e,
                                trace_id=call_trace_id,
                                span_id=call_span_id,
                                metadata={
                                    "tool": tool_name,
                                    "error_type": error_type,
                                    "attempt": attempt + 1
                                }
                            )
                        
                        if LOG_REALTIME_ERRORS:
                            print(f"  [NO RETRY] {tool_name}: {error_type} - {e}")
                        
                        # Record failure metric
                        if OBSERVABILITY_AVAILABLE and _metrics and EMIT_TOOL_METRICS:
                            _metrics._record_metric(
                                f"tool.{tool_name}.error",
                                1.0,
                                tags={"error_type": error_type, "retryable": "false"}
                            )
                        
                        raise
                    
                    # Last attempt - raise
                    if attempt == max_retries:
                        elapsed_ms = (time.time() - start_time) * 1000
                        
                        # Log final failure
                        if OBSERVABILITY_AVAILABLE and _logger:
                            _logger.error(
                                f"Retry exhausted: {tool_name}",
                                error=e,
                                trace_id=call_trace_id,
                                span_id=call_span_id,
                                metadata={
                                    "tool": tool_name,
                                    "error_type": error_type,
                                    "total_attempts": max_retries + 1,
                                    "total_latency_ms": elapsed_ms
                                }
                            )
                        
                        # Record failure metrics
                        if OBSERVABILITY_AVAILABLE and _metrics and EMIT_TOOL_METRICS:
                            _metrics._record_metric(
                                f"tool.{tool_name}.failure",
                                1.0,
                                tags={"error_type": error_type, "attempts": str(max_retries + 1)}
                            )
                            
                            _metrics._record_metric(
                                f"tool.{tool_name}.retry_count",
                                max_retries,
                                tags={"final_status": "failure"}
                            )
                        
                        if LOG_REALTIME_ERRORS:
                            print(f"  [RETRY FAILED] {tool_name}: all {max_retries + 1} attempts failed")
                        
                        raise
                    
                    # Calculate delay for next retry
                    delay = calculate_backoff_delay(
                        attempt=attempt,
                        base_delay=base_delay,
                        use_jitter=use_jitter
                    )
                    
                    # Log retry attempt
                    if OBSERVABILITY_AVAILABLE and _logger:
                        _logger.warning(
                            f"Retrying: {tool_name}",
                            trace_id=call_trace_id,
                            span_id=call_span_id,
                            metadata={
                                "tool": tool_name,
                                "error_type": error_type,
                                "attempt": attempt + 1,
                                "max_attempts": max_retries + 1,
                                "retry_delay_seconds": delay
                            }
                        )
                    
                    if LOG_REALTIME_ERRORS:
                        print(f"  [RETRY] {tool_name}: attempt {attempt + 1}/{max_retries + 1} failed ({error_type}), retrying in {delay:.2f}s")
                    
                    # Wait before retry
                    await asyncio.sleep(delay)
            
            # Should never reach here, but just in case
            raise last_exception
        
        return wrapper
    return decorator


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_backoff_delay(attempt: int, base_delay: float, use_jitter: bool = True) -> float:
    """
    Calculate exponential backoff delay with optional jitter
    
    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay in seconds
        use_jitter: Whether to add random jitter
    
    Returns:
        Delay in seconds
    
    Examples:
        attempt=0: 0.5s (base)
        attempt=1: 1.0s (2x)
        attempt=2: 2.0s (4x)
        With jitter: ±25% random variation
    """
    
    # Exponential backoff: delay = base * (2 ^ attempt)
    delay = base_delay * (2 ** attempt)
    
    # Add jitter (±25%)
    if use_jitter:
        jitter_factor = random.uniform(0.75, 1.25)
        delay *= jitter_factor
    
    return delay


def classify_error(error: Exception) -> str:
    """
    Classify error into categories for better handling
    
    Args:
        error: Exception to classify
    
    Returns:
        Error category string
    """
    
    # Custom error classes
    if isinstance(error, NetworkError):
        return "NetworkError"
    elif isinstance(error, HTTPError):
        return f"HTTPError({error.status_code})"
    elif isinstance(error, RateLimitError):
        return "RateLimitError"
    elif isinstance(error, InvalidKeyError):
        return "InvalidKeyError"
    elif isinstance(error, TimeoutError):
        return "TimeoutError"
    
    # httpx errors
    error_name = type(error).__name__
    if "Timeout" in error_name or "timeout" in str(error).lower():
        return "TimeoutError"
    elif "Connection" in error_name or "connection" in str(error).lower():
        return "NetworkError"
    elif "429" in str(error):
        return "RateLimitError"
    elif "401" in str(error) or "403" in str(error):
        return "InvalidKeyError"
    elif "4" in str(error)[:3]:  # 4xx errors
        return "ClientError"
    elif "5" in str(error)[:3]:  # 5xx errors
        return "ServerError"
    
    # Generic
    return error_name


def check_http_status(status_code: int, response_text: str = "") -> None:
    """
    Check HTTP status code and raise appropriate error
    
    Args:
        status_code: HTTP status code
        response_text: Response text for error message
    
    Raises:
        HTTPError: For error status codes
        RateLimitError: For 429 status
        InvalidKeyError: For 401/403 status
    """
    
    if status_code == 429:
        raise RateLimitError("API rate limit exceeded")
    elif status_code in (401, 403):
        raise InvalidKeyError(f"Invalid or unauthorized API key")
    elif status_code >= 500:
        raise HTTPError(status_code, f"Server error: {response_text[:100]}")
    elif status_code >= 400:
        raise HTTPError(status_code, f"Client error: {response_text[:100]}")
    elif status_code >= 300:
        raise HTTPError(status_code, f"Redirect: {response_text[:100]}")


# ============================================================================
# RATE LIMIT CONTEXT MANAGER
# ============================================================================

class RateLimitContext:
    """Context manager for rate-limited operations"""
    
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
    
    async def __aenter__(self):
        """Wait if rate limited"""
        while not _rate_limiter.is_allowed(self.tool_name):
            wait = _rate_limiter.wait_time(self.tool_name)
            if LOG_REALTIME_ERRORS:
                print(f"  [RATE LIMIT] {self.tool_name}: waiting {wait:.1f}s")
            await asyncio.sleep(wait)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Nothing to cleanup"""
        pass


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance"""
    return _rate_limiter


def reset_rate_limiter():
    """Reset the global rate limiter (useful for testing)"""
    global _rate_limiter
    _rate_limiter = RateLimiter()


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    # Error classes
    "APIError",
    "NetworkError",
    "HTTPError",
    "RateLimitError",
    "InvalidKeyError",
    "TimeoutError",
    
    # Retry decorator
    "with_retry",
    
    # Rate limiting
    "RateLimiter",
    "RateLimitContext",
    "get_rate_limiter",
    "reset_rate_limiter",
    
    # Utilities
    "calculate_backoff_delay",
    "classify_error",
    "check_http_status",
]
