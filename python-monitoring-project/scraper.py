#scraper.py - Main automation script
# Scrapes book data from books.toscrape.con
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from config import BASE_URL, START_URL, MAX_PAGES, OUTPUT_FILE, RATING_MAP

def get_page(url):
    """Fetch a single page and return BeautifulSoup object."""
    response = requests.get(url, timeout=10)
    response.raise_for_status() #Raises error if request fails
    return BeautifulSoup(response.text, "html.parser")

def parse_books(soup):
    """Extract book data from a single page."""
    books = []
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        title = article.h3.a["title"]
        price = article.find("p", class_='price_color').text.strip()
        rating_word = article.p['class'][1] #e.g, "Three"
        rating = RATING_MAP.get(rating_word, 0)

        books.append({
            "title": title,
            'price': price,
            'rating': rating
        })
    return books

def get_next_page(soup, current_url):
    """Find the URL of the next page, if it exists."""
    next_btn = soup.find('li', class_='next')
    if next_btn:
        next_href = next_btn.a['href']
        return BASE_URL + next_href
    return None

def run_scraper():
    """Main function to run the scraper."""
    print("Starting scraper...")
    all_books = []
    url = START_URL
    page_number = 1
    while url and page_number <= MAX_PAGES:
        print(f"Scraping page {page_number}: {url}")

        soup = get_page(url)
        books = parse_books(soup)
        all_books.extend(books)

        print(f"  Found {len(books)} books on page {page_number}")

        url = get_next_page(soup, url)
        page_number += 1
        time.sleep(1) # Polite delay between requests

    #now we need to save to CSV
    df = pd.DataFrame(all_books)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nDone! Scraped {len(all_books)} books total.")
    print(f"Data saved to: {OUTPUT_FILE}")

    return all_books

if __name__ == "__main__":
    run_scraper()