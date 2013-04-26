import sys
import logging

log = logging.getLogger('slapi')

LOG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'


def configure_log(log, log_level, log_format=LOG_FORMAT):
    # Clear existing log handlers
    log.handlers = []

    # Configure Log Formatting
    formatter = logging.Formatter(log_format)

    # Configure Logging Level
    try:
        log.setLevel(getattr(logging, log_level))
    except AttributeError:
        log.warn("Unknown logging level: %s" % (log_level))
        log.setLevel(logging.INFO)

    # Configure Handler
    streamhandler = logging.StreamHandler(sys.stdout)
    streamhandler.setFormatter(formatter)
    log.addHandler(streamhandler)
