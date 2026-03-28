import logging
import json
from contextlib import contextmanager
from datetime import datetime
import time
from typing import Dict, Any, Optional

def setup_json_logger(name: str) -> logging.Logger:
    """Provides a basic structured logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Simple JSON formatter
    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            log_record = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "name": record.name,
                "message": record.getMessage()
            }
            if hasattr(record, "trace_id"):
                log_record["trace_id"] = record.trace_id # type: ignore
            return json.dumps(log_record)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    
    # Avoid duplicate handlers if setup multiple times
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

@contextmanager
def trace_span(logger: logging.Logger, span_name: str, trace_id: Optional[str] = None):
    """
    Context manager to trace execution duration of a step.
    Produces structured start/end logs.
    """
    start_time = time.time()
    logger.info(f"SPAN_START: {span_name}", extra={"trace_id": trace_id} if trace_id else {})
    yield
    latency_ms = int((time.time() - start_time) * 1000)
    logger.info(f"SPAN_END: {span_name} ({latency_ms}ms)", extra={"trace_id": trace_id} if trace_id else {})
