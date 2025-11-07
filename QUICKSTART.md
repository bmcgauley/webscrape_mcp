# Quick Start Guide

Get your web scraping MCP server running in 5 minutes!

## Step 1: Install Python Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Using uv (faster)
uv pip install -r requirements.txt
```

## Step 2: Install Playwright (Optional but Recommended)

For JavaScript rendering and screenshots:

```bash
playwright install chromium
```

## Step 3: Test the Server

Test that the server runs correctly:

```bash
# Test basic import
python -c "import mcp; from bs4 import BeautifulSoup; print('✓ Dependencies OK')"

# The server itself runs via stdio and waits for MCP client connections
# You can verify it starts without errors (it will hang waiting for input):
timeout 2s python webscrape_mcp.py || echo "✓ Server starts OK"
```

## Step 4: Configure Claude Desktop

1. Find your Claude Desktop config file:
   - **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server configuration:

```json
{
  "mcpServers": {
    "webscrape": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/webscrape_mcp.py"]
    }
  }
}
```

**Important**: Replace `/ABSOLUTE/PATH/TO/` with the actual full path to your `webscrape_mcp.py` file!

3. Restart Claude Desktop

## Step 5: Test in Claude

Open Claude Desktop and try these commands:

### Test 1: Simple Scrape
```
Scrape this page: https://example.com
```

### Test 2: Extract Links
```
Find all links on https://example.com
```

### Test 3: Convert to Markdown
```
Scrape https://news.ycombinator.com and convert to markdown
```

## Troubleshooting

### Server not showing up in Claude?

1. Check the config file path is correct
2. Verify the path to `webscrape_mcp.py` is absolute (not relative)
3. Restart Claude Desktop completely
4. Check Claude Desktop logs for errors

### Playwright not working?

```bash
# Reinstall Playwright
pip install --force-reinstall playwright
playwright install chromium
```

### Import errors?

```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt
```

## Next Steps

- Read the full [README.md](README.md) for all features
- Check out [EXAMPLES.md](EXAMPLES.md) for usage examples
- Customize the server for your needs

## Quick Reference

All tool names start with `webscrape_`:

- `webscrape_scrape_url` - Scrape a single URL
- `webscrape_scrape_multiple_urls` - Batch scrape (up to 20 URLs)
- `webscrape_crawl_site` - Recursively crawl a website
- `webscrape_extract_links` - Extract all links from a page
- `webscrape_scrape_with_js` - Scrape JavaScript-rendered pages
- `webscrape_screenshot_url` - Capture page screenshots

Happy scraping! 🕷️
