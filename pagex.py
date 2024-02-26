import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def get_urls_from_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            urls = set()
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    parsed_url = urlparse(href)
                    if parsed_url.scheme and parsed_url.netloc:  # Check if it's an absolute URL
                        urls.add(href)
                    elif href.startswith('/'):  # Check if it's a relative URL
                        base_url = urlparse(url)
                        full_url = f"{base_url.scheme}://{base_url.netloc}{href}"
                        urls.add(full_url)
            return urls
        else:
            print("Failed to fetch page:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def process_url(url):
    urls = get_urls_from_page(url)
    if urls:
        print("URLs found on the page:")
        for u in urls:
            print(u)
    else:
        print("Failed to retrieve URLs from the page.")

if __name__ == "__main__":
    if not sys.stdin.isatty():  # Check if data is being piped in
        urls = [line.strip() for line in sys.stdin]
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(process_url, urls)
    else:
        print("No input provided via pipe.")
