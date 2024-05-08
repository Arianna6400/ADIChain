"""
Custom logging module to handle both error and info loggings for the application.
This module setups file handlers, formatters, and loggers.
"""

import logging
import os

def setup_logging(log_path, level, formatter):
    """
    Setup and return a logger with a file handler if it does not already exist.
    
    Args:
    log_path (str): Path where the log file will be saved.
    level (int): Logging level, e.g., logging.INFO, logging.ERROR.
    formatter (str): Format string for log messages.
    
    Returns:
    logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(log_path)

    if not logger.handlers:
        full_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_path)
        log_dir = os.path.dirname(full_log_path)
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        handler = logging.FileHandler(full_log_path)
        handler.setLevel(level)
        formatter = logging.Formatter(formatter)
        handler.setFormatter(formatter)
        
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False
    
    return logger

def log_error(error):
    """
    Log an error message to the error log file.
    
    Args:
    error (str): Error message to log.
    """
    error_log_path = '../../except.log'
    error_logger = setup_logging(error_log_path, logging.ERROR, 
                                 '%(asctime)s - %(levelname)s - %(message)s')
    error_logger.error(error)

def log_msg(message):
    """
    Log a regular message to the action log file.
    
    Args:
    message (str): Message to log.
    """
    info_log_path = '../../action_logs.txt'
    info_logger = setup_logging(info_log_path, logging.INFO, 
                                '%(asctime)s - %(levelname)s - %(message)s')
    info_logger.info(message)
