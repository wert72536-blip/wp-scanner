# WordPress / WooCommerce Security Scanner
A fast, non-destructive vulnerability scanner for WordPress and WooCommerce websites.
## Features

   - WordPress & WooCommerce Detection: Identifies the core CMS and its specific version.
   - Asset Enumeration: Lists all active themes and plugins.
   - Endpoint Analysis: Checks for exposed endpoints (e.g., xmlrpc.php, REST API).
   - Directory Listing: Detects if directory indexing is enabled.
   - Leak Detection: Searches for debug logs and wp-config.php backup files.
   - Malware Detection: Scans for suspicious patterns and signatures (e.g., eval, base64_decode).
   - Security Headers Analysis: Evaluates HTTP headers (CSP, HSTS, X-Frame-Options, etc.).
   - Login Security: Checks wp-login.php accessibility and brute-force protection.
   - Access Control: Identifies HTTPS issues and unauthorized access to sensitive files.
   - Comprehensive Reporting: Generates JSON reports categorized by risk level with actionable recommendations.
   - Modular Architecture: Designed for easy integration of new custom checks.

## Requirements

   - Python 3.9+
   - Install dependencies:
        pip install -r requirements.txt


## WordPress Security Scanner: Usage Instructions

    Navigate to the Project Folder
    Open your terminal and run:
    cd path/to/wp-scanner
    Ensure Dependencies Are Installed
    If you haven't installed the required libraries yet, run:
    pip install -r requirements.txt
    (or pip3 depending on your system).
    Select a Target
    Specify the domain or URL of the site you want to check.
    Examples:
        https://example.com
        http://mysite.ru
        shop.mydomain.bg (if the scheme is missing, https:// will be used by default).
        Important: Only scan resources you own or have explicit permission from the owner to test.
    Run the Scan
    Basic command (output to console):
    python scanner.py --url https://example.comTo save the report to a file:
    python scanner.py --url https://example.com --output report.jsonFor a "gentle" mode (1-second delay between requests) with detailed logging:
    python scanner.py --url https://example.com --output report.json --verbose --delay 1.0Full list of parameters:
        --url – Required, target URL.
        --output – Save JSON report to the specified file. If omitted, the report displays in the console.
        --delay – Delay between requests in seconds (default is 0.5).
        --verbose – Enable detailed execution logs.
    Analyze the Results
    Once finished, you will receive a JSON output with the following fields:
        risk_score (0-100) – Overall threat level.
        severity_summary – Count of issues by level (critical, high, medium, low, info).
        issues – A list of found vulnerabilities with descriptions and recommendations.
    Troubleshooting
        ModuleNotFoundError: No module named 'aiohttp' → Libraries are missing; repeat Step 2.
        ConnectionError or Timeout → Check if the site is up or try increasing the --delay to 2–3 seconds.
        If the scanner fails to detect WordPress → Ensure the site is actually running on WordPress, or run with the --verbose flag for diagnostics.

Done. The scanner performs a non-destructive check without attacking the site and provides a clear, readable report.