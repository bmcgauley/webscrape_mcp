#!/usr/bin/env python3
"""Fix the remaining tool functions that weren't updated."""

import re

def fix_scrape_url():
    with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the section starting with "# Format response based on requested format"
    # in scrape_url and replace it

    in_scrape_url = False
    format_section_start = -1

    for i, line in enumerate(lines):
        if 'async def scrape_url(params: ScrapeUrlInput)' in line:
            in_scrape_url = True
        elif in_scrape_url and '# Format response based on requested format' in line:
            format_section_start = i
            break

    if format_section_start == -1:
        print("[ERROR] Could not find format section in scrape_url")
        return

    # Find the end of the section (the return statement before the except)
    format_section_end = -1
    for i in range(format_section_start, len(lines)):
        if i > format_section_start and 'return content' in lines[i]:
            format_section_end = i
            break

    if format_section_end == -1:
        print("[ERROR] Could not find end of format section in scrape_url")
        return

    # Build the replacement
    new_section = '''        # Format response based on requested format
        if params.response_format == ResponseFormat.JSON:
            full_content = json.dumps({
                "url": params.url,
                "status_code": status_code,
                "content": _html_to_text(soup),
                "metadata": metadata if metadata else {},
                "links": links if links else [],
                "images": images if images else []
            }, indent=2)

        elif params.response_format == ResponseFormat.MARKDOWN:
            # Convert to markdown
            markdown_content = _html_to_markdown(html_content, params.url)

            result_parts = []

            if metadata:
                result_parts.append(f"# {metadata.get('title', 'Untitled Page')}\\n")
                if metadata.get('description'):
                    result_parts.append(f"**Description:** {metadata['description']}\\n")
                result_parts.append(f"**URL:** {params.url}\\n")
                result_parts.append("---\\n")

            result_parts.append(markdown_content)

            if links:
                result_parts.append(f"\\n\\n## Found Links ({len(links)})\\n")
                for link in links[:50]:  # Limit to first 50
                    result_parts.append(f"- {link}\\n")
                if len(links) > 50:
                    result_parts.append(f"... and {len(links) - 50} more links\\n")

            if images:
                result_parts.append(f"\\n\\n## Found Images ({len(images)})\\n")
                for img in images[:20]:  # Limit to first 20
                    result_parts.append(f"- {img}\\n")
                if len(images) > 20:
                    result_parts.append(f"... and {len(images) - 20} more images\\n")

            full_content = "".join(result_parts)

        elif params.response_format == ResponseFormat.TEXT:
            full_content = _html_to_text(soup)

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
'''

    # Replace the section
    lines[format_section_start:format_section_end+1] = [new_section]

    with open('webscrape_mcp.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("[OK] Fixed scrape_url")

def fix_scrape_with_js():
    with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the section in scrape_with_js
    in_function = False
    format_section_start = -1

    for i, line in enumerate(lines):
        if 'async def scrape_with_js(params: ScrapeWithJsInput)' in line:
            in_function = True
        elif in_function and '# Format response' in line and 'if params.response_format == ResponseFormat.JSON' in lines[i+1]:
            format_section_start = i
            break

    if format_section_start == -1:
        print("[ERROR] Could not find format section in scrape_with_js")
        return

    # Find the return statement
    format_section_end = -1
    for i in range(format_section_start, len(lines)):
        if 'return content' in lines[i] and i > format_section_start + 5:
            format_section_end = i
            break

    if format_section_end == -1:
        print("[ERROR] Could not find end of format section in scrape_with_js")
        return

    new_section = '''                # Format response
                if params.response_format == ResponseFormat.JSON:
                    full_content = json.dumps({
                        "url": params.url,
                        "title": metadata.get("title"),
                        "content": _html_to_text(soup)
                    }, indent=2)

                elif params.response_format == ResponseFormat.MARKDOWN:
                    markdown = _html_to_markdown(html_content, params.url)
                    full_content = f"# {metadata.get('title', 'Untitled Page')}\\n\\n{markdown}"

                elif params.response_format == ResponseFormat.TEXT:
                    full_content = _html_to_text(soup)

                else:  # HTML
                    full_content = html_content

                # Generate scrape ID and store in cache
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
'''

    lines[format_section_start:format_section_end+1] = [new_section]

    with open('webscrape_mcp.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("[OK] Fixed scrape_with_js")

def fix_screenshot_url():
    with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the section in screenshot_url
    in_function = False
    screenshot_section_start = -1

    for i, line in enumerate(lines):
        if 'async def screenshot_url(params: ScreenshotUrlInput)' in line:
            in_function = True
        elif in_function and '# Get page title' in line:
            screenshot_section_start = i
            break

    if screenshot_section_start == -1:
        print("[ERROR] Could not find screenshot section in screenshot_url")
        return

    # Find the return content statement
    screenshot_section_end = -1
    for i in range(screenshot_section_start, len(lines)):
        if 'return content' in lines[i] and i > screenshot_section_start + 5:
            screenshot_section_end = i
            break

    if screenshot_section_end == -1:
        print("[ERROR] Could not find end of screenshot section")
        return

    new_section = '''                # Get page title
                title = await page.title()

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

                content = json.dumps(result, indent=2)

                return content
'''

    lines[screenshot_section_start:screenshot_section_end+1] = [new_section]

    with open('webscrape_mcp.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("[OK] Fixed screenshot_url")

if __name__ == "__main__":
    print("Fixing remaining tool functions...")
    fix_scrape_url()
    fix_scrape_with_js()
    fix_screenshot_url()
    print("\\n[OK] All tools fixed!")
