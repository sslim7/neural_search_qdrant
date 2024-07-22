from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import time
import os

base_url = "https://help.swit.io"
lang = "?lang=ko"
visited_urls = set()
data = []

session = HTMLSession()

def scrape_page(url, retries=3):
    if url in visited_urls or not url.startswith(base_url):
        return

    print(f"Scraping {url}")
    visited_urls.add(url)

    try:
        response = session.get(url)
        response.html.render(timeout=30)  # JavaScript를 실행하여 페이지의 전체 내용을 로드합니다.
        soup = BeautifulSoup(response.html.html, "html.parser")

        # Get title
        title = soup.find("title").text if soup.find("title") else "No title"

        # Get meta description
        meta_description = soup.find("meta", attrs={"name": "description"})
        description = meta_description['content'] if meta_description else "No description"

        # Get content from the article
        content_div = soup.select_one("article")
        if content_div:
            data.append({
                "url": url,
                "title": title,
                "description": description,
                "content": content_div.text.strip()
            })
        else:
            print(f"No article content found at {url}")

        # Find all links to other help pages
        links = soup.find_all("a", href=True)
        for link in links:
            full_url = link['href']
            if full_url.startswith("/"):
                full_url = base_url + full_url
                if "?" not in full_url:
                    full_url += lang
            elif base_url in full_url and lang not in full_url:
                full_url += lang
            scrape_page(full_url)
            time.sleep(0.1)  # Add a delay to avoid overloading the server

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        if retries > 0:
            print(f"Retrying ({retries} retries left)...")
            time.sleep(5)  # Add a delay before retrying
            scrape_page(url, retries - 1)
        else:
            print(f"Failed to scrape {url} after several retries.")

    # Save progress intermittently
    if len(data) % 10 == 0:
        save_data()

def save_data():
    data_dir = os.path.join("..", "data")
    os.makedirs(data_dir, exist_ok=True)

    # Save the data to a JSON file
    with open(os.path.join(data_dir, "swit_help_center_ko.json"), "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(data)} pages.")

# Start scraping from the base URL
scrape_page(base_url + lang)

# Save the final data to a JSON file
save_data()

print(f"Scraped {len(data)} pages.")