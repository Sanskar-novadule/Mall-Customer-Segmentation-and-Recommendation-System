import logging

import structlog


logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(
            fmt="iso"
        ),
        structlog.dev.ConsoleRenderer(),
    ],
)


logger = structlog.get_logger()