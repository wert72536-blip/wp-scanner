import re
from urllib.parse import urlparse
from typing import Optional

def normalize_url(url: str) -> str:
    """Ensure URL has scheme and ends without a trailing slash."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.rstrip('/')

def get_domain(url: str) -> str:
    return urlparse(url).netloc

def extract_version_from_meta(html: str) -> Optional[str]:
    """Extract WordPress version from generator meta tag."""
    match = re.search(r'<meta\s+name="generator"\s+content="WordPress\s+([\d.]+)"', html, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def is_woocommerce(html: str, headers: dict) -> bool:
    """Check if WooCommerce is likely installed."""
    if 'woocommerce' in html.lower():
        return True
    if 'wp-content/plugins/woocommerce' in html:
        return True
    return False