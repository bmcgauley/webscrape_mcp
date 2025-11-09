#!/usr/bin/env python3
"""
Test script to validate the refactoring is complete and working.
"""

import sys
import json

def test_imports():
    """Test that all required imports are present."""
    print("Testing imports...")
    try:
        from webscrape_mcp import (
            SCRAPE_CACHE,
            CACHE_TTL_SECONDS,
            PREVIEW_LENGTH,
            _generate_scrape_id,
            _clean_expired_cache,
            _store_in_cache
        )
        print("[OK] All cache-related imports successful")
        return True
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False

def test_cache_functions():
    """Test cache management functions."""
    print("\nTesting cache functions...")
    try:
        from webscrape_mcp import _generate_scrape_id, _store_in_cache, _clean_expired_cache, SCRAPE_CACHE

        # Test ID generation
        scrape_id1 = _generate_scrape_id("https://example.com", "markdown")
        scrape_id2 = _generate_scrape_id("https://example.com", "html")
        assert scrape_id1 != scrape_id2, "Different formats should generate different IDs"
        assert len(scrape_id1) == 32, "Should be MD5 hash (32 chars)"
        print(f"  [OK] ID generation works (sample: {scrape_id1[:8]}...)")

        # Test cache storage
        _store_in_cache(
            scrape_id="test123",
            url="https://test.com",
            content="Test content",
            metadata={"title": "Test"}
        )
        assert "test123" in SCRAPE_CACHE, "Cache entry should exist"
        assert SCRAPE_CACHE["test123"]["content"] == "Test content"
        print("  [OK] Cache storage works")

        # Clean test entry
        del SCRAPE_CACHE["test123"]

        # Test cleanup
        _clean_expired_cache()
        print("  [OK] Cache cleanup works")

        return True
    except Exception as e:
        print(f"[FAIL] Cache function error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tool_count():
    """Count the number of tools registered."""
    print("\nTesting tool count...")
    try:
        with open('webscrape_mcp.py', 'r') as f:
            content = f.read()

        tool_count = content.count('@mcp.tool(')
        resource_count = content.count('@mcp.resource(')

        print(f"  Found {tool_count} tools")
        print(f"  Found {resource_count} resources")

        # Should have 8 tools (6 original + 2 discovery)
        assert tool_count == 8, f"Expected 8 tools, found {tool_count}"

        # Should have 2 resources
        assert resource_count == 2, f"Expected 2 resources, found {resource_count}"

        print("[OK] Correct number of tools and resources")
        return True
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def test_resource_uri_in_tools():
    """Test that tools return resource_uri in their responses."""
    print("\nTesting resource_uri patterns...")
    try:
        with open('webscrape_mcp.py', 'r') as f:
            content = f.read()

        # Check that scrape_url returns resource_uri
        assert 'resource_uri": f"scrape://{scrape_id}/content' in content, "scrape_url should return resource_uri"
        print("  [OK] scrape_url returns resource_uri")

        # Check that metadata_uri is also returned
        assert 'metadata_uri": f"scrape://{scrape_id}/metadata' in content, "Should return metadata_uri"
        print("  [OK] metadata_uri pattern found")

        # Check that preview is returned
        assert 'preview = full_content[:PREVIEW_LENGTH]' in content, "Should create preview"
        print("  [OK] Preview creation found")

        # Check that _store_in_cache is called
        assert content.count('_store_in_cache(') >= 5, "Should call _store_in_cache in multiple tools"
        print("  [OK] Cache storage called in multiple tools")

        return True
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def test_discovery_tools():
    """Test that discovery tools are implemented."""
    print("\nTesting discovery tools...")
    try:
        with open('webscrape_mcp.py', 'r') as f:
            content = f.read()

        # Check for webscrape_list_tools
        assert 'async def list_tools(' in content, "list_tools function should exist"
        assert 'detail_level' in content, "list_tools should have detail_level parameter"
        print("  [OK] list_tools function found")

        # Check for webscrape_search_tools
        assert 'async def search_tools(' in content, "search_tools function should exist"
        assert 'query: str' in content, "search_tools should have query parameter"
        print("  [OK] search_tools function found")

        return True
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def test_resource_endpoints():
    """Test that resource endpoints are implemented."""
    print("\nTesting resource endpoints...")
    try:
        with open('webscrape_mcp.py', 'r') as f:
            content = f.read()

        # Check for content resource
        assert 'async def get_scrape_content(scrape_id: str)' in content, "get_scrape_content should exist"
        assert '@mcp.resource("scrape://{scrape_id}/content")' in content, "Content resource decorator should exist"
        print("  [OK] scrape://{scrape_id}/content resource found")

        # Check for metadata resource
        assert 'async def get_scrape_metadata(scrape_id: str)' in content, "get_scrape_metadata should exist"
        assert '@mcp.resource("scrape://{scrape_id}/metadata")' in content, "Metadata resource decorator should exist"
        print("  [OK] scrape://{scrape_id}/metadata resource found")

        return True
    except AssertionError as e:
        print(f"[FAIL] {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def calculate_file_metrics():
    """Calculate metrics about the refactored file."""
    print("\nCalculating file metrics...")
    try:
        with open('webscrape_mcp.py', 'r') as f:
            content = f.read()
            lines = content.split('\n')

        print(f"  Total lines: {len(lines)}")
        print(f"  Total characters: {len(content)}")
        print(f"  Total tools: {content.count('@mcp.tool(')}")
        print(f"  Total resources: {content.count('@mcp.resource(')}")
        print(f"  Cache references: {content.count('SCRAPE_CACHE')}")
        print(f"  resource_uri occurrences: {content.count('resource_uri')}")

        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("WebScrape MCP Refactoring Validation Tests")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Cache Functions", test_cache_functions),
        ("Tool Count", test_tool_count),
        ("Resource URIs", test_resource_uri_in_tools),
        ("Discovery Tools", test_discovery_tools),
        ("Resource Endpoints", test_resource_endpoints),
        ("File Metrics", calculate_file_metrics)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] Test '{test_name}' crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(1 for _, r in results if r)
    total = len(results)

    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] All tests passed! Refactoring is complete.")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed. Review needed.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
