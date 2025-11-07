# Usage Examples

Practical examples for using the Web Scraping MCP Server.

## Basic Scraping

### Example 1: Scrape a Blog Post

**User Query:**
```
Scrape this blog post and summarize it: https://example.com/blog/2024/ai-trends
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com/blog/2024/ai-trends",
  "response_format": "markdown",
  "include_metadata": true
}
```

**Result:** Clean markdown with article content, perfect for summarization.

---

### Example 2: Extract Just Text

**User Query:**
```
Get the plain text content from https://example.com/article without any formatting
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com/article",
  "response_format": "text",
  "include_metadata": false
}
```

**Result:** Pure text content without HTML or markdown formatting.

---

### Example 3: Get Structured Data

**User Query:**
```
Scrape https://example.com/product and give me JSON with all the data
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com/product",
  "response_format": "json",
  "include_links": true,
  "include_images": true
}
```

**Result:** Structured JSON with content, links, images, and metadata.

---

## Batch Scraping

### Example 4: Compare Multiple Articles

**User Query:**
```
Compare the content of these three articles:
- https://site1.com/article1
- https://site2.com/article2  
- https://site3.com/article3
```

**Claude's Tool Call:**
```json
{
  "urls": [
    "https://site1.com/article1",
    "https://site2.com/article2",
    "https://site3.com/article3"
  ],
  "response_format": "markdown",
  "include_metadata": true
}
```

**Result:** All three articles scraped concurrently with metadata for comparison.

---

### Example 5: Scrape All Pages from a Sitemap

**User Query:**
```
I have these 10 URLs from a sitemap. Scrape them all and extract the main content.
[list of URLs]
```

**Claude's Tool Call:**
```json
{
  "urls": ["url1", "url2", "url3", "...10 URLs total..."],
  "response_format": "text"
}
```

**Result:** Fast parallel scraping of all 10 pages.

---

## Website Crawling

### Example 6: Discover All Documentation Pages

**User Query:**
```
Find all pages in the documentation section: https://docs.example.com/getting-started
```

**Claude's Tool Call:**
```json
{
  "url": "https://docs.example.com/getting-started",
  "max_depth": 2,
  "max_pages": 50,
  "same_domain_only": true,
  "response_format": "markdown"
}
```

**Result:** Crawls 2 levels deep, up to 50 pages, only from docs.example.com.

---

### Example 7: Build a Sitemap

**User Query:**
```
Build a sitemap of all pages under https://example.com/blog/
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com/blog/",
  "max_depth": 3,
  "max_pages": 100,
  "same_domain_only": true,
  "response_format": "json"
}
```

**Result:** JSON structure with all discovered URLs and their metadata.

---

### Example 8: Shallow Crawl

**User Query:**
```
Get just the direct subpages of https://example.com/products/
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com/products/",
  "max_depth": 1,
  "max_pages": 20,
  "same_domain_only": true
}
```

**Result:** Only pages directly linked from the starting URL (depth=1).

---

## Link Extraction

### Example 9: Find All Internal Links

**User Query:**
```
Show me all internal links on https://example.com
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com",
  "same_domain_only": true,
  "include_anchors": false
}
```

**Result:** List of all internal links, categorized and counted.

---

### Example 10: External Link Analysis

**User Query:**
```
What external sites does https://example.com link to?
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com",
  "same_domain_only": false,
  "include_anchors": false
}
```

**Result:** Separate lists of internal and external links.

---

### Example 11: Complete Link Map

**User Query:**
```
Get every single link on this page including anchors: https://example.com/guide
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com/guide",
  "same_domain_only": false,
  "include_anchors": true
}
```

