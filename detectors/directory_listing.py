from core.base_detector import BaseDetector, Finding

class DirectoryListing(BaseDetector):
    DIRS_TO_CHECK = ['/wp-content/uploads/', '/wp-includes/', '/wp-content/plugins/']

    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        for path in self.DIRS_TO_CHECK:
            full = url.rstrip('/') + path
            status, body, _ = await session.get(full)
            if status == 200 and ('Index of' in body or 'Parent Directory' in body):
                findings.append(Finding(
                    "Directory Listing",
                    "high",
                    f"Directory listing is enabled on {path}.",
                    "Disable directory indexing in the web server configuration (e.g., Options -Indexes in Apache)."
                ))
        return findings