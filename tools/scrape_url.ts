/**
 * Scrape a single URL and return content in various formats
 *
 * This tool fetches a web page and extracts its content. Instead of returning
 * full content (which can be 25KB+), it stores the content and returns a
 * resource URI for efficient retrieval.
 *
 * @category scraping
 * @returns_resource true
 */
export interface ScrapeUrlParams {
  /** URL to scrape (must start with http:// or https://) */
  url: string;

  /** Output format */
  response_format?: "markdown" | "html" | "text" | "json";

  /** Include all links found on page */
  include_links?: boolean;

  /** Include image URLs found on page */
  include_images?: boolean;

  /** Include page metadata (title, description, etc.) */
  include_metadata?: boolean;
}

export interface ScrapeUrlResult {
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

  /** HTTP status code */
  status_code: number;

  /** When content was scraped */
  scraped_at: string;

  /** When cached content expires */
  expires_at: string;

  /** Statistics about the scrape */
  stats: {
    total_links: number;
    total_images: number;
    has_metadata: boolean;
  };
}
