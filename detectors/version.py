from core.base_detector import BaseDetector, Finding
from utils.helpers import extract_version_from_meta

class WordPressVersion(BaseDetector):
    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        version = extract_version_from_meta(html)
        if version:
            # Simple check: assume latest stable is 6.5 (as of 2025-05) – would be updated dynamically in production
            # We'll treat anything below 6.0 as outdated
            try:
                major = int(version.split('.')[0])
                if major < 6:
                    findings.append(Finding(
                        "WordPress Version",
                        "high" if major < 5 else "medium",
                        f"WordPress version {version} is exposed and outdated.",
                        "Update WordPress to the latest version and consider hiding the version number."
                    ))
                else:
                    findings.append(Finding(
                        "WordPress Version",
                        "low",
                        f"WordPress version {version} is exposed.",
                        "Remove the generator meta tag to hide the version."
                    ))
            except:
                pass
        else:
            # Might still be in readme.html
            readme_status, readme_body, _ = await session.get(url + '/readme.html')
            if readme_status == 200:
                import re
                match = re.search(r'Version\s+([\d.]+)', readme_body)
                if match:
                    version = match.group(1)
                    findings.append(Finding(
                        "WordPress Version",
                        "high",
                        f"WordPress version {version} exposed via readme.html.",
                        "Remove or block access to readme.html, and hide version."
                    ))
        return findings