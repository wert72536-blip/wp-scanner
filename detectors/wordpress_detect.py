from core.base_detector import BaseDetector, Finding
from utils.helpers import is_woocommerce

class WordPressDetection(BaseDetector):
    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        wp_indicators = ['wp-content', 'wp-includes', 'wp-admin', '/wp-json/']
        detected = any(ind in html for ind in wp_indicators)
        if not detected:
            # Try to fetch /wp-admin/ to be sure
            status, body, _ = await session.get(url + '/wp-admin/')
            detected = ('wp-login.php' in body or 'WordPress' in body)
        if not detected:
            findings.append(Finding(
                "Platform", "info",
                "The site does not appear to be a WordPress site.",
                "No WordPress specific recommendations."
            ))
            return findings

        findings.append(Finding(
            "Platform", "info",
            "WordPress detected.",
            "Ensure WordPress and all extensions are kept up to date."
        ))

        # WooCommerce detection
        if is_woocommerce(html, headers):
            findings.append(Finding(
                "Platform", "info",
                "WooCommerce detected.",
                "Regularly update WooCommerce and review security settings."
            ))
        else:
            # Check for WooCommerce REST API base
            wc_status, _, _ = await session.get(url + '/wp-json/wc/v3/')
            if wc_status in (200, 401, 403):
                findings.append(Finding(
                    "Platform", "info",
                    "WooCommerce appears to be present (REST API endpoint found).",
                    "Verify that the API is properly secured if not needed."
                ))
        return findings