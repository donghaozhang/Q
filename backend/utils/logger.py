import logging, os
try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False
    # Fallback to regular logging if structlog not available
    class MockStructlog:
        processors = type('processors', (), {'JSONRenderer': lambda: lambda x: x})()
        def get_logger(self): return logging.getLogger(__name__)
    structlog = MockStructlog()

ENV_MODE = os.getenv("ENV_MODE", "LOCAL")

renderer = [structlog.processors.JSONRenderer()] if STRUCTLOG_AVAILABLE else []
if ENV_MODE.lower() == "local".lower():
    renderer = [structlog.dev.ConsoleRenderer()]

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.dict_tracebacks,
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.contextvars.merge_contextvars,
        *renderer,
    ],
    cache_logger_on_first_use=True,
)

logger: structlog.stdlib.BoundLogger = structlog.get_logger(level=logging.DEBUG)
