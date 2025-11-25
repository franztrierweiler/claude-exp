# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Flask web application that performs web searches via DuckDuckGo web scraping and displays results with ASCII art in a retro terminal-style interface. Search results are limited to 5 answers. Images from search results are converted and displayed as ASCII art. No API keys required. Designed for deployment on Azure App Service.

## Architecture

### Core Components

1. **Flask Web Application**: Python web framework serving the application
2. **Web Interface**: HTML/CSS/JavaScript frontend with retro terminal theme
3. **Search API**: RESTful endpoint for handling search requests
4. **Web Scraper**: Scrapes DuckDuckGo search results using requests + BeautifulSoup
5. **HTML Parser**: Extracts titles, URLs, snippets, and images from DuckDuckGo's HTML structure
6. **Ad Filter**: Filters out advertisements to show only organic search results
7. **ASCII Formatter**: Converts images from search results to ASCII art using ascii-magic
8. **Results Limiter**: Ensures only top 5 results are processed and displayed

### Key Technologies

- **Web Framework**: Flask 3.0+ (Python web framework)
- **Production Server**: Gunicorn (WSGI server for Azure deployment)
- **Web Scraping**: DuckDuckGo HTML version (more scraper-friendly than Google)
- **HTTP Library**: requests library with proper User-Agent headers
- **HTML Parsing**: BeautifulSoup for parsing and extracting search results
- **Frontend**: Vanilla HTML/CSS/JavaScript with AJAX for search requests
- **Image Processing**: PIL/Pillow for image handling + ascii-magic for ASCII art conversion
- **Deployment Target**: Azure App Service (Linux, Python runtime)
- **No API Keys**: Uses direct web scraping, no authentication required

### Module Structure

```
project-root/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── routes.py             # Web routes and API endpoints
│   ├── search.py             # SearchEngine class (web scraping)
│   ├── formatter.py          # AsciiFormatter class (ASCII conversion)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Retro terminal-style CSS
│   │   ├── js/
│   │   │   └── main.js       # Frontend JavaScript
│   │   └── images/
│   └── templates/
│       ├── base.html         # Base template
│       └── index.html        # Search page
├── app.py                    # Flask entry point for Azure
├── requirements.txt          # Python dependencies
├── CLAUDE.md                 # Project documentation (this file)
├── DEPLOYMENT.md             # Azure deployment guide
├── .gitignore               # Git ignore patterns
└── README.md                # Project readme
```

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server locally
python app.py

# Run with Flask CLI
flask run

# Run with Gunicorn (production-like)
gunicorn --bind=0.0.0.0:5000 --timeout 600 app:app

# Run with virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Test the application
# Open browser: http://localhost:5000

