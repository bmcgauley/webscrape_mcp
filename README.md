# Web Scraping MCP Server

A powerful, open-source web scraping Model Context Protocol (MCP) server that works just like Firecrawl—but without API keys! Built with Python and modern web scraping libraries.

## Features

- **🔍 Smart Scraping**: Extract content from any web page with automatic format detection
- **📄 Multiple Formats**: Get content as Markdown, HTML, plain text, or structured JSON
- **🕷️ Website Crawling**: Recursively crawl websites with depth and page limits
- **🔗 Link Extraction**: Fast discovery of all links on a page
- **⚡ JavaScript Support**: Render dynamic pages with Playwright
- **📸 Screenshots**: Capture full-page or viewport screenshots
- **🚀 Batch Processing**: Scrape multiple URLs concurrently
- **🎯 No API Keys**: Completely free and open-source

## Tools

### 1. `webscrape_scrape_url`
Scrape content from a single URL.

**Best for:**
- Extracting article content
- Converting web pages to markdown
- Getting page metadata
- Scraping static websites

**Parameters:**
- `url` (string, required): The web page URL to scrape
- `response_format` (enum, default: "markdown"): Output format (markdown, html, text, json)
- `include_links` (boolean, default: false): Extract all links from the page
- `include_images` (boolean, default: false): Extract image URLs
- `include_metadata` (boolean, default: true): Include page metadata

**Example:**
```python
{
  "url": "https://example.com/article",
  "response_format": "markdown",
  "include_links": true
}
```

### 2. `webscrape_scrape_multiple_urls`
Scrape multiple URLs concurrently (max 20).

**Best for:**
- Batch processing article URLs
- Scraping multiple pages from a sitemap
- Comparing content across pages

**Parameters:**
- `urls` (array, required): List of 1-20 URLs to scrape
- `response_format` (enum, default: "markdown"): Output format
- `include_metadata` (boolean, default: true): Include page metadata

**Example:**
```python
{
  "urls": [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
  ],
  "response_format": "json"
}
```

### 3. `webscrape_crawl_site`
Recursively crawl a website following links.

**Best for:**
- Discovering all pages in a section
- Scraping documentation sites
- Building sitemaps
- Content auditing

**Parameters:**
- `url` (string, required): Starting URL to crawl from
- `max_depth` (integer, default: 2): Maximum link depth (0-5)
- `max_pages` (integer, default: 20): Maximum pages to crawl (1-100)
- `same_domain_only` (boolean, default: true): Only crawl same domain
- `response_format` (enum, default: "markdown"): Output format

**Example:**
```python
{
  "url": "https://docs.example.com",
  "max_depth": 3,
  "max_pages": 50,
  "same_domain_only": true
}
```

### 4. `webscrape_extract_links`
Extract all links from a web page.

**Best for:**
- Site mapping
- Finding all subpages
- Link analysis
- Navigation discovery

