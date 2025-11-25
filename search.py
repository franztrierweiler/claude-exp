"""Search functionality module using DuckDuckGo web scraping."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import urllib.parse
import time


class GoogleSearcher:
    """Handles search queries via DuckDuckGo web scraping (more reliable than Google)."""

    def __init__(self):
        """Initialize the searcher."""
        self.base_url = "https://html.duckduckgo.com/html/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'identity',  # Don't accept compression
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Perform a search and return results by scraping DuckDuckGo.

        Args:
            query: The search query string
            num_results: Number of results to return (max 10)

        Returns:
            List of search result dictionaries with title, link, snippet, and image
        """
        # DuckDuckGo HTML version uses POST requests
        data = {
            'q': query,
            'b': '',  # Start from beginning
            'kl': 'us-en',  # Region
        }

        try:
            response = self.session.post(
                self.base_url,
                data=data,
                timeout=15
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            # DuckDuckGo HTML results are in div.result or div.results_links
            search_results = soup.find_all('div', class_='result')

            if not search_results:
                # Try alternative selector
                search_results = soup.find_all('div', class_='results_links')

            for item in search_results[:num_results]:
                try:
                    result = self._parse_result(item)
                    if result:
                        results.append(result)
                except Exception:
                    continue

            # Try to enrich first few results with images
            if results:
                results = self._enrich_with_images(query, results)

            return results[:num_results]

        except requests.exceptions.RequestException as e:
            print(f"Error performing search: {e}")
            return []
        except Exception as e:
            print(f"Error parsing search results: {e}")
            return []

    def _parse_result(self, item) -> Optional[Dict]:
        """Parse a single search result item from DuckDuckGo."""
        # Find title - usually in a.result__a
        title_elem = item.find('a', class_='result__a')
        if not title_elem:
            # Try h2 > a
            h2 = item.find('h2')
            if h2:
                title_elem = h2.find('a')

        if not title_elem:
            return None

        title = title_elem.get_text().strip()
        link = title_elem.get('href', '')

        # DDG sometimes uses redirect URLs, extract actual URL
        if link.startswith('//duckduckgo.com/l/?'):
            try:
                # Extract uddg parameter
                parsed = urllib.parse.urlparse(link)
                params = urllib.parse.parse_qs(parsed.query)
                if 'uddg' in params:
                    link = urllib.parse.unquote(params['uddg'][0])
            except Exception:
                pass

        if not link or not link.startswith('http'):
            return None

        # Filter out ads (DuckDuckGo ads contain 'y.js' or 'ad_domain')
        if '/y.js?' in link or 'ad_domain' in link or '/aclick?' in link:
            return None

        # Find snippet/description - usually in a.result__snippet
        snippet = 'No description available'
        snippet_elem = item.find('a', class_='result__snippet')
        if snippet_elem:
            snippet = snippet_elem.get_text().strip()

        # Try to find an image
        image = None
        img_elem = item.find('img')
        if img_elem:
            src = img_elem.get('src') or img_elem.get('data-src')
            if src and src.startswith('http'):
                image = src

        return {
            'title': title,
            'link': link,
            'snippet': snippet,
            'image': image
        }

    def _enrich_with_images(self, query: str, results: List[Dict]) -> List[Dict]:
        """
        Try to get images for search results from DuckDuckGo Images.

        Args:
            query: The search query
            results: List of search results

        Returns:
            Updated results with images where possible
        """
        try:
            # DuckDuckGo Images search
            image_url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}&iax=images&ia=images"

            response = self.session.get(image_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find image elements
            images = []
            for img in soup.find_all('img')[:5]:
                src = img.get('src') or img.get('data-src')
                if src and src.startswith('http') and 'logo' not in src.lower():
                    images.append(src)
                    if len(images) >= 3:
                        break

            # Add images to results that don't have them
            image_idx = 0
            for result in results:
                if not result['image'] and image_idx < len(images):
                    result['image'] = images[image_idx]
                    image_idx += 1

        except Exception:
            pass

        return results

    def download_image(self, url: str) -> Optional[bytes]:
        """
        Download an image from a URL.

        Args:
            url: The image URL

        Returns:
            Image bytes or None if download fails
        """
        try:
            response = self.session.get(
                url,
                timeout=10,
                stream=True
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException:
            return None
