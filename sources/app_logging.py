import logging

# Create or get a logger
logger = logging.getLogger('example_logger')

# Set the minimum level of log messages the logger will handle
logger.setLevel(logging.DEBUG)

# Create a handler and set its level
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# Create a formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# Attach the handler to the logger
logger.addHandler(stream_handler)

# Log messages
logger.info("####### App logging examples with python #######")
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
