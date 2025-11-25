"""ASCII formatting and image conversion module."""
import io
import shutil
from typing import Dict, Optional
from PIL import Image
from ascii_magic import AsciiArt


class AsciiFormatter:
    """Handles formatting of search results and images to ASCII."""

    def __init__(self):
        """Initialize the formatter."""
        self.terminal_width = shutil.get_terminal_size().columns

    def format_result(self, result: Dict, index: int) -> str:
        """
        Format a single search result as ASCII text.

        Args:
            result: Dictionary containing title, link, snippet, and image
            index: Result number (1-5)

        Returns:
            Formatted ASCII string
        """
        separator = "=" * min(self.terminal_width, 80)
        output = []

        output.append(f"\n{separator}")
        output.append(f"RESULT #{index}")
        output.append(separator)
        output.append(f"\nTitle: {result['title']}")
        output.append(f"URL:   {result['link']}")
        output.append(f"\n{result['snippet']}\n")

        return "\n".join(output)

    def image_to_ascii(self, image_data: bytes, width: int = 80) -> Optional[str]:
        """
        Convert image bytes to ASCII art.

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
            # Create a temporary file-like object
            ascii_art = AsciiArt.from_pillow_image(image)
            ascii_art.to_terminal(columns=min(width, self.terminal_width - 4))

            return "ASCII art displayed above"

        except Exception as e:
            return f"[Could not convert image to ASCII: {e}]"

    def format_image_result(self, result: Dict, index: int, image_data: bytes) -> str:
        """
        Format a search result with an image as ASCII.

        Args:
            result: Dictionary containing title, link, snippet, and image
            index: Result number (1-5)
            image_data: Raw image bytes

        Returns:
            Formatted ASCII string with image
        """
        separator = "=" * min(self.terminal_width, 80)
        output = []

        output.append(f"\n{separator}")
        output.append(f"RESULT #{index} (WITH IMAGE)")
        output.append(separator)

        # Display ASCII art
        print("\n" + "\n".join(output))
        self.image_to_ascii(image_data, width=60)

        output = []
        output.append(f"\nTitle: {result['title']}")
        output.append(f"URL:   {result['link']}")
        output.append(f"\n{result['snippet']}\n")

        return "\n".join(output)

    def format_header(self, query: str, num_results: int) -> str:
        """
        Format the search header.

        Args:
            query: The search query
            num_results: Number of results

        Returns:
            Formatted header string
        """
        separator = "=" * min(self.terminal_width, 80)
        output = []

        output.append(f"\n{separator}")
        output.append(f"GOOGLE SEARCH: {query}")
        output.append(f"Results: {num_results}")
        output.append(separator)

        return "\n".join(output)

    def format_footer(self) -> str:
        """
        Format the search footer.

        Returns:
            Formatted footer string
        """
        separator = "=" * min(self.terminal_width, 80)
        return f"\n{separator}\nSearch complete.\n{separator}\n"
