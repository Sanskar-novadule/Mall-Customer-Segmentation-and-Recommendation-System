from backend.logger import logger
from backend.database import log_error


def handle_exception(
    error,
    endpoint=None,
    upload_id=None,
):
    """
    Central application error handler.

    Logs the error using Structlog
    and stores the error in PostgreSQL.
    """

    error_type = type(error).__name__
    error_message = str(error)

    # 1. Structlog
    logger.error(
        "application_error",
        endpoint=endpoint,
        upload_id=upload_id,
        error_type=error_type,
        error_message=error_message,
    )

    # 2. PostgreSQL
    try:
        log_error(
            error_type=error_type,
            error_message=error_message,
            endpoint=endpoint,
            upload_id=upload_id,
        )

    except Exception as logging_error:

        logger.error(
            "database_error_logging_failed",
            error_type=type(logging_error).__name__,
            error_message=str(logging_error),
        )