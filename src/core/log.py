import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"
#enum valid log levels
class LogLevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"

def configure_logging(log_level: str = LogLevels.error):
    """
       Configures the logging settings for the application.
        Put this function in main.py to set up logging.
            configure_logging(LogLevels.debug)

       Args:
           log_level (str): The desired logging level. Defaults to LogLevels.error.
                           Valid values are "INFO", "WARN", "ERROR", "DEBUG".

       Behavior:
           - If the provided log_level is invalid, the logging level is set to "ERROR".
           - If the log_level is "DEBUG", a detailed log format is used.
           - For other valid log levels, the default log format is used.
       """
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return
    logging.basicConfig(level=log_level)
#Use this to test logging configuration
if __name__ == '__main__':
    configure_logging(LogLevels.info)
    logging.debug("This is a debug log")
    logging.info("This is an info log")
    logging.warning("This is a warning log")
    logging.error("This is an error log")
    logging.critical("This is a critical log")
