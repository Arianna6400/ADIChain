import logging
import os

def setup_logging(log_path, level, formatter):
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
    error_log_path = '../../except.log'  
    error_logger = setup_logging(error_log_path, logging.ERROR, '%(asctime)s - %(levelname)s - %(message)s')
    error_logger.error(error)

def log_msg(message):
    info_log_path = '../../action_logs.txt'  
    info_logger = setup_logging(info_log_path, logging.INFO, '%(asctime)s - %(levelname)s - %(message)s')
    info_logger.info(message)
