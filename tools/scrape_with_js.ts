/**
 * Scrape JavaScript-rendered pages using a headless browser
 *
 * This tool uses Playwright to render JavaScript and capture dynamic content
 * that isn't available in the raw HTML. Essential for modern SPAs and
 * dynamically loaded content.
 *
 * Note: Requires Playwright to be installed.
 * Install with: pip install playwright && playwright install chromium
 *
 * @category rendering
 * @returns_resource true
 */
export interface ScrapeWithJsParams {
  /** URL to scrape with JavaScript rendering */
  url: string;

  /** CSS selector to wait for before scraping (optional) */
  wait_for_selector?: string;

  /** Additional seconds to wait for page load (0-30) */
  wait_seconds?: number;

  /** Output format */
  response_format?: "markdown" | "html" | "text" | "json";
}

export interface ScrapeWithJsResult {
  /** Operation success status */
  success: boolean;

  /** Unique identifier for this scrape */
  scrape_id: string;

  /** Original URL */
  url: string;

  /** Resource URI to fetch full content */
  resource_uri: string;

  /** Resource URI to fetch metadata */
  metadata_uri: string;

  /** Preview of content (first 500 chars) */
  preview: string;

  /** Total content length in bytes */
  content_length: number;

  /** Content format */
  format: string;

  /** Rendering method used */
  rendering_method: "javascript";

  /** When content was scraped */
  scraped_at: string;

  /** When cached content expires */
  expires_at: string;
}
