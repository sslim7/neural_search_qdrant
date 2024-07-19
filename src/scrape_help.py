from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import time
import os

base_url = "https://help.swit.io"
visited_urls = set()
data = []

session = HTMLSession()

def scrape_page(url):
    if url in visited_urls or not url.startswith(base_url):
        return

    print(f"Scraping {url}")
    visited_urls.add(url)
    response = session.get(url)
    response.html.render()  # JavaScript를 실행하여 페이지의 전체 내용을 로드합니다.
    soup = BeautifulSoup(response.html.html, "html.parser")

    # Get title
    title = soup.find("title").text if soup.find("title") else "No title"

    # Get meta description
    meta_description = soup.find("meta", attrs={"name": "description"})
    description = meta_description['content'] if meta_description else "No description"
    print("\ntitle:\n", title)
    print("\ndescription:\n", description)
    # Get content from the article
    content_div = soup.select_one("article")
    if content_div:
        print("\ncontent:\n", content_div.text.strip())
        data.append({
            "title": title,
            "description": description,
            "content": content_div.text.strip(),
            "url": url
        })
    else:
        print(f"No article content found at {url}")

    # Find all links to other help pages
    links = soup.find_all("a", href=True)
    for link in links:
        full_url = base_url + link['href'] if link['href'].startswith("/") else link['href']
        scrape_page(full_url)
        time.sleep(0.1)  # Add a delay to avoid overloading the server

# Start scraping from the base URL
scrape_page(base_url)

# Ensure the data directory exists
data_dir = os.path.join("..", "data")
os.makedirs(data_dir, exist_ok=True)

# Save the data to a JSON file
with open(os.path.join(data_dir, "swit_help_center.json"), "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Scraped {len(data)} pages.")