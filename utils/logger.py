import logging
import os
from pathlib import Path

def setup_logger():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("PDFEditor")
    logger.setLevel(logging.DEBUG)
    
    # File handler
    fh = logging.FileHandler(log_dir / "app.log")
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger

logger = setup_logger()
