"""ASCII formatting and image conversion module for web display."""
import io
from typing import Dict, Optional
from PIL import Image
from ascii_magic import AsciiArt


class AsciiFormatter:
    """Handles formatting of search results and images to ASCII for web display."""

    def __init__(self, width: int = 80):
        """
        Initialize the formatter.

        Args:
            width: Terminal width in characters for ASCII art
        """
        self.width = width

    def image_to_ascii(self, image_data: bytes, width: int = 60) -> Optional[str]:
        """
        Convert image bytes to ASCII art string.

        Args:
            image_data: Raw image bytes
            width: Width of ASCII art in characters

        Returns:
            ASCII art string or None if conversion fails
        """
        try:
            # Open image from bytes
            image = Image.open(io.BytesIO(image_data))

            # Convert to ASCII using ascii-magic
            ascii_art = AsciiArt.from_pillow_image(image)

            # Convert to string instead of printing to terminal
            # We'll capture the ASCII output as a string
            ascii_str = ascii_art.to_ascii(columns=min(width, self.width))

            return ascii_str

        except Exception as e:
            return None

    def format_result_for_web(self, result: Dict, index: int, image_ascii: Optional[str] = None) -> Dict:
        """
        Format a search result for web display.

        Args:
            result: Dictionary containing title, link, snippet, and image
            index: Result number (1-5)
            image_ascii: Optional ASCII art string for the image

        Returns:
            Dictionary with formatted result data
        """
        return {
            'index': index,
            'title': result['title'],
            'link': result['link'],
            'snippet': result['snippet'],
            'image_url': result.get('image'),
            'ascii_art': image_ascii
        }
