# Search ASCII CLI

A Python command-line tool that performs web searches (via DuckDuckGo) and displays results in ASCII format. Images from search results are automatically converted to ASCII art.

## Features

- Perform web searches from the command line (no API key required!)
- Uses DuckDuckGo for reliable, ad-filtered search results
- Display up to 5 search results in ASCII format
- Automatic image-to-ASCII art conversion for images in search results
- Clean, terminal-friendly output
- Web scraping approach - no API keys or authentication needed

## Prerequisites

- Python 3.7 or higher

## Setup

### 1. Clone or download this repository

```bash
git clone <repository-url>
cd claude-exp
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

That's it! No API keys or additional configuration needed.

## Usage

### Basic search

```bash
python main.py "search query"
```

### Examples

```bash
# Search for Python tutorials
python main.py python tutorials

# Search with quotes
python main.py "machine learning"

# Specify number of results (max 5)
python main.py -n 3 "data science"
```

### Command-line options

```
positional arguments:
  query                 Search query (can be multiple words)

optional arguments:
  -h, --help            Show help message
  -n, --num-results N   Number of results to display (default: 5, max: 5)
```

## Output Format

The tool displays results in the following format:

```
================================================================================
GOOGLE SEARCH: your query
Results: 5
================================================================================

================================================================================
RESULT #1 (WITH IMAGE)
================================================================================

[ASCII art representation of the image]

Title: Result Title
URL:   https://example.com

Result description snippet...

================================================================================
RESULT #2
================================================================================

Title: Another Result
URL:   https://example2.com

Another description snippet...
```

## How It Works

The tool uses DuckDuckGo web scraping to:
1. Send a search request to DuckDuckGo HTML version
2. Parse the HTML response using BeautifulSoup
3. Filter out advertisements to show only organic results
4. Extract titles, URLs, snippets, and images from search results
5. Download images and convert them to ASCII art
6. Display everything in a clean ASCII format

## Limitations

- Some images may not be available or convertible to ASCII art
- Rate limiting: Be respectful and don't spam requests
- DuckDuckGo's HTML structure may change over time, requiring parser updates

## Troubleshooting

### "No results found or search failed"
- Check your internet connection
- DuckDuckGo may be temporarily rate-limiting requests
- Try waiting a moment before searching again

### Image download failures
- Some images may be blocked by CORS or authentication
- The tool will display text results even if images fail to download

### Parse errors
- DuckDuckGo's HTML structure may have changed
- The tool will attempt to extract as much information as possible

## Project Structure

```
.
├── main.py           # CLI entry point
├── search.py         # DuckDuckGo web scraping implementation
├── formatter.py      # ASCII formatting and image conversion
├── requirements.txt  # Python dependencies
├── .gitignore        # Git ignore patterns
└── README.md         # This file
```

## Legal Notice

This tool is for educational purposes. Web scraping should be done responsibly and respectfully. DuckDuckGo is generally more permissive of scraping than other search engines, but always be mindful of rate limiting.

## License

This project is provided as-is for educational purposes.
