#!/usr/bin/env python3
"""
Script to refactor webscrape_mcp.py to implement progressive disclosure pattern.
"""

def refactor_webscrape_mcp():
    # Read the original file
    with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add imports after datetime import
    import_old = "from datetime import datetime"
    import_new = """from datetime import datetime, timedelta
import hashlib
import time"""
    content = content.replace(import_old, import_new)

    # 2. Add cache constants after DEFAULT_TIMEOUT
    constants_old = """DEFAULT_TIMEOUT = 30.0

# Response format enum"""
    constants_new = """DEFAULT_TIMEOUT = 30.0

# Cache constants for progressive disclosure
CACHE_TTL_SECONDS = 3600  # 1 hour TTL for cached scrapes
PREVIEW_LENGTH = 500  # Character limit for content previews

# Global cache for scrape results (resource-based pattern)
SCRAPE_CACHE: Dict[str, Dict[str, Any]] = {}

# Response format enum"""
    content = content.replace(constants_old, constants_new)

    # 3. Add cache management functions before Tool Implementations section
    cache_functions = '''

# ============================================================================
# Cache Management Functions (Progressive Disclosure Pattern)
# ============================================================================

def _generate_scrape_id(url: str, format_or_suffix: str) -> str:
    """
    Generate a unique ID for a scrape operation.

    Args:
        url: The URL being scraped
        format_or_suffix: Format type or additional suffix for uniqueness

    Returns:
        MD5 hash string as scrape ID
    """
    unique_string = f"{url}_{format_or_suffix}_{int(time.time())}"
    return hashlib.md5(unique_string.encode()).hexdigest()


def _clean_expired_cache():
    """Remove expired entries from the scrape cache."""
    current_time = datetime.utcnow()
    expired_ids = []

    for scrape_id, entry in SCRAPE_CACHE.items():
        if current_time > entry.get("expires_at", current_time):
            expired_ids.append(scrape_id)

    for scrape_id in expired_ids:
        del SCRAPE_CACHE[scrape_id]


def _store_in_cache(
    scrape_id: str,
    url: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    links: Optional[List[str]] = None,
    images: Optional[List[str]] = None
):
    """
    Store scrape results in cache for resource-based access.

    Args:
        scrape_id: Unique identifier for this scrape
        url: Original URL
        content: Full scraped content
        metadata: Optional page metadata
        links: Optional list of links
        images: Optional list of images
    """
    # Clean expired entries first
    _clean_expired_cache()

    # Store the scrape result
    SCRAPE_CACHE[scrape_id] = {
        "url": url,
        "content": content,
        "metadata": metadata or {},
        "links": links or [],
        "images": images or [],
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(seconds=CACHE_TTL_SECONDS)
    }


'''

    # Insert cache functions before "# ========... Tool Implementations"
    tool_implementations_marker = "# ============================================================================\n# Tool Implementations\n# ============================================================================"
    content = content.replace(
        tool_implementations_marker,
        cache_functions + tool_implementations_marker
    )

    # 4. Add discovery tools before the first @mcp.tool
    discovery_tools = '''

# ============================================================================
# Discovery Tools (Progressive Disclosure)
# ============================================================================

@mcp.tool(
    name="webscrape_list_tools",
    annotations={
        "title": "List WebScrape Tools",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True
    }
)
async def list_tools(
    detail_level: Literal["minimal", "brief", "full"] = "minimal",
    category: Optional[str] = None
) -> str:
    """
    List available web scraping tools with configurable detail level.

    Enables progressive disclosure - agents can discover tools without loading
    all schemas into context upfront.

    Args:
        detail_level: Amount of detail to return
            - "minimal": Just tool names (smallest token usage)
            - "brief": Names and descriptions
            - "full": Complete schemas with all parameters
        category: Optional filter by category ("scraping", "extraction", "rendering")

    Returns:
        JSON string with tool information based on detail level
    """
    tools = {
        "webscrape_scrape_url": {
            "name": "webscrape_scrape_url",
            "description": "Scrape content from a single URL",
            "category": "scraping",
            "best_for": ["Extracting article content", "Getting page information", "Converting web pages to markdown"]
        },
        "webscrape_scrape_multiple_urls": {
            "name": "webscrape_scrape_multiple_urls",
            "description": "Scrape multiple URLs concurrently (batch operation)",
            "category": "scraping",
            "best_for": ["Scraping multiple pages from a sitemap", "Batch processing article URLs", "Comparing content across pages"]
        },
        "webscrape_crawl_site": {
            "name": "webscrape_crawl_site",
            "description": "Recursively crawl a website following links",
            "category": "scraping",
            "best_for": ["Discovering all pages in a section", "Scraping documentation sites", "Building sitemaps"]
        },
        "webscrape_extract_links": {
            "name": "webscrape_extract_links",
            "description": "Extract all links from a web page",
            "category": "extraction",
            "best_for": ["Site mapping", "Finding all subpages", "Link analysis"]
        },
        "webscrape_scrape_with_js": {
            "name": "webscrape_scrape_with_js",
            "description": "Scrape JavaScript-rendered pages using headless browser",
            "category": "rendering",
            "best_for": ["Single Page Applications", "Pages with lazy-loaded content", "JavaScript-heavy websites"]
        },
        "webscrape_screenshot_url": {
            "name": "webscrape_screenshot_url",
            "description": "Capture a screenshot of a web page",
            "category": "rendering",
            "best_for": ["Visual documentation", "Page appearance verification", "Creating thumbnails"]
        }
    }

    # Filter by category if requested
    if category:
        tools = {k: v for k, v in tools.items() if v.get("category") == category}

    # Return based on detail level
    if detail_level == "minimal":
        return json.dumps(list(tools.keys()), indent=2)
    elif detail_level == "brief":
        brief_tools = [
            {
                "name": v["name"],
                "description": v["description"],
                "category": v["category"]
            }
            for v in tools.values()
        ]
        return json.dumps(brief_tools, indent=2)
    else:  # full
        return json.dumps(tools, indent=2)


@mcp.tool(
    name="webscrape_search_tools",
    annotations={
        "title": "Search WebScrape Tools",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True
    }
)
async def search_tools(
    query: str,
    category: Optional[str] = None
) -> str:
    """
    Search for web scraping tools by keyword or category.

    Args:
        query: Search term (e.g., "javascript", "crawl", "links", "batch")
        category: Optional category filter ("scraping", "extraction", "rendering")

    Returns:
        JSON array of matching tools with their descriptions
    """
    tools = {
        "webscrape_scrape_url": {
            "name": "webscrape_scrape_url",
            "description": "Scrape content from a single URL",
            "category": "scraping",
            "keywords": ["scrape", "url", "single", "page", "content", "markdown", "html"]
        },
        "webscrape_scrape_multiple_urls": {
            "name": "webscrape_scrape_multiple_urls",
            "description": "Scrape multiple URLs concurrently (batch operation)",
            "category": "scraping",
            "keywords": ["scrape", "multiple", "batch", "concurrent", "urls", "bulk"]
        },
        "webscrape_crawl_site": {
            "name": "webscrape_crawl_site",
            "description": "Recursively crawl a website following links",
            "category": "scraping",
            "keywords": ["crawl", "recursive", "follow", "links", "site", "depth", "sitemap"]
        },
        "webscrape_extract_links": {
            "name": "webscrape_extract_links",
            "description": "Extract all links from a web page",
            "category": "extraction",
            "keywords": ["extract", "links", "urls", "hrefs", "navigation", "mapping"]
        },
        "webscrape_scrape_with_js": {
            "name": "webscrape_scrape_with_js",
            "description": "Scrape JavaScript-rendered pages using headless browser",
            "category": "rendering",
            "keywords": ["javascript", "js", "render", "spa", "react", "vue", "angular", "dynamic", "playwright"]
        },
        "webscrape_screenshot_url": {
            "name": "webscrape_screenshot_url",
            "description": "Capture a screenshot of a web page",
            "category": "rendering",
            "keywords": ["screenshot", "capture", "image", "visual", "png", "thumbnail"]
        }
    }

    query_lower = query.lower()
    matching_tools = []

    for tool_id, tool_info in tools.items():
        # Check if query matches name, description, or keywords
        if (query_lower in tool_info["name"].lower() or
            query_lower in tool_info["description"].lower() or
            any(query_lower in keyword for keyword in tool_info.get("keywords", []))):

            # Apply category filter if specified
            if category is None or tool_info.get("category") == category:
                matching_tools.append({
                    "name": tool_info["name"],
                    "description": tool_info["description"],
                    "category": tool_info["category"]
                })

    return json.dumps(matching_tools, indent=2)


# ============================================================================
# Resource Access Endpoints (Progressive Disclosure)
# ============================================================================

@mcp.resource("scrape://{scrape_id}/content")
async def get_scrape_content(scrape_id: str) -> str:
    """
    Retrieve full scraped content by ID.

    This resource endpoint enables the progressive disclosure pattern - tools return
    resource URIs instead of full content, then agents can fetch the content only
    when needed.

    Args:
        scrape_id: Unique identifier from a scrape operation

    Returns:
        Full scraped content

    Raises:
        Exception: If scrape ID not found or expired
    """
    # Clean expired cache entries
    _clean_expired_cache()

    if scrape_id not in SCRAPE_CACHE:
        raise Exception(
            f"Scrape ID '{scrape_id}' not found in cache. "
            f"It may have expired (TTL: {CACHE_TTL_SECONDS}s) or never existed. "
            f"Please perform the scrape operation again."
        )

    entry = SCRAPE_CACHE[scrape_id]

    # Check if expired
    if datetime.utcnow() > entry["expires_at"]:
        del SCRAPE_CACHE[scrape_id]
        raise Exception(
            f"Scrape ID '{scrape_id}' has expired. "
            f"Cache TTL is {CACHE_TTL_SECONDS} seconds. "
            f"Please scrape the URL again."
        )

    return entry["content"]


@mcp.resource("scrape://{scrape_id}/metadata")
async def get_scrape_metadata(scrape_id: str) -> str:
    """
    Retrieve metadata for a scrape without the full content.

    Useful for getting information about a scrape (URL, links, images, stats)
    without loading the entire content payload.

    Args:
        scrape_id: Unique identifier from a scrape operation

    Returns:
        JSON string with metadata

    Raises:
        Exception: If scrape ID not found or expired
    """
    # Clean expired cache entries
    _clean_expired_cache()

    if scrape_id not in SCRAPE_CACHE:
        raise Exception(f"Scrape ID '{scrape_id}' not found in cache")

    entry = SCRAPE_CACHE[scrape_id]

    # Check if expired
    if datetime.utcnow() > entry["expires_at"]:
        del SCRAPE_CACHE[scrape_id]
        raise Exception(f"Scrape ID '{scrape_id}' has expired")

    metadata_response = {
        "scrape_id": scrape_id,
        "url": entry["url"],
        "metadata": entry["metadata"],
        "links": entry["links"],
        "images": entry["images"],
        "link_count": len(entry["links"]),
        "image_count": len(entry["images"]),
        "content_length": len(entry["content"]),
        "created_at": entry["created_at"].isoformat() + "Z",
        "expires_at": entry["expires_at"].isoformat() + "Z"
    }

    return json.dumps(metadata_response, indent=2)


'''

    # Insert discovery tools right before the first tool implementation
    first_tool_marker = '@mcp.tool(\n    name="webscrape_scrape_url",'
    content = content.replace(
        first_tool_marker,
        discovery_tools + first_tool_marker
    )

    # Write the modified content
    with open('webscrape_mcp.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] Step 1 complete: Added cache infrastructure, discovery tools, and resource endpoints")

if __name__ == "__main__":
    refactor_webscrape_mcp()