# Deploy to Azure (see DEPLOYMENT.md for full guide)
git push azure main
```

## API Endpoints

### GET /
- Homepage with search interface
- Returns: HTML page with search form

### POST /search
- Performs web search and returns results as JSON
- Content-Type: application/json
- Request body:
  ```json
  {
    "query": "search query",
    "num_results": 5
  }
  ```
- Response:
  ```json
  {
    "success": true,
    "query": "search query",
    "results": [
      {
        "index": 1,
        "title": "Result title",
        "link": "https://example.com",
        "snippet": "Description...",
        "image_url": "https://...",
        "ascii_art": "ASCII representation..."
      }
    ]
  }
  ```

### GET /health
- Health check endpoint for Azure App Service monitoring
- Returns: `{"status": "healthy", "service": "web-search-app"}`

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

- API returns proper HTTP status codes (400 for bad requests, 500 for server errors)
- Gracefully handles network errors, parsing failures, and image download failures
- Skip individual results that fail to parse rather than failing entire search
- Display text results even when images fail to download or convert to ASCII
- Frontend JavaScript handles errors and displays user-friendly messages

### HTML Parsing Considerations

- DuckDuckGo's HTML structure is more stable than Google's
- Parser looks for elements with classes: 'result__a' (title), 'result__snippet' (description)
- Filters out advertisements, base64-encoded images, and logo images
- Skips results that don't have required fields (title, link)
- Handles both direct URLs and DuckDuckGo redirect URLs

### ASCII Art Display

- Image-to-ASCII conversion uses ascii-magic library
- ASCII art rendered in `<pre>` tags with monospace font
- Terminal-style green-on-black theme for retro aesthetic
- ASCII art quality depends on terminal width (set to 60 chars default)
- Properly escaped for HTML display to prevent rendering issues

### Frontend Architecture

- **Vanilla JavaScript**: No frameworks, simple and lightweight
- **AJAX Requests**: Fetch API for asynchronous search requests
- **Progressive Enhancement**: Search form works with JavaScript
- **Responsive Design**: Mobile-friendly layout with CSS media queries
- **Loading States**: Shows loading spinner during search
- **Error Handling**: User-friendly error messages displayed in UI

### Azure App Service Configuration

- **Runtime**: Python 3.11 on Linux
- **Startup Command**: `gunicorn --bind=0.0.0.0 --timeout 600 app:app`
- **Timeout**: 600 seconds (10 minutes) to account for slow web scraping
- **Port**: Automatically assigned by Azure (via PORT environment variable)
- **Always On**: Recommended for production to prevent cold starts
- **Logging**: Application logging enabled for troubleshooting

## Dependencies

Current dependencies in requirements.txt:
- `Flask>=3.0.0`: Web framework for Python
- `requests>=2.31.0`: HTTP requests for web scraping and image downloads
- `beautifulsoup4>=4.12.0`: HTML parsing for extracting search results
- `Pillow>=10.0.0`: Image processing for ASCII art conversion
- `ascii-magic>=2.3.0`: Image-to-ASCII conversion
- `gunicorn>=21.2.0`: Production WSGI server for Azure deployment

## Legal and Ethical Considerations

This tool uses DuckDuckGo web scraping, which should be done responsibly:
- DuckDuckGo is generally more permissive of scraping than other search engines
- Respect rate limits and avoid spamming requests
- Tool is intended for educational and personal use
- For high-volume production use, consider official search APIs
- Images are dynamically downloaded and converted; respect copyright and fair use

## Azure Deployment

This application is designed to be deployed on Azure App Service. Key considerations:

### Deployment Steps Summary
1. Install and configure Azure CLI
2. Create Azure resources (Resource Group, App Service Plan, Web App)
3. Configure startup command for Gunicorn
4. Deploy via Git, GitHub, or ZIP
5. Monitor logs and verify functionality

### Resource Requirements
- **Free Tier (F1)**: Suitable for testing, 60 min CPU/day limit
- **Basic Tier (B1)**: Recommended minimum for production ($~13/month)
- **Standard Tier (S1+)**: For auto-scaling and high traffic

### Environment Variables
- `FLASK_ENV`: Set to 'production' for deployment
- `SECRET_KEY`: Set a secure random key for production
- `PORT`: Automatically set by Azure (don't override)

### Monitoring
- Use Azure Application Insights for performance monitoring
- Enable application logging for debugging
- Check `/health` endpoint for service status
- Use Kudu console for file access and diagnostics

For detailed deployment instructions, see **DEPLOYMENT.md**.

## Testing Locally

Before deploying to Azure, test the application locally:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Test in browser
# Navigate to: http://localhost:5000
# Enter a search query and verify:
# - Search results appear
# - Images convert to ASCII art
# - Links open correctly
# - No JavaScript errors in console
```

## Troubleshooting

### Application won't start
- Check that all dependencies are installed: `pip list`
- Verify Python version: `python --version` (3.9+ required)
- Check for syntax errors: `python -m py_compile app.py`

### Search returns no results
- DuckDuckGo may be blocking requests; check User-Agent headers
- Verify internet connectivity
- Check HTML structure hasn't changed (DuckDuckGo may update layout)

### ASCII art not displaying
- Verify images are downloading successfully (check logs)
- Ensure ascii-magic and Pillow are installed correctly
- Check that images are not too large (5MB limit in code)

### Deployment issues
- Verify startup command is correct in Azure App Service configuration
- Check deployment logs in Kudu console
- Ensure all files are committed and pushed to Git repository
- Verify requirements.txt is in root directory
