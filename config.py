"""
Ghost Protocol - Global Configuration
Advanced Integration Mode Controller

This module controls the runtime behavior of the entire system:
- REALTIME_MODE: Use real APIs vs mock data
- Latency simulation for mock responses
- Error logging and debugging toggles
"""

import os
from typing import Tuple
from pathlib import Path
from dotenv import load_dotenv

# Load backend/.env before reading any environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "backend" / ".env")


# ============================================================================
# RUNTIME MODE CONFIGURATION
# ============================================================================

# Master switch: Controls entire system behavior
# True  = Use real APIs (Google, Etherscan, Gmail, etc.)
# False = Use enhanced mock generators with artificial latency
REALTIME_MODE: bool = os.getenv("REALTIME_MODE", "False").lower() == "true"

# Mock mode flag from environment (legacy-style switch)
USE_MOCK_DATA_FLAG: bool = os.getenv("USE_MOCK_DATA", "False").lower() == "true"

# Force realtime override: when true, runtime must use REALTIME regardless of other flags
FORCE_REALTIME_OVERRIDE: bool = os.getenv("FORCE_REALTIME_OVERRIDE", "False").lower() == "true"

# --- REALTIME MODE OVERRIDE LOGIC --------------------------------------------
if FORCE_REALTIME_OVERRIDE:
    FINAL_MOCK_MODE: bool = False
elif REALTIME_MODE and not USE_MOCK_DATA_FLAG:
    FINAL_MOCK_MODE = False
else:
    FINAL_MOCK_MODE = True

# Public flag used throughout the codebase
USE_REALTIME: bool = (FINAL_MOCK_MODE is False)


# ============================================================================
# MOCK MODE CONFIGURATION
# ============================================================================

# Artificial latency range for mock API responses (seconds)
# Simulates realistic network delays when REALTIME_MODE = False
# Format: (min_latency, max_latency)
MOCK_LATENCY_RANGE: Tuple[float, float] = (0.3, 1.2)

# Enable detailed mock data generation logs
# Useful for debugging mock response structure
LOG_MOCK_GENERATION: bool = os.getenv("LOG_MOCK_GENERATION", "False").lower() == "true"


# ============================================================================
# ERROR HANDLING CONFIGURATION
# ============================================================================

# Log real-time API errors to console/files
# When True, detailed error messages are emitted
# When False, errors are silent (fallback to mock)
LOG_REALTIME_ERRORS: bool = os.getenv("LOG_REALTIME_ERRORS", "True").lower() == "true"

# Log mode switches (REALTIME → MOCK fallback)
# Helps track when API failures trigger fallback
LOG_MODE_SWITCHES: bool = True

# Log API key validation results
# Shows which keys are present/missing on startup
LOG_KEY_VALIDATION: bool = True


# ============================================================================
# RETRY & RATE LIMITING CONFIGURATION
# ============================================================================

# Maximum retry attempts for failed API calls
MAX_RETRIES: int = 3

# Exponential backoff base delay (seconds)
# Actual delays: 0.5s, 1s, 2s, 4s...
RETRY_BASE_DELAY: float = 0.5

# Add random jitter to retry delays (prevents thundering herd)
RETRY_JITTER: bool = True

# Global timeout for all API requests (seconds)
API_TIMEOUT: float = 30.0

# Rate limit: Max requests per minute (per tool)
RATE_LIMIT_PER_MINUTE: int = 60


# ============================================================================
# OBSERVABILITY CONFIGURATION
# ============================================================================

# Enable detailed observability for tool calls
# Emits logs, traces, and metrics for every tool execution
ENABLE_TOOL_OBSERVABILITY: bool = True

# Log level for tool operations
# Options: "DEBUG", "INFO", "WARNING", "ERROR"
TOOL_LOG_LEVEL: str = os.getenv("TOOL_LOG_LEVEL", "INFO")

# Emit metrics for tool performance
EMIT_TOOL_METRICS: bool = True

# Emit distributed traces for tool calls
EMIT_TOOL_TRACES: bool = True


# ============================================================================
# AGENT-LEVEL CONFIGURATION
# ============================================================================

# Confidence thresholds based on runtime mode
# REALTIME mode requires higher confidence (real data)
# MOCK mode uses lower threshold (artificial data)
REALTIME_CONFIDENCE_THRESHOLD: float = 0.85
MOCK_CONFIDENCE_THRESHOLD: float = 0.60

# Asset count boost for mock mode
# When using mock data, artificially increase discovered assets
# to make demos more impressive (additive, not multiplicative)
MOCK_ASSET_COUNT_BOOST: int = 5


# ============================================================================
# API KEY REQUIREMENTS
# ============================================================================

# List of critical API keys (system fails to REALTIME without these)
CRITICAL_API_KEYS = [
    "GEMINI_API_KEY",  # Required for Memorial Chat
]

