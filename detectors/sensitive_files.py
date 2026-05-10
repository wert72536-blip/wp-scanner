from core.base_detector import BaseDetector, Finding

class SensitiveFiles(BaseDetector):
    FILES = [
        '/readme.html',
        '/license.txt',
        '/wp-config-sample.php',
        '/wp-admin/install.php',
        '/wp-content/debug.log',
    ]

    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        for path in self.FILES:
            full = url.rstrip('/') + path
            status, _, _ = await session.get(full)
            if status == 200:
                sev = 'critical' if 'wp-config' in path else 'high'
                findings.append(Finding(
                    "Sensitive Files",
                    sev,
                    f"Publicly accessible sensitive file: {path}.",
                    "Delete the file or deny public access in web server configuration."
                ))
        return findings