# monitor.py - Monitoring system for the scraper

import logging
import time
import psutil
import os
from datetime import datetime

# ________________________________
# 1. LOGGING SETUP
# ________________________________
def setup_logger():
    """Create and configer the logger."""
    # Log file named with today's date e.g. logs/scraper_2026-03-20.log
    log_filename = f"logs/scraper_{datetime.now().strftime('%Y-%m-%d')}.log"

    logging.basicConfig(
        level=logging.INFO, #Record INFO and above (INFO, WARNING, ERROR)
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_filename), #Save to file
            logging.StreamHandler() # Also print to terminal
        ]
    )
    return logging.getLogger(__name__)

#now I need to create a global logger to ues everywhere
logger = setup_logger()

# ________________________________
# 2. PERFORMANCE MONITOR CLASS
# ________________________________
class ScraperMonitor:
    """Tracks performance matrics during scraping."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.pages_scraped = 0
        self.books_scraped = 0
        self.errors = []
        self.page_times = [] # How long each page took

    def start(self):
        """Call this when the scraper starts."""
        self.start_time = time.time()
        logger.info("=" * 50)
        logger.info("SCRAPER STARTED")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 50)
