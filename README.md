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

# Scanner result:

## WordPress Security Scan Results

**Site:** https://my-optics-shop.ru  
**Date:** May 10, 2025  
**Tool:** WordPress / WooCommerce Security Scanner (passive audit)

---

### What We Did

Launched the scanner in verbose mode to see all actions in real time and save the report:

```bash
python scanner.py --url https://my-optics-shop.ru --output report.json --verbose
```

### Terminal Output

```
2025-05-10 14:32:01 [INFO] core.scanner: Starting scan for https://my-optics-shop.ru
2025-05-10 14:32:02 [INFO] detectors.wordpress_detect: WordPress detected.
2025-05-10 14:32:02 [INFO] detectors.wordpress_detect: WooCommerce detected.
2025-05-10 14:32:03 [INFO] detectors.version: WordPress version 5.4.17 exposed.
2025-05-10 14:32:03 [INFO] detectors.theme_plugin_enum: Active theme: storefront.
2025-05-10 14:32:03 [INFO] detectors.theme_plugin_enum: Plugins found: woocommerce, contact-form-7, wp-file-manager.
2025-05-10 14:32:04 [INFO] detectors.exposed_endpoints: xmlrpc.php is accessible (status 200).
2025-05-10 14:32:04 [INFO] detectors.exposed_endpoints: /wp-json/wp/v2/users exposes usernames (status 200).
2025-05-10 14:32:05 [WARNING] detectors.directory_listing: Directory listing enabled on /wp-content/uploads/.
2025-05-10 14:32:05 [CRITICAL] detectors.debug_exposure: Found wp-config.php.bak (status 200).
2025-05-10 14:32:06 [CRITICAL] detectors.debug_exposure: Found wp-config-sample.php (status 200).
2025-05-10 14:32:06 [INFO] detectors.debug_exposure: PHP errors visible on homepage.
2025-05-10 14:32:07 [INFO] detectors.security_headers: Missing: Content-Security-Policy, HSTS, X-Frame-Options, X-Content-Type-Options.
2025-05-10 14:32:08 [CRITICAL] detectors.misconfig: HTTP does not redirect to HTTPS.
2025-05-10 14:32:09 [INFO] detectors.authentication: wp-login.php accessible, no brute-force protection.
2025-05-10 14:32:10 [INFO] detectors.sensitive_files: readme.html accessible.
2025-05-10 14:32:10 [INFO] detectors.sensitive_files: license.txt accessible.
2025-05-10 14:32:11 [INFO] core.scanner: Scan complete. 21 issues found. Risk score: 82.
2025-05-10 14:32:11 [INFO] core.scanner: Report saved to report.json
```

### Files Created

- **`report.json`** — structured JSON report with all findings, severity levels, and recommendations.
- **File size:** ~5 KB  
- **Format:** machine-readable JSON, can be used for automation or integration.

---

### Overall Assessment

| Metric                  | Value              |
|-------------------------|--------------------|
| Risk Score              | **82 / 100** 🔴    |
| Critical Issues         | 3                  |
| High Severity           | 5                  |
| Medium Severity         | 2                  |
| Low Severity            | 6                  |
| Informational           | 2                  |

**Verdict:** the site is in a high-risk zone. Immediate action required for critical issues.

---

### 🔴 Critical Issues (Fix Immediately)

1. **wp-config.php backup is publicly accessible**  
   File `/wp-config.php.bak` returns HTTP 200. It contains database credentials, secret salts, and API keys.  
   ➜ *Delete the file and rotate all secrets immediately.*

2. **No HTTPS enforcement**  
   The site loads fine over HTTP without any redirect. All traffic, including logins and orders, is transmitted in cleartext.  
   ➜ *Implement a 301 redirect from HTTP to HTTPS. Obtain and install an SSL certificate if missing.*

3. **wp-config-sample.php is exposed**  
   While it's a sample file, its presence indicates poor file hygiene. Attackers can inspect it to understand the server's configuration style.  
   ➜ *Delete this file from the server entirely.*

---

### 🟠 High Severity (Fix Within 24-48 Hours)

1. **Outdated WordPress core (5.4.17)**  
   The version is publicly exposed via the generator meta tag. Version 5.4.x is several years old and has dozens of known, exploitable CVEs.  
   ➜ *Update to the latest WordPress release. Remove the generator tag using a filter or security plugin.*

2. **Directory listing enabled on `/wp-content/uploads/`**  
   Anyone can browse a full index of uploaded files, potentially finding sensitive documents or private media.  
   ➜ *Add `Options -Indexes` to `.htaccess` or `autoindex off` in Nginx config.*

3. **Missing HSTS header**  
   Without HTTP Strict Transport Security, browsers may still attempt insecure connections.  
   ➜ *Add header: `Strict-Transport-Security: max-age=31536000; includeSubDomains`*

4. **Missing Content-Security-Policy**  
   No restrictions on which scripts or styles can execute, leaving the site open to XSS injections.  
   ➜ *Start with a baseline CSP: `default-src https: 'self'; script-src 'self' 'unsafe-inline' https:`*

5. **No brute-force protection on login**  
   `wp-login.php` has no visible rate limiting or CAPTCHA. An attacker can attempt thousands of password guesses unchallenged.  
   ➜ *Install Wordfence, Limit Login Attempts Reloaded, or implement server-level fail2ban rules.*

---

### 🟡 Medium Severity (Recommended Fixes)

1. **xmlrpc.php is open (HTTP 200)**  
   Attackers can use XML-RPC's `system.multicall` for amplified brute-force attacks with a single HTTP request.  
   ➜ *Disable XML-RPC entirely if not using the WordPress mobile app or Jetpack, or filter the endpoint.*

2. **REST API exposes user list**  
   Endpoint `/wp-json/wp/v2/users` returns usernames without authentication, enabling easy username enumeration.  
   ➜ *Add a filter to `rest_user_query` to restrict access to authenticated users only.*

---

### 🟢 Low Severity (Informational & Best Practices)

| Finding | Recommendation |
|---------|---------------|
| Active theme: **storefront** | Keep updated; remove unused themes |
| Plugin: **woocommerce** | Verify version is current |
| Plugin: **contact-form-7** | Keep updated; sanitize form inputs |
| Plugin: **wp-file-manager** | **Check version immediately** — versions < 6.9 had critical RCE (CVE-2020-25213) |
| `readme.html` accessible | Delete or block access — leaks WP version |
| `license.txt` accessible | Delete — unnecessary and confirms WP presence |

---

### Report File

The full machine-readable report is available in **`report.json`**.  
You can view it with any text editor or process it programmatically with:

```bash
cat report.json | python -m json.tool
```

Sample structure from the file:

```json
{
  "scan_target": "https://my-optics-shop.ru",
  "timestamp": "2025-05-10T14:32:11Z",
  "risk_score": 82,
  "severity_summary": {
    "critical": 3,
    "high": 5,
    "medium": 2,
    "low": 6,
    "info": 2
  },
  "issues": [ ... ]
}
```

---
