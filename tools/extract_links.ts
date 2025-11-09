/**
 * Extract all links from a web page
 *
 * This tool quickly discovers all hyperlinks on a page, making it ideal
 * for building sitemaps or finding related pages.
 *
 * @category extraction
 * @returns_resource false
 */
export interface ExtractLinksParams {
  /** URL to extract links from */
  url: string;

  /** Only return links from the same domain */
  same_domain_only?: boolean;

  /** Include anchor/fragment links (e.g., #section) */
  include_anchors?: boolean;
}

export interface ExtractLinksResult {
  /** Operation success status */
  success: boolean;

  /** URL that was analyzed */
  url: string;

  /** Total number of links found */
  total_links: number;

  /** Number of internal links */
  internal_links_count: number;

  /** Number of external links */
  external_links_count: number;

  /** When extraction was performed */
  extracted_at: string;

  /** Array of internal links */
  internal_links: string[];

  /** Array of external links (empty if same_domain_only is true) */
  external_links: string[];
}
