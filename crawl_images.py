import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import sys

def generate_arrows(n):
    """Returns a string of '>' characters of length n."""
    return '>' * n

def get_image_filenames(url, visited_urls, visited_images, level=0, verbose=False, fullurl=False):
    """
    Recursively crawls a website starting from the given URL,
    and prints filenames of all unique image files found.
    Optionally prints each visited URL to stderr with recursion level info.
    """
    if verbose:
        print(f"{level}:{generate_arrows(level)} {url}", file=sys.stderr)
    
    parsed_url = urlparse(url)
    
    # Ignore webcal: URLs
    if parsed_url.scheme == "webcal":
        return
    
    base_host = parsed_url.netloc
    
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find and print unique image filenames
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        if img_url:
            img_url = urljoin(url, img_url)  # Convert relative URLs to absolute
            img_filename = img_url.split('/')[-1]
            if re.search(r'\.(jpg|jpeg|png|gif|bmp|webp)$', img_filename, re.IGNORECASE):
                if img_filename not in visited_images:
                    if fullurl:
                        print(img_url)
                    else:
                        print(img_filename)
                    visited_images.add(img_filename)
    
    # Find and follow links on the same host
    for link in soup.find_all('a', href=True):
        next_url = urljoin(url, link['href'])
        parsed_next_url = urlparse(next_url)
        
        if parsed_next_url.scheme != "webcal" and parsed_next_url.netloc == base_host:  # Stay within the same host
            get_image_filenames(next_url, visited_urls, visited_images, level + 1, verbose, fullurl)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} <URL> [--verbose --fullurl]", file=sys.stderr)
        sys.exit(1)
    
    start_url = sys.argv[1]
    verbose_flag = "--verbose" in sys.argv
    fullurl_flag = "--fullurl" in sys.argv
    visited_urls = set()
    visited_images = set()
    get_image_filenames(start_url, visited_urls, visited_images, verbose=verbose_flag, fullurl=fullurl_flag)
