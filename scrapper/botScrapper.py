import requests
from bs4 import BeautifulSoup
import random
import time
import csv

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)...",
    # Add more user agents if you want
]

def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS)
    }

def scrape_page(url):
    try:
        headers = get_random_headers()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # TODO: update selector to your target data
        items = []
        for elem in soup.select('div.example_class'):
            title = elem.get_text(strip=True)
            items.append(title)
        return items
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []

def main():
    base_url = "https://example.com/page="
    all_data = []
    for page in range(1, 6):  # scrape first 5 pages
        url = base_url + str(page)
        print(f"Scraping {url}")
        data = scrape_page(url)
        if not data:
            print("No data found, stopping.")
            break
        all_data.extend(data)
        time.sleep(random.uniform(2,5))  # random delay

    # Save to CSV
    with open("scraped_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title"])
        for item in all_data:
            writer.writerow([item])
    print(f"Saved {len(all_data)} items to scraped_data.csv")

if __name__ == "__main__":
    main()

