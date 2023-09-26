"""Create and modify Logger
"""
import logging

class CustomFormatter(logging.Formatter):
    bold_on = '\x1b[1m'
    bold_off = '\x1b[22m'

    magenta = '\x1b[35m'
    cyan = '\x1b[36m'
    yellow = '\x1b[33m'
    red = '\x1b[31m'

    reset = '\x1b[0m'

    format = ' - %(filename)s:%(lineno)d]: %(message)s'

    FORMATS = {
        logging.DEBUG: magenta + '\n[' + bold_on + '%(levelname)s' + bold_off + format + reset,
        logging.INFO: cyan + '\n[' + bold_on + '%(levelname)s' + bold_off + format + reset,
        logging.WARNING: yellow + '\n[' + bold_on + '%(levelname)s' + bold_off + format + reset,
        logging.ERROR: red + '\n[' + bold_on + '%(levelname)s' + bold_off + format + reset,
        logging.CRITICAL: red + bold_on + '\n[' + '%(levelname)s' + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Creates logger for file and sets level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # This can be changed for later use in error/logging handling

# Add a colored console handler with the custom formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(console_handler)

def main():
    """For testing
    """
    logger.debug('This is a debug-level message')
    logger.info('This is an info-level message')
    logger.warning('This is a warning-level message')
    logger.error('This is an error-level message')
    logger.critical('This is a critical-level message')


if __name__ == '__main__':
    main()