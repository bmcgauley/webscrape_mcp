#!/usr/bin/env python3
"""
Script to update all tool functions to return resource URIs instead of full content.
"""

def update_scrape_url():
    with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace the formatting and return logic in scrape_url
    old_pattern = """        # Format response based on requested format
        if params.response_format == ResponseFormat.JSON:
            result = {
                "url": params.url,
                "status_code": status_code,
                "scraped_at": datetime.utcnow().isoformat() + "Z"
            }

            if metadata:
                result["metadata"] = metadata

            # Get text content
            result["content"] = _html_to_text(soup)

            if links:
                result["links"] = links
                result["link_count"] = len(links)

            if images:
                result["images"] = images
                result["image_count"] = len(images)

            content = json.dumps(result, indent=2)

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

            content = "".join(result_parts)

        elif params.response_format == ResponseFormat.TEXT:
            content = _html_to_text(soup)

        else:  # HTML
            content = html_content

        # Truncate if necessary
        content, was_truncated = _truncate_response(content, params.response_format.value)

        if was_truncated:
            content += "\\n\\n⚠️ Response truncated due to size limit. Use response_format='json' or scrape specific sections for full content."

        return content"""

    new_pattern = """        # Format response based on requested format
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

        return json.dumps(response, indent=2)"""

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("[OK] Updated scrape_url")
    else:
        print("[WARN] Could not find exact pattern in scrape_url")

    # Also update the error handler
    old_error = """    except Exception as e:
        return f"Error scraping {params.url}: {str(e)}\""""

    new_error = """    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "url": params.url
        }, indent=2)"""

    content = content.replace(old_error, new_error)

    with open('webscrape_mcp.py', 'w', encoding='utf-8') as f:
        f.write(content)

def update_scrape_multiple_urls():
    with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Update the results processing in scrape_multiple_urls
    old_pattern = """        for url, result in zip(params.urls, results):
            if isinstance(result, Exception):
                output["results"].append({
                    "url": url,
                    "success": False,
                    "error": str(result)
                })
            else:
                output["results"].append({
                    "url": url,
                    "success": True,
                    "content": result
                })"""

    new_pattern = """        for url, result in zip(params.urls, results):
            if isinstance(result, Exception):
                output["results"].append({
                    "url": url,
                    "success": False,
                    "error": str(result)
                })
            else:
                # result is already a JSON string with resource URIs from scrape_url
                try:
                    result_data = json.loads(result)
                    output["results"].append(result_data)
                except:
                    # Fallback if result isn't JSON
                    output["results"].append({
                        "url": url,
                        "success": True,
                        "content": result
                    })"""

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("[OK] Updated scrape_multiple_urls")
    else:
        print("[WARN] Could not find exact pattern in scrape_multiple_urls")

    with open('webscrape_mcp.py', 'w', encoding='utf-8') as f:
        f.write(content)

def update_crawl_site():
    with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Update the crawl results storage
    old_pattern = """                # Store result
                results.append({
                    "url": current_url,
                    "depth": depth,
                    "title": metadata.get("title"),
                    "status_code": status_code,
                    "content": content[:5000] if len(content) > 5000 else content  # Limit individual page content
                })"""

    new_pattern = """                # Generate scrape ID and store in cache
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
                    "metadata_uri": f"scrape://{scrape_id}/metadata",
                    "title": metadata.get("title"),
                    "status_code": status_code,
                    "content_length": len(content),
                    "preview": content[:200] + "..." if len(content) > 200 else content
                })"""

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("[OK] Updated crawl_site")
    else:
        print("[WARN] Could not find exact pattern in crawl_site")

    with open('webscrape_mcp.py', 'w', encoding='utf-8') as f:
        f.write(content)

def update_scrape_with_js():
    with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Update the JS scraping return logic
    old_pattern = """                # Format response
                if params.response_format == ResponseFormat.JSON:
                    result = {
                        "url": params.url,
                        "title": metadata.get("title"),
                        "scraped_at": datetime.utcnow().isoformat() + "Z",
                        "content": _html_to_text(soup)
                    }
                    content = json.dumps(result, indent=2)

                elif params.response_format == ResponseFormat.MARKDOWN:
                    markdown = _html_to_markdown(html_content, params.url)
                    content = f"# {metadata.get('title', 'Untitled Page')}\\n\\n{markdown}"

                elif params.response_format == ResponseFormat.TEXT:
                    content = _html_to_text(soup)

                else:  # HTML
                    content = html_content

                # Truncate if necessary
                content, was_truncated = _truncate_response(content, params.response_format.value)

                if was_truncated:
                    content += "\\n\\n⚠️ Response truncated due to size limit."

                return content"""

    new_pattern = """                # Format response
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

                return json.dumps(response, indent=2)"""

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("[OK] Updated scrape_with_js")
    else:
        print("[WARN] Could not find exact pattern in scrape_with_js")

    with open('webscrape_mcp.py', 'w', encoding='utf-8') as f:
        f.write(content)

def update_screenshot_url():
    with open('webscrape_mcp.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Update screenshot to return resource URI
    old_pattern = """                # Get page title
                title = await page.title()

                result = {
                    "url": params.url,
                    "title": title,
                    "viewport": {
                        "width": params.width,
                        "height": params.height
                    },
                    "full_page": params.full_page,
                    "screenshot_size_bytes": len(screenshot_bytes),
                    "captured_at": datetime.utcnow().isoformat() + "Z",
                    "image_data": f"data:image/png;base64,{screenshot_b64}"
                }

                content = json.dumps(result, indent=2)

                return content"""

    new_pattern = """                # Get page title
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

                return content"""

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("[OK] Updated screenshot_url")
    else:
        print("[WARN] Could not find exact pattern in screenshot_url")

    with open('webscrape_mcp.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    print("Updating tool functions to return resource URIs...")
    update_scrape_url()
    update_scrape_multiple_urls()
    update_crawl_site()
    update_scrape_with_js()
    update_screenshot_url()
    print("\\n[OK] All tool functions updated!")
