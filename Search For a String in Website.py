import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin

# Function to fetch and parse a web page, searching for the string
def fetch_and_search_url(base_url, search_string):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        return None

    # Search for the string in all paragraphs
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        if search_string in paragraph.get_text():
            return base_url

    return None

# Function to extract URLs containing a specific string from a website
def extract_urls_with_string(base_url, search_string, max_workers=5):
    visited = set()
    queue = [(base_url, 0)]
    result_urls = set()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while queue:
            current_url, depth = queue.pop(0)

            # Check if we have already visited this URL
            if current_url in visited:
                continue

            # Fetch and search the current URL in parallel
            future = executor.submit(fetch_and_search_url, current_url, search_string)

            if future.result() is not None:
                result_urls.add(future.result())

            # Add current URL to visited set
            visited.add(current_url)

            # Continue to one level of subpages
            if depth < 1:
                try:
                    response = requests.get(current_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                except Exception as e:
                    continue

                for link in soup.find_all('a', href=True):
                    subpage_url = urljoin(current_url, link['href'])
                    parsed_url = urlparse(subpage_url)
                    if parsed_url.netloc == urlparse(base_url).netloc:
                        queue.append((subpage_url, depth + 1))

    return result_urls

# User inputs
base_url = "https://phet-dev.colorado.edu/html/build-an-atom/0.0.0-3/simple-text-only-test-page.html"
search_string = input("Enter the string to search for: ")

# Call the function to extract URLs
result_urls = extract_urls_with_string(base_url, search_string)

# Print the URLs containing the specified string
for url in result_urls:
    print(url)
