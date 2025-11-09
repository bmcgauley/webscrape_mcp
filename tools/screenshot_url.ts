/**
 * Capture a screenshot of a web page
 *
 * This tool renders a page and captures it as an image, useful for
 * visual documentation, testing, or archival purposes.
 *
 * Note: Requires Playwright to be installed.
 * Install with: pip install playwright && playwright install chromium
 *
 * @category rendering
 * @returns_resource true
 */
export interface ScreenshotUrlParams {
  /** URL to screenshot */
  url: string;

  /** Capture full page (true) or visible viewport only (false) */
  full_page?: boolean;

  /** Browser viewport width in pixels (320-3840) */
  width?: number;

  /** Browser viewport height in pixels (240-2160) */
  height?: number;
}

export interface ScreenshotUrlResult {
  /** Operation success status */
  success: boolean;

  /** Unique identifier for this screenshot */
  scrape_id: string;

  /** URL that was screenshot */
  url: string;

  /** Page title */
  title: string;

  /** Resource URI to fetch screenshot image data */
  resource_uri: string;

  /** Viewport dimensions used */
  viewport: {
    width: number;
    height: number;
  };

  /** Whether full page was captured */
  full_page: boolean;

  /** Screenshot file size in bytes */
  screenshot_size_bytes: number;

  /** When screenshot was captured */
  captured_at: string;

  /** When cached screenshot expires */
  expires_at: string;

  /** Note about retrieving the screenshot */
  note: string;
}
