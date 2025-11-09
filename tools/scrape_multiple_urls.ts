/**
 * Scrape multiple URLs concurrently
 *
 * This tool efficiently scrapes multiple web pages at once, making it ideal
 * for batch operations. Maximum 20 URLs per request.
 *
 * @category scraping
 * @returns_resource true
 */
export interface ScrapeMultipleUrlsParams {
  /** List of URLs to scrape (1-20 URLs) */
  urls: string[];

  /** Output format for all pages */
  response_format?: "markdown" | "html" | "text" | "json";

  /** Include page metadata */
  include_metadata?: boolean;
}

export interface ScrapeMultipleUrlsResult {
  /** Operation success status */
  success: boolean;

  /** Total number of URLs processed */
  total_urls: number;

  /** When scraping was performed */
  scraped_at: string;

  /** Array of individual scrape results */
  results: Array<{
    url: string;
    success: boolean;
    scrape_id?: string;
    resource_uri?: string;
    preview?: string;
    content_length?: number;
    error?: string;
  }>;
}
