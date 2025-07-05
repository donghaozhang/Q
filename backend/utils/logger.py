import logging, os
try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False
    # Fallback to regular logging if structlog not available
    class MockStructlog:
        processors = type('processors', (), {
            'JSONRenderer': lambda: lambda x: x,
            'dict_tracebacks': lambda x: x,
            'TimeStamper': lambda fmt: lambda x: x,
            'CallsiteParameterAdder': lambda params: lambda x: x,
            'CallsiteParameter': type('CallsiteParameter', (), {
                'FILENAME': 'filename',
                'FUNC_NAME': 'func_name', 
                'LINENO': 'lineno'
            })()
        })()
        dev = type('dev', (), {'ConsoleRenderer': lambda: lambda x: x})()
        stdlib = type('stdlib', (), {
            'add_log_level': lambda x: x,
            'PositionalArgumentsFormatter': lambda: lambda x: x,
            'BoundLogger': logging.Logger
        })()
        contextvars = type('contextvars', (), {
            'merge_contextvars': lambda x: x
        })()
        def configure(self, **kwargs): pass
        def get_logger(self, **kwargs): return logging.getLogger(__name__)
    structlog = MockStructlog()

ENV_MODE = os.getenv("ENV_MODE", "LOCAL")

if STRUCTLOG_AVAILABLE:
    renderer = [structlog.processors.JSONRenderer()]
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
else:
    # Use regular logging when structlog is not available
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
