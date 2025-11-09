/**
 * Recursively crawl a website starting from a given URL
 *
 * This tool discovers and scrapes pages by following links, respecting
 * depth and page limits. Perfect for exploring website structure or
 * scraping multiple related pages.
 *
 * @category scraping
 * @returns_resource true
 */
export interface CrawlSiteParams {
  /** Starting URL to crawl from */
  url: string;

  /** Maximum crawl depth (0 = only start URL, 1 = start + direct links, etc.) */
  max_depth?: number; // 0-5, default 2

  /** Maximum number of pages to crawl */
  max_pages?: number; // 1-100, default 20

  /** Only crawl URLs from the same domain */
  same_domain_only?: boolean;

  /** Output format for crawled pages */
  response_format?: "markdown" | "html" | "text" | "json";
}

export interface CrawlSiteResult {
  /** Operation success status */
  success: boolean;

  /** Starting URL */
  start_url: string;

  /** Number of pages successfully crawled */
  pages_crawled: number;

  /** Maximum depth configured */
  max_depth: number;

  /** Maximum pages configured */
  max_pages: number;

  /** When crawl was performed */
  crawled_at: string;

  /** Array of crawled pages with resource references */
  results: Array<{
    url: string;
    depth: number;
    scrape_id?: string;
    resource_uri?: string;
    title?: string;
    status_code?: number;
    content_length?: number;
    preview?: string;
    error?: string;
  }>;
}
