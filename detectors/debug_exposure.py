from core.base_detector import BaseDetector, Finding

class DebugExposure(BaseDetector):
    PATHS = [
        '/wp-content/debug.log',
        '/wp-content/debug.log',
        '/wp-config-sample.php',
        '/wp-config.php~',
        '/wp-config.php.bak',
        '/wp-config.php.old',
        '/wp-config.php.save',
        '/.wp-config.php.swp',
    ]

    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        for path in self.PATHS:
            full = url.rstrip('/') + path
            status, body, _ = await session.get(full)
            if status == 200:
                sev = 'critical' if 'wp-config' in path.lower() else 'high'
                findings.append(Finding(
                    "Debug / Config Exposure",
                    sev,
                    f"Sensitive file exposed: {path}",
                    "Immediately remove or block public access to this file. Review wp-config.php for secrets and change them if leaked."
                ))
        # Check for PHP errors in homepage HTML
        if 'Notice:' in html or 'Warning:' in html or 'Fatal error:' in html:
            findings.append(Finding(
                "Debug Exposure",
                "high",
                "PHP errors are displayed on the site. Debug mode may be enabled.",
                "Disable WP_DEBUG and WP_DEBUG_DISPLAY in wp-config.php, and set error_reporting to off in production."
            ))
        return findings