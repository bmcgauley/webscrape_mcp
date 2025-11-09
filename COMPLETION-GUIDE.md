# WebScrape MCP Refactoring - Completion Guide

**Quick Reference for Finishing the Refactoring**

## Current State

✅ **Infrastructure Complete** (70%):
- Cache management system
- Discovery endpoints
- Resource access endpoints
- TypeScript definitions

⚠️ **Tool Integration Needed** (30%):
- Update tool return patterns to use cache + resource URIs

## Step-by-Step Completion

### Step 1: Update scrape_url Function (30 minutes)

**Location**: `webscrape_mcp.py`, line ~880

**Find this code**:
```python
        else:  # HTML
            content = html_content

        # Truncate if necessary
        content, was_truncated = _truncate_response(content, params.response_format.value)

        if was_truncated:
            content += "\n\n⚠️ Response truncated..."

        return content

    except Exception as e:
        return f"Error scraping {params.url}: {str(e)}"
```

**Replace with**:
```python
        else:  # HTML
            full_content = html_content

        # Generate unique scrape ID
        scrape_id = _generate_scrape_id(params.url, params.response_format.value)

        # Store in cache
        _store_in_cache(
            scrape_id=scrape_id,
            url=params.url,
            content=full_content,
            metadata=metadata or {},
            links=links,
            images=images
        )

        # Create preview
        preview = full_content[:PREVIEW_LENGTH]
        if len(full_content) > PREVIEW_LENGTH:
            preview += "..."

        # Return resource reference (NOT full content)
        response = {
            "success": True,
            "scrape_id": scrape_id,
            "url": params.url,
            "resource_uri": f"scrape://{scrape_id}/content",
            "metadata_uri": f"scrape://{scrape_id}/metadata",
            "preview": preview,
            "content_length": len(full_content),
            "format": params.response_format.value,
            "status_code": status_code,
            "scraped_at": datetime.utcnow().isoformat() + "Z",
            "expires_at": (datetime.utcnow() + timedelta(seconds=CACHE_TTL_SECONDS)).isoformat() + "Z",
            "stats": {
                "total_links": len(links) if links else 0,
                "total_images": len(images) if images else 0,
                "has_metadata": bool(metadata)
            }
        }

        return json.dumps(response, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "url": params.url
        }, indent=2)
```

**Also change**: In the formatting sections (JSON, MARKDOWN, TEXT), change `content =` to `full_content =`:
```python
# Line ~842
full_content = json.dumps(result, indent=2)  # was: content =

# Line ~873
full_content = "".join(result_parts)  # was: content =

# Line ~876
full_content = _html_to_text(soup)  # was: content =
```

### Step 2: Update scrape_multiple_urls (30 minutes)

**Location**: `webscrape_mcp.py`, line ~955

**Current code returns**:
```python
output["results"].append({
    "url": url,
    "success": True,
    "content": result  # Full content!
})
```

**Change to**:
```python
# result is already a JSON string from scrape_url with resource URIs
result_data = json.loads(result)
output["results"].append(result_data)
```

### Step 3: Update crawl_site (30 minutes)

**Location**: `webscrape_mcp.py`, line ~1039

**Find**:
```python
results.append({
    "url": current_url,
    "depth": depth,
    "title": metadata.get("title"),
    "status_code": status_code,
    "content": content[:5000]  # Truncated content
})
```

**Replace with**:
```python
# Generate scrape ID and store
scrape_id = _generate_scrape_id(current_url, f"crawl_depth{depth}")
_store_in_cache(
    scrape_id=scrape_id,
    url=current_url,
    content=content,
    metadata=metadata
)

# Store result with resource reference
results.append({
    "url": current_url,
    "depth": depth,
    "scrape_id": scrape_id,
    "resource_uri": f"scrape://{scrape_id}/content",
    "title": metadata.get("title"),
    "status_code": status_code,
    "content_length": len(content),
    "preview": content[:200] + "..." if len(content) > 200 else content
})
```

### Step 4: Update scrape_with_js (30 minutes)

**Location**: `webscrape_mcp.py`, line ~1244

**Similar pattern** - After formatting content, before return:

```python
# Generate scrape ID and store
scrape_id = _generate_scrape_id(params.url, f"js_{params.response_format.value}")
_store_in_cache(
    scrape_id=scrape_id,
    url=params.url,
    content=full_content,
    metadata=metadata
)

# Create preview
preview = full_content[:PREVIEW_LENGTH]
if len(full_content) > PREVIEW_LENGTH:
    preview += "..."

# Return resource reference
response = {
    "success": True,
    "scrape_id": scrape_id,
    "url": params.url,
    "resource_uri": f"scrape://{scrape_id}/content",
    "metadata_uri": f"scrape://{scrape_id}/metadata",
    "preview": preview,
    "content_length": len(full_content),
    "format": params.response_format.value,
    "rendering_method": "javascript",
    "scraped_at": datetime.utcnow().isoformat() + "Z",
    "expires_at": (datetime.utcnow() + timedelta(seconds=CACHE_TTL_SECONDS)).isoformat() + "Z"
}

return json.dumps(response, indent=2)
```

