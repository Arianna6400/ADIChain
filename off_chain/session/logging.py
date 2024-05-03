import logging

logging.basicConfig(filename='except.log', level=logging.ERROR)

def log_error(error):
    # Log level ERROR
    logging.error(f"An error occurred: {error}")