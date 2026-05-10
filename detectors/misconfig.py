from core.base_detector import BaseDetector, Finding

class Misconfig(BaseDetector):
    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        # Check HTTP to HTTPS redirect
        if url.startswith('https://'):
            http_url = url.replace('https://', 'http://', 1)
            status, _, resp_headers = await session.get(http_url, allow_redirects=False)
            if status == 200:
                findings.append(Finding(
                    "Misconfiguration",
                    "critical",
                    "HTTP is accessible without redirecting to HTTPS.",
                    "Implement a 301 redirect from HTTP to HTTPS."
                ))
            elif status in (301, 302):
                location = resp_headers.get('Location', '')
                if not location.startswith('https://'):
                    findings.append(Finding(
                        "Misconfiguration",
                        "high",
                        "HTTP redirects to another HTTP or incorrect location.",
                        "Ensure redirect goes to the HTTPS version."
                    ))
        # Check for www vs non-www consistency
        # (skipped for brevity)
        return findings