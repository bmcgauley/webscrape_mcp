/**
 * Web Scraping MCP Tools
 *
 * This module provides TypeScript definitions for all web scraping tools.
 * Tools are organized by category for easy discovery.
 *
 * @module webscrape_mcp/tools
 */

export * from './scrape_url';
export * from './scrape_multiple_urls';
export * from './crawl_site';
export * from './extract_links';
export * from './scrape_with_js';
export * from './screenshot_url';

/**
 * Tool categories for filtering and search
 */
export type ToolCategory = "scraping" | "extraction" | "rendering";

/**
 * Discovery metadata for all tools
 */
export const TOOLS = {
  scraping: [
    "webscrape_scrape_url",
    "webscrape_scrape_multiple_urls",
    "webscrape_crawl_site"
  ],
  extraction: [
    "webscrape_extract_links"
  ],
  rendering: [
    "webscrape_scrape_with_js",
    "webscrape_screenshot_url"
  ]
} as const;

/**
 * Search for tools by keyword
 *
 * @param query - Search term
 * @param category - Optional category filter
 * @returns Array of matching tool names
 */
export function searchTools(query: string, category?: ToolCategory): string[] {
  const allTools = category ? TOOLS[category] : Object.values(TOOLS).flat();
  const queryLower = query.toLowerCase();

  return allTools.filter(tool => tool.toLowerCase().includes(queryLower));
}

/**
 * Get tools by category
 *
 * @param category - Tool category
 * @returns Array of tool names in that category
 */
export function getToolsByCategory(category: ToolCategory): readonly string[] {
  return TOOLS[category];
}
