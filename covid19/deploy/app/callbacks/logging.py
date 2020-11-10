import logging
import os

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(os.environ.get('LOGLEVEL', 'WARNING'))
    fh = logging.FileHandler('logs/log.out')
    fh.setLevel(os.environ.get('LOGLEVEL', 'WARNING'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger