import re
from urllib.parse import urljoin
from core.base_detector import BaseDetector, Finding

class ThemePluginEnum(BaseDetector):
    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        # Extract theme from stylesheet URL pattern: /wp-content/themes/{theme}/
        theme_match = re.search(r'/wp-content/themes/([^/]+)/', html)
        if theme_match:
            theme_name = theme_match.group(1)
            findings.append(Finding(
                "Themes",
                "low",
                f"Active theme detected: {theme_name}",
                "Keep the theme updated and remove unused themes."
            ))
        # Extract plugins from resource URLs: /wp-content/plugins/{plugin}/
        plugins = set(re.findall(r'/wp-content/plugins/([^/]+)/', html))
        for plugin in plugins:
            if plugin not in ['woocommerce', 'elementor', 'contact-form-7']:  # example; not a real check
                pass
            findings.append(Finding(
                "Plugins",
                "low",
                f"Plugin detected: {plugin}",
                "Ensure all plugins are up to date and necessary."
            ))
        # Check readme files of common plugins for version? Could be done but minimal.
        return findings