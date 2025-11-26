"""
Ghost Protocol - Observability Layer
Logging, Tracing, Metrics, and Evaluation
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import time


# ============================================================================
# 1. STRUCTURED LOGGING MODULE
# ============================================================================

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class LogEntry:
    timestamp: str
    level: LogLevel
    message: str
    agent_id: Optional[str] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    error: Optional[Dict] = None


class StructuredLogger:
    """Structured logging for all agent operations"""
    
    def __init__(self, service_name: str = "ghost-protocol"):
        self.service_name = service_name
        self.logs: List[LogEntry] = []
        self.log_handlers: List = []
    
    def debug(self, message: str, **kwargs):
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, error: Optional[Exception] = None, **kwargs):
        error_dict = None
        if error:
            error_dict = {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": None  # Would include full traceback
            }
        self._log(LogLevel.ERROR, message, error=error_dict, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log(LogLevel.CRITICAL, message, **kwargs)
    
    def _log(self, level: LogLevel, message: str, **kwargs):
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level,
            message=message,
            agent_id=kwargs.get("agent_id"),
            session_id=kwargs.get("session_id"),
            trace_id=kwargs.get("trace_id"),
            span_id=kwargs.get("span_id"),
            metadata=kwargs.get("metadata", {}),
            error=kwargs.get("error")
        )
        
        self.logs.append(entry)
        self._emit(entry)
    
    def _emit(self, entry: LogEntry):
        """Emit log to handlers (console, file, cloud)"""
        log_dict = {
            "timestamp": entry.timestamp,
            "level": entry.level.value,
            "service": self.service_name,
            "message": entry.message,
            "agent_id": entry.agent_id,
            "session_id": entry.session_id,
            "trace_id": entry.trace_id,
            "span_id": entry.span_id,
            "metadata": entry.metadata
        }
        
        if entry.error:
            log_dict["error"] = entry.error
        
        # Print to console (would send to CloudWatch/Datadog in production)
        print(json.dumps(log_dict, indent=2))
    
    def query_logs(self, session_id: Optional[str] = None, 
                   agent_id: Optional[str] = None,
                   level: Optional[LogLevel] = None,
                   limit: int = 100) -> List[LogEntry]:
        """Query logs with filters"""
        filtered = self.logs
        
        if session_id:
            filtered = [log for log in filtered if log.session_id == session_id]
        if agent_id:
            filtered = [log for log in filtered if log.agent_id == agent_id]
        if level:
            filtered = [log for log in filtered if log.level == level]
        
        return filtered[-limit:]


# ============================================================================
# 2. TRACING SPANS
# ============================================================================

@dataclass
class Span:
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    operation_name: str
    agent_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    status: str = "in_progress"  # in_progress, success, error
    tags: Dict = field(default_factory=dict)
    logs: List[Dict] = field(default_factory=list)
    error: Optional[Dict] = None


class Tracer:
    """Distributed tracing for agent operations"""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.active_spans: Dict[str, Span] = {}
        self.completed_spans: List[Span] = []
        self.traces: Dict[str, List[str]] = {}  # trace_id -> span_ids
    
    def start_span(self, operation_name: str, agent_id: str,
                   trace_id: Optional[str] = None,
                   parent_span_id: Optional[str] = None,
                   tags: Optional[Dict] = None) -> str:
        """Start a new tracing span"""
        
        if trace_id is None:
            trace_id = self._generate_trace_id()
        
        span_id = self._generate_span_id()
        
        span = Span(
            span_id=span_id,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            operation_name=operation_name,
            agent_id=agent_id,
            start_time=datetime.now(),
            tags=tags or {}
        )
        
        self.active_spans[span_id] = span
        
        if trace_id not in self.traces:
            self.traces[trace_id] = []
        self.traces[trace_id].append(span_id)
        
        self.logger.info(
            f"Span started: {operation_name}",
            agent_id=agent_id,
            trace_id=trace_id,
            span_id=span_id,
            metadata={"operation": operation_name}
        )
        
        return span_id
    
    def end_span(self, span_id: str, status: str = "success", 
                 error: Optional[Exception] = None):
        """End a tracing span"""
        
        if span_id not in self.active_spans:
            self.logger.warning(f"Span {span_id} not found")
            return
        
        span = self.active_spans[span_id]
        span.end_time = datetime.now()
        span.duration_ms = (span.end_time - span.start_time).total_seconds() * 1000
        span.status = status
        
        if error:
            span.error = {
                "type": type(error).__name__,
                "message": str(error)
            }
        
        self.completed_spans.append(span)
        del self.active_spans[span_id]
        
        self.logger.info(
            f"Span completed: {span.operation_name}",
            agent_id=span.agent_id,
            trace_id=span.trace_id,
            span_id=span_id,
            metadata={
                "duration_ms": span.duration_ms,
                "status": status
            }
        )
    
    def add_span_log(self, span_id: str, message: str, metadata: Optional[Dict] = None):
        """Add log entry to span"""
        if span_id in self.active_spans:
            self.active_spans[span_id].logs.append({
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "metadata": metadata or {}
            })
    
    def set_span_tag(self, span_id: str, key: str, value: Any):
        """Set tag on span"""
        if span_id in self.active_spans:
            self.active_spans[span_id].tags[key] = value
    
    def get_trace(self, trace_id: str) -> List[Span]:
        """Get all spans for a trace"""
        span_ids = self.traces.get(trace_id, [])
        spans = []
        
        for sid in span_ids:
            # Check active and completed
            if sid in self.active_spans:
                spans.append(self.active_spans[sid])
            else:
                for completed in self.completed_spans:
                    if completed.span_id == sid:
                        spans.append(completed)
                        break
        
        return spans
    
    def _generate_trace_id(self) -> str:
        import hashlib
        raw = f"trace_{datetime.now().isoformat()}_{id(self)}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
    
    def _generate_span_id(self) -> str:
        import hashlib
        raw = f"span_{datetime.now().isoformat()}_{id(self)}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12]


class TracingContext:
    """Context manager for tracing spans"""
    
    def __init__(self, operation_name: str, trace_id: str, agent_id: str = "unknown"):
        self.operation_name = operation_name
        self.trace_id = trace_id
        self.agent_id = agent_id
        self.span_id = None
        self.child_spans = []
    
    def __enter__(self):
        # In a real implementation, this would use the global tracer
        # For now, we just track the trace_id
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up span
        pass
    
    def add_child_span(self, name: str):
        """Add a child span (for documentation)"""
        self.child_spans.append(name)


# ============================================================================
# 3. METRICS COLLECTION
# ============================================================================

@dataclass
class MetricPoint:
    metric_name: str
    value: float
    timestamp: datetime
    tags: Dict = field(default_factory=dict)


class MetricsCollector:
    """Collect and aggregate metrics"""
    
    def __init__(self):
        self.metrics: List[MetricPoint] = []
        self.counters: Dict[str, float] = {}
        self.gauges: Dict[str, float] = {}
    
    # ---- Accuracy Metrics ----
    
    def record_death_detection_accuracy(self, confidence: float, was_correct: bool,
                                       session_id: str):
        """Record death detection accuracy"""
        self._record_metric(
            "death_detection.accuracy",
            1.0 if was_correct else 0.0,
            tags={"confidence": str(confidence), "session_id": session_id}
        )
        
        self._record_metric(
            "death_detection.confidence",
            confidence,
            tags={"session_id": session_id}
        )
    
    def record_asset_discovery_accuracy(self, discovered: int, total: int,
                                       session_id: str):
        """Record asset discovery completeness"""
        accuracy = discovered / total if total > 0 else 0.0
        
        self._record_metric(
            "asset_discovery.accuracy",
            accuracy,
            tags={"session_id": session_id}
        )
        
        self._record_metric(
            "asset_discovery.count",
            discovered,
            tags={"session_id": session_id}
        )
    
    def record_message_delivery_success(self, success: bool, recipient: str,
                                       session_id: str):
        """Record legacy message delivery"""
        self._record_metric(
            "legacy.delivery_success",
            1.0 if success else 0.0,
            tags={"recipient": recipient, "session_id": session_id}
        )
    
    def record_contract_execution_success(self, success: bool, gas_used: float,
                                         session_id: str):
        """Record smart contract execution"""
        self._record_metric(
            "contract.execution_success",
            1.0 if success else 0.0,
            tags={"session_id": session_id}
        )
        
        self._record_metric(
            "contract.gas_used",
            gas_used,
            tags={"session_id": session_id}
        )
    
    # ---- Latency Metrics ----
    
    def record_tool_latency(self, tool_name: str, latency_ms: float):
        """Record tool execution latency"""
        self._record_metric(
            f"tool.latency_ms",
            latency_ms,
            tags={"tool_name": tool_name}
        )
    
    def record_agent_latency(self, agent_name: str, latency_ms: float = None,
                            duration_ms: float = None, session_id: str = ""):
        """Record agent execution latency"""
        # Support both parameter names for compatibility
        latency = latency_ms or duration_ms or 0.0
        self._record_metric(
            f"agent.latency_ms.{agent_name}",
            latency,
            tags={"session_id": session_id}
        )
    
    def record_pipeline_latency(self, duration_ms: float, session_id: str):
        """Record end-to-end pipeline latency"""
        self._record_metric(
            "pipeline.total_latency_ms",
            duration_ms,
            tags={"session_id": session_id}
        )
    
    # ---- User Satisfaction Metrics ----
    
    def record_family_satisfaction(self, rating: float, session_id: str,
                                  feedback: Optional[str] = None):
        """Record family satisfaction rating (1-5 scale)"""
        self._record_metric(
            "satisfaction.family_rating",
            rating,
            tags={"session_id": session_id, "feedback": feedback or "none"}
        )
    
    def record_message_quality_score(self, score: float, recipient: str,
                                    session_id: str):
        """Record AI-generated message quality (0-1 scale)"""
        self._record_metric(
            "satisfaction.message_quality",
            score,
            tags={"recipient": recipient, "session_id": session_id}
        )
    
    # ---- Time Saved Metrics ----
    
    def record_time_saved(self, task_type: str, estimated_manual_hours: float,
                         actual_hours: float, session_id: str):
        """Record time saved vs manual process"""
        time_saved = estimated_manual_hours - actual_hours
        
        self._record_metric(
            "efficiency.time_saved_hours",
            time_saved,
            tags={"task": task_type, "session_id": session_id}
        )
        
        self._record_metric(
            "efficiency.automation_ratio",
            1 - (actual_hours / estimated_manual_hours) if estimated_manual_hours > 0 else 0,
            tags={"task": task_type, "session_id": session_id}
        )
    
    # ---- Core Methods ----
    
    def _record_metric(self, metric_name: str, value: float, tags: Optional[Dict] = None):
        """Record a metric point"""
        point = MetricPoint(
            metric_name=metric_name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {}
        )
        self.metrics.append(point)
    
    def increment_counter(self, counter_name: str, value: float = 1.0):
        """Increment a counter"""
        if counter_name not in self.counters:
            self.counters[counter_name] = 0.0
        self.counters[counter_name] += value
    
    def set_gauge(self, gauge_name: str, value: float):
        """Set a gauge value"""
        self.gauges[gauge_name] = value
    
    def get_metrics(self, metric_name: str, 
                   time_range_minutes: Optional[int] = None) -> List[MetricPoint]:
        """Query metrics"""
        filtered = [m for m in self.metrics if m.metric_name == metric_name]
        
        if time_range_minutes:
            cutoff = datetime.now() - timedelta(minutes=time_range_minutes)
            filtered = [m for m in filtered if m.timestamp >= cutoff]
        
        return filtered
    
    def aggregate_metric(self, metric_name: str, aggregation: str = "avg",
                        time_range_minutes: Optional[int] = None) -> float:
        """Aggregate metrics (avg, sum, min, max, count)"""
        points = self.get_metrics(metric_name, time_range_minutes)
        
        if not points:
            return 0.0
        
        values = [p.value for p in points]
        
        if aggregation == "avg":
            return sum(values) / len(values)
        elif aggregation == "sum":
            return sum(values)
        elif aggregation == "min":
            return min(values)
        elif aggregation == "max":
            return max(values)
        elif aggregation == "count":
            return len(values)
        else:
            return 0.0


# ============================================================================
# 4. AGENT EVALUATION RUNNER
# ============================================================================

@dataclass
class EvaluationCase:
    case_id: str
    agent_name: str
    input_data: Dict
    expected_output: Any
    ground_truth: Dict
    tags: List[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    case_id: str
    agent_name: str
    success: bool
    actual_output: Any
    expected_output: Any
    accuracy_score: float
    latency_ms: float
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class AgentEvaluator:
    """Evaluate agent performance on test datasets"""
    
    def __init__(self, logger: StructuredLogger, metrics: MetricsCollector):
        self.logger = logger
        self.metrics = metrics
        self.test_cases: List[EvaluationCase] = []
        self.results: List[EvaluationResult] = []
    
    def add_test_case(self, case: EvaluationCase):
        """Add evaluation test case"""
        self.test_cases.append(case)
    
    def load_mock_dataset(self):
        """Load mock evaluation dataset"""
        
        # DeathDetectionAgent test cases
        self.test_cases.extend([
            EvaluationCase(
                case_id="dd_001",
                agent_name="DeathDetectionAgent",
                input_data={
                    "user_id": "user_001",
                    "full_name": "John Doe",
                    "sources": ["obituary", "death_registry", "social_media"]
                },
                expected_output={"is_confirmed": True, "confidence": 0.98},
                ground_truth={"actually_deceased": True},
                tags=["death_detection", "high_confidence"]
            ),
            EvaluationCase(
                case_id="dd_002",
                agent_name="DeathDetectionAgent",
                input_data={
                    "user_id": "user_002",
                    "full_name": "Jane Smith",
                    "sources": ["social_media"]
                },
                expected_output={"is_confirmed": False, "confidence": 0.3},
                ground_truth={"actually_deceased": False},
                tags=["death_detection", "low_confidence"]
            )
        ])
        
        # DigitalAssetAgent test cases
        self.test_cases.extend([
            EvaluationCase(
                case_id="da_001",
                agent_name="DigitalAssetAgent",
                input_data={
                    "user_id": "user_001",
                    "vault_path": "/mock/vault.kdbx"
                },
                expected_output={"total_assets": 15},
                ground_truth={"actual_total": 15, "missed": 0},
                tags=["asset_discovery", "complete"]
            ),
            EvaluationCase(
                case_id="da_002",
                agent_name="DigitalAssetAgent",
                input_data={
                    "user_id": "user_003",
                    "vault_path": "/mock/vault2.kdbx"
                },
                expected_output={"total_assets": 8},
                ground_truth={"actual_total": 10, "missed": 2},
                tags=["asset_discovery", "incomplete"]
            )
        ])
        
        # LegacyAgent test cases
        self.test_cases.extend([
            EvaluationCase(
                case_id="lg_001",
                agent_name="LegacyAgent",
                input_data={
                    "user_id": "user_001",
                    "recipient": "son_michael",
                    "context_type": "farewell"
                },
                expected_output={"message_quality": 0.9, "delivery_success": True},
                ground_truth={"family_rating": 4.8},
                tags=["legacy", "high_quality"]
            )
        ])
        
        # SmartContractAgent test cases
        self.test_cases.extend([
            EvaluationCase(
                case_id="sc_001",
                agent_name="SmartContractAgent",
                input_data={
                    "user_id": "user_001",
                    "beneficiaries": {"wallet_1": "0xABC", "wallet_2": "0xDEF"},
                    "assets": [{"type": "ETH", "amount": 2.5}]
                },
                expected_output={"success": True, "gas_used": 0.002},
                ground_truth={"transaction_confirmed": True},
                tags=["smart_contract", "success"]
            )
        ])
    
    async def run_evaluation(self, agent_instance: Any, case: EvaluationCase) -> EvaluationResult:
        """Run single evaluation case"""
        
        start_time = time.time()
        
        try:
            # Execute agent
            actual_output = await agent_instance.execute(case.input_data)
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Calculate accuracy
            accuracy = self._calculate_accuracy(case, actual_output)
            
            # Determine success
            success = accuracy >= 0.8
            
            result = EvaluationResult(
                case_id=case.case_id,
                agent_name=case.agent_name,
                success=success,
                actual_output=actual_output,
                expected_output=case.expected_output,
                accuracy_score=accuracy,
                latency_ms=latency_ms
            )
            
            self.logger.info(
                f"Evaluation completed: {case.case_id}",
                metadata={
                    "accuracy": accuracy,
                    "latency_ms": latency_ms,
                    "success": success
                }
            )
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            
            result = EvaluationResult(
                case_id=case.case_id,
                agent_name=case.agent_name,
                success=False,
                actual_output=None,
                expected_output=case.expected_output,
                accuracy_score=0.0,
                latency_ms=latency_ms,
                error=str(e)
            )
            
            self.logger.error(
                f"Evaluation failed: {case.case_id}",
                error=e,
                metadata={"case_id": case.case_id}
            )
        
        self.results.append(result)
        return result
    
    def _calculate_accuracy(self, case: EvaluationCase, actual_output: Any) -> float:
        """Calculate accuracy score based on agent type"""
        
        if case.agent_name == "DeathDetectionAgent":
            # Compare confidence and correctness
            expected_conf = case.expected_output.get("confidence", 0)
            actual_conf = actual_output.get("confidence", 0)
            conf_diff = abs(expected_conf - actual_conf)
            
            expected_decision = case.expected_output.get("is_confirmed")
            actual_decision = actual_output.get("is_confirmed")
            decision_match = 1.0 if expected_decision == actual_decision else 0.0
            
            return (decision_match * 0.7) + ((1 - conf_diff) * 0.3)
        
        elif case.agent_name == "DigitalAssetAgent":
            # Compare asset counts
            expected_total = case.expected_output.get("total_assets", 0)
            actual_total = actual_output.get("total_assets", 0)
            
            if expected_total == 0:
                return 1.0 if actual_total == 0 else 0.0
            
            return min(actual_total / expected_total, 1.0)
        
        elif case.agent_name == "LegacyAgent":
            # Compare message quality
            expected_quality = case.expected_output.get("message_quality", 0)
            actual_quality = actual_output.get("message_quality", 0)
            
            return 1 - abs(expected_quality - actual_quality)
        
        elif case.agent_name == "SmartContractAgent":
            # Binary success
            expected_success = case.expected_output.get("success", False)
            actual_success = actual_output.get("success", False)
            
            return 1.0 if expected_success == actual_success else 0.0
        
        return 0.0
    
    def generate_report(self) -> Dict:
        """Generate evaluation report with success metrics"""
        
        if not self.results:
            return {"error": "No results available"}
        
        # Overall metrics
        total_cases = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        failed = total_cases - successful
        
        avg_accuracy = sum(r.accuracy_score for r in self.results) / total_cases
        avg_latency = sum(r.latency_ms for r in self.results) / total_cases
        
        # Per-agent metrics
        agent_metrics = {}
        for agent_name in set(r.agent_name for r in self.results):
            agent_results = [r for r in self.results if r.agent_name == agent_name]
            agent_metrics[agent_name] = {
                "total_cases": len(agent_results),
                "successful": sum(1 for r in agent_results if r.success),
                "avg_accuracy": sum(r.accuracy_score for r in agent_results) / len(agent_results),
                "avg_latency_ms": sum(r.latency_ms for r in agent_results) / len(agent_results)
            }
        
        # Error analysis
        errors = [r for r in self.results if r.error]
        error_summary = {}
        for err_result in errors:
            error_type = err_result.error.split(":")[0] if err_result.error else "Unknown"
            error_summary[error_type] = error_summary.get(error_type, 0) + 1
        
        return {
            "summary": {
                "total_cases": total_cases,
                "successful": successful,
                "failed": failed,
                "success_rate": successful / total_cases,
                "avg_accuracy": avg_accuracy,
                "avg_latency_ms": avg_latency
            },
            "agent_metrics": agent_metrics,
            "error_analysis": {
                "total_errors": len(errors),
                "error_types": error_summary
            }
        }
    
    def analyze_failures(self) -> List[Dict]:
        """Detailed failure analysis"""
        failures = [r for r in self.results if not r.success]
        
        analysis = []
        for failure in failures:
            analysis.append({
                "case_id": failure.case_id,
                "agent": failure.agent_name,
                "accuracy_score": failure.accuracy_score,
                "error": failure.error,
                "expected": failure.expected_output,
                "actual": failure.actual_output
            })
        
        return analysis


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_observability_usage():
    """Demonstrate observability in action"""
    
    # Setup
    logger = StructuredLogger("ghost-protocol")
    metrics = MetricsCollector()
    tracer = Tracer(logger)
    
    session_id = "session_123"
    
    # Start trace
    trace_id = tracer._generate_trace_id()
    
    # Agent execution with tracing
    span_id = tracer.start_span(
        "death_detection",
        agent_id="dd_001",
        trace_id=trace_id,
        tags={"session_id": session_id}
    )
    
    # Log agent activity
    logger.info(
        "Starting death detection",
        agent_id="dd_001",
        session_id=session_id,
        trace_id=trace_id,
        span_id=span_id
    )
    
    # Simulate work
    import time
    time.sleep(0.1)
    
    # Record metrics
    metrics.record_death_detection_accuracy(
        confidence=0.98,
        was_correct=True,
        session_id=session_id
    )
    
    metrics.record_agent_latency(
        agent_name="death_detection",
        duration_ms=120.5,
        session_id=session_id
    )
    
    # End span
    tracer.end_span(span_id, status="success")
    
    # Query metrics
    accuracy_metrics = metrics.get_metrics("death_detection.accuracy")
    avg_accuracy = metrics.aggregate_metric("death_detection.accuracy", "avg")
    
    return {
        "trace_id": trace_id,
        "span_id": span_id,
        "avg_accuracy": avg_accuracy
    }
