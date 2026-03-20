# config.py - Central configuration for the project

BASE_URL = "http://books.toscrape.com/catalogue/"
START_URL = "http://books.toscrape.com/catalogue/page-1.html"

# How many pages to scrape (keep it small to start)
MAX_PAGES = 5

# Output file
OUTPUT_FILE = "reports/books_data.csv"

# Rating word-to-number mapping
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}