**Result:** Complete list including fragment identifiers (#section).

---

## JavaScript Rendering

### Example 12: Scrape a React App

**User Query:**
```
Scrape content from this React app: https://app.example.com/dashboard
```

**Claude's Tool Call:**
```json
{
  "url": "https://app.example.com/dashboard",
  "wait_for_selector": ".dashboard-content",
  "wait_seconds": 3,
  "response_format": "markdown"
}
```

**Result:** Fully rendered content after JavaScript execution.

---

### Example 13: Wait for Dynamic Content

**User Query:**
```
This page loads data dynamically: https://example.com/data
Wait for the table to load before scraping.
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com/data",
  "wait_for_selector": "table.data-table",
  "wait_seconds": 5,
  "response_format": "text"
}
```

**Result:** Content scraped only after the table element appears.

---

### Example 14: Scrape SPA

**User Query:**
```
Extract content from this single-page app: https://vue-app.example.com
```

**Claude's Tool Call:**
```json
{
  "url": "https://vue-app.example.com",
  "wait_seconds": 4,
  "response_format": "markdown"
}
```

**Result:** Waits for Vue.js to render before capturing content.

---

## Screenshots

### Example 15: Full Page Screenshot

**User Query:**
```
Take a full-page screenshot of https://example.com
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com",
  "full_page": true,
  "width": 1920,
  "height": 1080
}
```

**Result:** Base64-encoded full-page PNG screenshot.

---

### Example 16: Mobile Screenshot

**User Query:**
```
How does https://example.com look on mobile?
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com",
  "full_page": true,
  "width": 375,
  "height": 812
}
```

**Result:** Screenshot at iPhone X dimensions (375x812).

---

### Example 17: Viewport Only Screenshot

**User Query:**
```
Screenshot just the visible part of https://example.com
```

**Claude's Tool Call:**
```json
{
  "url": "https://example.com",
  "full_page": false,
  "width": 1920,
  "height": 1080
}
```

**Result:** Screenshot of viewport only, not the entire scrollable page.

---

## Advanced Use Cases

### Example 18: Research Multiple Sources

**User Query:**
```
Research AI safety by scraping these sources and comparing their perspectives:
- https://site1.com/ai-safety
- https://site2.com/ai-alignment
- https://site3.com/ai-risks
```

**Claude would:**
1. Use `webscrape_scrape_multiple_urls` to get all three
2. Analyze and compare the content
3. Synthesize findings

---

### Example 19: Monitor Competitor Content

**User Query:**
```
Scrape our competitor's blog and list their latest posts: https://competitor.com/blog
```

**Claude would:**
1. Use `webscrape_scrape_url` to get the blog page
2. Use `webscrape_extract_links` to find post URLs
3. Use `webscrape_scrape_multiple_urls` to get post content

---

### Example 20: Documentation Index

**User Query:**
```
Create an index of all documentation at https://docs.example.com
```

**Claude would:**
1. Use `webscrape_crawl_site` with depth=3
2. Extract titles and first paragraphs
3. Build structured index with categories

---

## Error Handling Examples

### Example 21: Handling 404s

**User Query:**
```
Scrape https://example.com/nonexistent-page
```

**Result:**
```
Error scraping https://example.com/nonexistent-page: HTTP 404: https://example.com/nonexistent-page
```

---

### Example 22: Timeout Handling

**User Query:**
```
Scrape https://very-slow-site.com
```

**Result:**
```
Error scraping https://very-slow-site.com: Request timeout for: https://very-slow-site.com
```

---

## Tips and Tricks

### When to Use Each Tool

| Scenario | Tool | Why |
|----------|------|-----|
| Single article/page | `scrape_url` | Simplest, fastest |
| Known list of URLs | `scrape_multiple_urls` | Parallel processing |
| Explore website | `crawl_site` | Discovers pages |
| Find navigation | `extract_links` | Fast link discovery |
| Dynamic content | `scrape_with_js` | Renders JavaScript |
| Visual verification | `screenshot_url` | Captures appearance |

### Performance Tips

1. **Start Small**: Test with single pages before crawling
2. **Use Specific Depth**: Set `max_depth=1` for faster crawls
3. **Limit Pages**: Use `max_pages=20` to avoid overwhelming results
4. **Choose Format Wisely**: 
   - Use `text` for simple content
   - Use `json` for structured data
   - Use `markdown` for readability

### Common Patterns

```
# Pattern 1: Explore then Extract
1. extract_links to find URLs
2. scrape_multiple_urls to get content

# Pattern 2: Crawl and Analyze
1. crawl_site to discover pages
2. Filter relevant URLs
3. scrape_with_js if needed for dynamic content

# Pattern 3: Quick Research
1. scrape_multiple_urls for known sources
2. Compare and synthesize
```

## Need More Examples?

Check the README.md for detailed tool documentation and parameters.
