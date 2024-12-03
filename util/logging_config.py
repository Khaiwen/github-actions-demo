import logging

def setup_logging(log_level=logging.INFO, log_format=None):
    """Configures logging for the application."""
    if log_format is None:
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(level=log_level, format=log_format)