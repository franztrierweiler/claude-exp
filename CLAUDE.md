# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python CLI application that performs web searches via DuckDuckGo web scraping and displays results in ASCII format. When images are available in search results, they are converted and displayed as ASCII art. Search results are limited to 5 answers. No API keys required.

## Architecture

### Core Components

1. **CLI Interface**: Command-line argument parsing using argparse to accept search queries
2. **Web Scraper**: Scrapes DuckDuckGo search results using requests + BeautifulSoup
3. **HTML Parser**: Extracts titles, URLs, snippets, and images from DuckDuckGo's HTML structure
4. **Ad Filter**: Filters out advertisements to show only organic search results
5. **ASCII Formatter**: Converts text results to ASCII-formatted output
6. **Image-to-ASCII Converter**: Downloads and converts images from search results to ASCII art using ascii-magic
7. **Results Limiter**: Ensures only top 5 results are processed and displayed

### Key Technologies

- **Web Scraping**: Uses DuckDuckGo HTML version (more scraper-friendly than Google)
- **HTTP Library**: requests library with proper User-Agent headers
- **HTML Parsing**: BeautifulSoup for parsing and extracting search results
- **CLI Framework**: argparse (Python stdlib) for argument parsing
- **Image Processing**: PIL/Pillow for image handling + ascii-magic for ASCII art conversion
- **No API Keys**: Uses direct web scraping, no authentication required

### Module Structure

- **main.py**: CLI entry point, argument parsing, orchestrates search and display
- **search.py**: `GoogleSearcher` class (uses DuckDuckGo) handles web scraping, HTML parsing, ad filtering, image downloading
- **formatter.py**: `AsciiFormatter` class handles ASCII output formatting and image-to-ASCII conversion

## Common Commands

```bash
# Run the CLI tool
python main.py "search query"

# Run with specific number of results
python main.py -n 3 "search query"

# Install dependencies
pip install -r requirements.txt

# Run with virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run tests (when implemented)
python -m pytest
python -m pytest tests/test_specific.py  # Single test file

# Lint code (if using)
pylint *.py
flake8 *.py
```

## Development Notes

### Web Scraping Approach

- **DuckDuckGo HTML Version**: Uses html.duckduckgo.com which is designed for simpler scraping
- **POST Requests**: DuckDuckGo HTML uses POST requests with form data
- **User-Agent Required**: Proper User-Agent headers required for successful requests
- **HTML Structure**: Parses divs with class 'result' or 'results_links'
- **Ad Filtering**: Filters out URLs containing '/y.js?', 'ad_domain', or '/aclick?'
- **URL Extraction**: Handles DuckDuckGo redirect URLs and extracts actual target URLs
- **Image Enrichment**: Attempts to fetch images from DuckDuckGo Images results
- **Rate Limiting**: Be respectful with request frequency

### Error Handling

- Gracefully handle network errors, parsing failures, and image download failures
- Skip individual results that fail to parse rather than failing entire search
- Display text results even when images fail to download

### HTML Parsing Considerations

- DuckDuckGo's HTML structure is more stable than Google's
- Parser looks for elements with classes: 'result__a' (title), 'result__snippet' (description)
- Filters out advertisements, base64-encoded images, and logo images
- Skips results that don't have required fields (title, link)
- Handles both direct URLs and DuckDuckGo redirect URLs

### ASCII Art Display

- Image-to-ASCII conversion quality depends on terminal width and image resolution
- Uses `shutil.get_terminal_size()` to adapt to terminal dimensions
- ASCII art display may vary across different terminal emulators

## Dependencies

Current dependencies in requirements.txt:
- `requests>=2.31.0`: HTTP requests for web scraping and image downloads
- `beautifulsoup4>=4.12.0`: HTML parsing for extracting search results
- `Pillow>=10.0.0`: Image processing for ASCII art conversion
- `ascii-magic>=2.3.0`: Image-to-ASCII conversion

## Legal and Ethical Considerations

This tool uses DuckDuckGo web scraping, which should be done responsibly:
- DuckDuckGo is generally more permissive of scraping than other search engines
- Respect rate limits and avoid spamming requests
- Tool is intended for educational and personal use
- For high-volume production use, consider official search APIs