**Parameters:**
- `url` (string, required): URL to extract links from
- `same_domain_only` (boolean, default: false): Only return links from same domain
- `include_anchors` (boolean, default: false): Include fragment links (#section)

**Example:**
```python
{
  "url": "https://example.com",
  "same_domain_only": true,
  "include_anchors": false
}
```

### 5. `webscrape_scrape_with_js`
Scrape JavaScript-rendered pages using Playwright.

**Best for:**
- Single Page Applications (React, Vue, Angular)
- Pages with lazy-loaded content
- JavaScript-heavy websites
- Dynamic dashboards

**Parameters:**
- `url` (string, required): URL to scrape with JS rendering
- `wait_for_selector` (string, optional): CSS selector to wait for
- `wait_seconds` (integer, default: 2): Additional wait time (0-30 seconds)
- `response_format` (enum, default: "markdown"): Output format

**Example:**
```python
{
  "url": "https://app.example.com/dashboard",
  "wait_for_selector": ".data-loaded",
  "wait_seconds": 3,
  "response_format": "markdown"
}
```

### 6. `webscrape_screenshot_url`
Capture a screenshot of a web page.

**Best for:**
- Visual documentation
- Page appearance verification
- Archiving page layouts
- Creating thumbnails

**Parameters:**
- `url` (string, required): URL to screenshot
- `full_page` (boolean, default: true): Capture full page or viewport
- `width` (integer, default: 1920): Viewport width in pixels (320-3840)
- `height` (integer, default: 1080): Viewport height in pixels (240-2160)

**Example:**
```python
{
  "url": "https://example.com",
  "full_page": true,
  "width": 1920,
  "height": 1080
}
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Step 1: Clone or Download

```bash
# Create a directory for your MCP server
mkdir webscrape-mcp
cd webscrape-mcp

# Copy the server file and requirements
```

### Step 2: Install Dependencies

#### Using pip:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Using uv:

```bash
# Install dependencies
uv pip install -r requirements.txt
```

### Step 3: Install Playwright (Optional but Recommended)

For JavaScript rendering and screenshot features:

```bash
# Install Playwright browsers
playwright install chromium
```

This installs the Chromium browser needed for the `webscrape_scrape_with_js` and `webscrape_screenshot_url` tools.

## Configuration

### Claude Desktop

Add to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "webscrape": {
      "command": "python",
      "args": ["/absolute/path/to/webscrape_mcp.py"]
    }
  }
}
```

Or with uv:

```json
{
  "mcpServers": {
    "webscrape": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/webscrape-mcp", "python", "webscrape_mcp.py"]
    }
  }
}
```

### Other MCP Clients

For other MCP-compatible clients (Cursor, VS Code, etc.), refer to their documentation for adding MCP servers via stdio transport.

## Usage Examples

### Example 1: Scrape a Blog Post

```
User: "Scrape this article and convert it to markdown: https://example.com/blog/post"

Claude uses: webscrape_scrape_url
{
  "url": "https://example.com/blog/post",
  "response_format": "markdown",
  "include_metadata": true
}

Returns: Clean markdown with title, content, and metadata
```

### Example 2: Find All Documentation Pages

```
User: "Find all pages in the docs section: https://docs.example.com"

Claude uses: webscrape_crawl_site
{
  "url": "https://docs.example.com",
  "max_depth": 2,
  "max_pages": 50,
  "same_domain_only": true
}

Returns: List of all discovered pages with their content
```

### Example 3: Scrape Dynamic Content

```
User: "Scrape this React app page: https://app.example.com/data"

Claude uses: webscrape_scrape_with_js
{
  "url": "https://app.example.com/data",
  "wait_for_selector": ".data-table",
  "wait_seconds": 3
}

Returns: Fully rendered page content after JavaScript execution
```

### Example 4: Extract All Links

```
User: "Get all internal links from this page: https://example.com"

Claude uses: webscrape_extract_links
{
  "url": "https://example.com",
  "same_domain_only": true,
  "include_anchors": false
}

Returns: JSON with categorized internal/external links
```

## Features in Detail

### Content Extraction

The server intelligently extracts content from web pages:

- **Markdown**: Clean, readable format perfect for LLMs
- **HTML**: Raw HTML for detailed analysis
- **Text**: Pure text without formatting
- **JSON**: Structured data with metadata

### Metadata Extraction

Automatically extracts:
- Page title
- Meta description
- Keywords
- Author information
- Open Graph data (og:title, og:description, etc.)

### Pagination Support

All list-based tools support pagination:
- Configurable page limits
- Offset-based pagination
- Total count reporting

### Error Handling

Robust error handling for:
- Network timeouts
- Invalid URLs
- HTTP errors (404, 403, 429, etc.)
- JavaScript rendering failures
- Content too large warnings

### Character Limits

Responses are limited to 25,000 characters to prevent overwhelming results. When content exceeds this limit:
- The server truncates gracefully
- Provides clear truncation notices
- Suggests ways to get more specific results

## Comparison with Firecrawl

| Feature | This Server | Firecrawl |
|---------|-------------|-----------|
| **Cost** | Free, open-source | Paid API (with free tier) |
| **API Keys** | None required | Required |
| **Single URL Scraping** | ✅ | ✅ |
| **Batch Scraping** | ✅ (20 URLs) | ✅ |
| **Website Crawling** | ✅ | ✅ |
| **Link Extraction** | ✅ | ✅ (Map feature) |
| **JavaScript Rendering** | ✅ (Playwright) | ✅ |
| **Screenshots** | ✅ | ✅ |
| **Multiple Formats** | ✅ | ✅ |
| **AI Extraction** | ❌ | ✅ |
| **Web Search** | ❌ | ✅ |
| **Rate Limiting** | None | Yes (plan-based) |

## Technical Details

### Built With

- **FastMCP**: Official MCP Python SDK
- **BeautifulSoup4**: HTML parsing
- **lxml**: Fast HTML/XML processing
- **html2text**: HTML to Markdown conversion
- **httpx**: Modern async HTTP client
- **Playwright**: Browser automation (optional)

### Architecture

The server follows MCP best practices:
- Async/await for all I/O operations
- Pydantic v2 models for input validation
- Comprehensive error handling
- Tool annotations for better UX
- Response format flexibility
- Character limit protection

## Troubleshooting

### "Module 'playwright' not found"

Install Playwright and browsers:
```bash
pip install playwright
playwright install chromium
```

### "Connection timeout" errors

- Increase the default timeout in the code
- Check your internet connection
- Some sites may block scrapers

### "Too many requests" / 429 errors

- Add delays between requests
- Some sites have rate limiting
- Consider using a proxy (modify the code)

### Responses are truncated

- Use more specific selectors
- Scrape specific sections instead of full pages
- Use JSON format which is more compact
- Reduce `max_pages` or `max_depth` for crawling

## Best Practices

1. **Respect robots.txt**: Check if scraping is allowed
2. **Rate limiting**: Don't overwhelm servers with requests
3. **Legal compliance**: Ensure you have the right to scrape content
4. **Start small**: Test with single pages before crawling
5. **Use specific selectors**: For JavaScript rendering, wait for specific elements

## Contributing

This server is open-source and contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## License

MIT License - feel free to use and modify as needed.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review MCP documentation at modelcontextprotocol.io

---

Built with ❤️ following MCP best practices