# List of optional API keys (system works with fallback if missing)
OPTIONAL_API_KEYS = [
    "GOOGLE_SEARCH_API_KEY",
    "GOOGLE_SEARCH_ENGINE_ID",
    "ETHERSCAN_API_KEY",
    "POLYGONSCAN_API_KEY",
    "COINMARKETCAP_API_KEY",
    "GMAIL_CREDENTIALS_JSON",
    "GDRIVE_CREDENTIALS_JSON",
    "DROPBOX_ACCESS_TOKEN",
    "NEWS_API_KEY",
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_current_mode() -> str:
    """Get human-readable current runtime mode"""
    return "REALTIME" if USE_REALTIME else "MOCK"


def should_use_realtime() -> bool:
    """Check if system should attempt real API calls"""
    return USE_REALTIME


def get_confidence_threshold() -> float:
    """Get appropriate confidence threshold for current mode"""
    return REALTIME_CONFIDENCE_THRESHOLD if USE_REALTIME else MOCK_CONFIDENCE_THRESHOLD


def get_mock_latency() -> Tuple[float, float]:
    """Get mock latency range for artificial delays"""
    return MOCK_LATENCY_RANGE


def is_observability_enabled() -> bool:
    """Check if observability is enabled"""
    return ENABLE_TOOL_OBSERVABILITY


# ============================================================================
# STARTUP VALIDATION
# ============================================================================

def validate_configuration():
    """Validate configuration on startup - prints warnings if needed"""
    
    warnings = []
    
    # Check mode configuration
    if USE_REALTIME:
        # Check critical keys
        import os
        missing_critical = [key for key in CRITICAL_API_KEYS if not os.getenv(key)]
        if missing_critical:
            warnings.append(
                f"REALTIME_MODE enabled but missing critical keys: {', '.join(missing_critical)}"
            )
            warnings.append("System may fallback to MOCK mode for affected services")
    
    # Check latency configuration
    if MOCK_LATENCY_RANGE[0] > MOCK_LATENCY_RANGE[1]:
        warnings.append(
            f"Invalid MOCK_LATENCY_RANGE: min ({MOCK_LATENCY_RANGE[0]}) > max ({MOCK_LATENCY_RANGE[1]})"
        )
    
    # Check retry configuration
    if MAX_RETRIES < 1:
        warnings.append(f"MAX_RETRIES ({MAX_RETRIES}) should be >= 1")
    
    if RETRY_BASE_DELAY <= 0:
        warnings.append(f"RETRY_BASE_DELAY ({RETRY_BASE_DELAY}) should be > 0")
    
    # Emit warnings if any
    if warnings:
        print("\n⚠️  Configuration Warnings:")
        for warning in warnings:
            print(f"   - {warning}")
        print()
    
    return len(warnings) == 0


# ============================================================================
# CONFIGURATION DISPLAY
# ============================================================================

def print_configuration():
    """Print current configuration (useful for debugging)"""
    
    print("=" * 70)
    print("🔧 Ghost Protocol - Runtime Configuration")
    print("=" * 70)
    print(f"Runtime Mode:           {get_current_mode()}")
    print(f"Mock Mode (final):      {'ENABLED' if FINAL_MOCK_MODE else 'DISABLED'}")
    print(f"Force Realtime Override:{'ACTIVE' if FORCE_REALTIME_OVERRIDE else 'INACTIVE'}")
    print(f"Confidence Threshold:   {get_confidence_threshold():.2f}")
    print(f"Mock Latency Range:     {MOCK_LATENCY_RANGE[0]:.1f}s - {MOCK_LATENCY_RANGE[1]:.1f}s")
    print(f"Max Retries:            {MAX_RETRIES}")
    print(f"API Timeout:            {API_TIMEOUT}s")
    print(f"Observability:          {'Enabled' if ENABLE_TOOL_OBSERVABILITY else 'Disabled'}")
    print(f"Log Realtime Errors:    {'Yes' if LOG_REALTIME_ERRORS else 'No'}")
    print(f"Log Mode Switches:      {'Yes' if LOG_MODE_SWITCHES else 'No'}")
    print("=" * 70)
    print()


# ============================================================================
# AUTO-VALIDATION ON IMPORT
# ============================================================================

# Validate configuration when module is imported
_config_valid = validate_configuration()

# Print configuration if in debug mode
if os.getenv("DEBUG_CONFIG", "False").lower() == "true":
    print_configuration()


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    # Mode flags
    "REALTIME_MODE",
    "USE_REALTIME",
    "FINAL_MOCK_MODE",
    "FORCE_REALTIME_OVERRIDE",
    "MOCK_LATENCY_RANGE",
    "LOG_REALTIME_ERRORS",
    "LOG_MODE_SWITCHES",
    "LOG_KEY_VALIDATION",
    
    # Retry configuration
    "MAX_RETRIES",
    "RETRY_BASE_DELAY",
    "RETRY_JITTER",
    "API_TIMEOUT",
    "RATE_LIMIT_PER_MINUTE",
    
    # Observability
    "ENABLE_TOOL_OBSERVABILITY",
    "TOOL_LOG_LEVEL",
    "EMIT_TOOL_METRICS",
    "EMIT_TOOL_TRACES",
    
    # Agent configuration
    "REALTIME_CONFIDENCE_THRESHOLD",
    "MOCK_CONFIDENCE_THRESHOLD",
    "MOCK_ASSET_COUNT_BOOST",
    
    # API keys
    "CRITICAL_API_KEYS",
    "OPTIONAL_API_KEYS",
    
    # Helper functions
    "get_current_mode",
    "should_use_realtime",
    "get_confidence_threshold",
    "get_mock_latency",
    "is_observability_enabled",
    "validate_configuration",
    "print_configuration",
]
