from core.base_detector import BaseDetector, Finding

class BackdoorPatterns(BaseDetector):
    # Known malicious filenames often left by attackers
    BACKDOOR_FILES = [
        '/shell.php', '/cmd.php', '/c99.php', '/r57.php', '/upload.php',
        '/wp-content/uploads/shell.php', '/wp-admin/includes/shell.php',
        '/adminer.php', '/1.php', '/wp-login.php.bak'
    ]

    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        for path in self.BACKDOOR_FILES:
            full = url.rstrip('/') + path
            status, body, _ = await session.get(full)
            if status == 200:
                # Check for common obfuscated PHP patterns
                if any(pattern in body for pattern in ['eval(', 'base64_decode(', '<?php']):
                    findings.append(Finding(
                        "Backdoor Pattern",
                        "critical",
                        f"Potential backdoor file found at {path}. Contains suspicious code.",
                        "Immediately remove the file and investigate server compromise. Change all passwords."
                    ))
        return findings