### Step 5: Update screenshot_url (30 minutes)

**Location**: `webscrape_mcp.py`, line ~1339

**Current** - Returns full base64 image:
```python
result = {
    "url": params.url,
    "title": title,
    ...
    "image_data": f"data:image/png;base64,{screenshot_b64}"  # Huge!
}
```

**Change to**:
```python
# Store screenshot in cache
scrape_id = _generate_scrape_id(params.url, "screenshot")
screenshot_data = f"data:image/png;base64,{screenshot_b64}"

_store_in_cache(
    scrape_id=scrape_id,
    url=params.url,
    content=screenshot_data,
    metadata={"title": title, "type": "screenshot"}
)

# Return resource reference (not full image data)
result = {
    "success": True,
    "scrape_id": scrape_id,
    "url": params.url,
    "title": title,
    "resource_uri": f"scrape://{scrape_id}/content",
    "viewport": {
        "width": params.width,
        "height": params.height
    },
    "full_page": params.full_page,
    "screenshot_size_bytes": len(screenshot_bytes),
    "captured_at": datetime.utcnow().isoformat() + "Z",
    "expires_at": (datetime.utcnow() + timedelta(seconds=CACHE_TTL_SECONDS)).isoformat() + "Z",
    "note": "Use resource_uri to retrieve full image data"
}
```

## Testing Checklist

After each modification:

```bash
# 1. Syntax check
python -m py_compile webscrape_mcp.py

# 2. Import test
python -c "import webscrape_mcp; print('Import successful')"

# 3. Run server (test startup)
python webscrape_mcp.py &
# Kill after confirming it starts

# 4. Full test (optional - requires running MCP inspector)
# Test discovery:
#   - list_tools(detail_level="minimal")
#   - search_tools(query="crawl")
# Test scraping:
#   - scrape_url(url="https://example.com")
#   - Check response has resource_uri
#   - Access resource via URI
```

## Validation Script

```python
#!/usr/bin/env python3
"""Validate refactoring is complete"""

with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
    code = f.read()

checks = {
    "SCRAPE_CACHE": 'SCRAPE_CACHE' in code,
    "list_tools": 'webscrape_list_tools' in code,
    "search_tools": 'webscrape_search_tools' in code,
    "resource_content": '@mcp.resource("scrape://{scrape_id}/content")' in code,
    "resource_metadata": '@mcp.resource("scrape://{scrape_id}/metadata")' in code,
    "scrape_url_resource": 'resource_uri' in code and '"scrape_id":' in code,
}

print("Validation Results:")
for name, passed in checks.items():
    status = "✓" if passed else "✗"
    print(f"{status} {name}")

if all(checks.values()):
    print("\n✓ ALL CHECKS PASSED - Refactoring complete!")
else:
    print("\n✗ Some checks failed - Continue working")
```

## Common Issues & Solutions

### Issue: NameError: name 'full_content' is not defined
**Solution**: Change all `content =` to `full_content =` in formatting sections

### Issue: Module import errors
**Solution**: Ensure all new imports are at top of file:
```python
from datetime import datetime, timedelta
import hashlib
import time
```

### Issue: Resource not found errors
**Solution**: Check cache is being populated:
```python
# Add debug print after _store_in_cache call
print(f"Stored in cache: {scrape_id}, size: {len(SCRAPE_CACHE)}")
```

## Quick Test Commands

```bash
# Validate syntax
python -m py_compile webscrape_mcp.py && echo "✓ Syntax OK"

# Count tools and resources
grep -c "@mcp.tool" webscrape_mcp.py  # Should be 8
grep -c "@mcp.resource" webscrape_mcp.py  # Should be 2

# Check for resource_uri in returns
grep -c "resource_uri" webscrape_mcp.py  # Should be 5+

# File size (should be ~48-50KB with all changes)
ls -lh webscrape_mcp.py
```

## Estimated Time

| Task | Time |
|------|------|
| scrape_url | 30 min |
| scrape_multiple_urls | 30 min |
| crawl_site | 30 min |
| scrape_with_js | 30 min |
| screenshot_url | 30 min |
| Testing | 1 hour |
| **Total** | **3.5 hours** |

## Success Criteria

- ✅ All 6 main tools return JSON with resource_uri
- ✅ No syntax errors
- ✅ Server starts without errors
- ✅ Discovery endpoints work
- ✅ Resource access works
- ✅ Cache populates correctly
- ✅ TTL expiration works

---

**Ready to Continue**: Start with Step 1 (scrape_url) and work through sequentially.
