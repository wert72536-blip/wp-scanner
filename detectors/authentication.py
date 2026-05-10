from core.base_detector import BaseDetector, Finding

class Authentication(BaseDetector):
    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        login_url = url.rstrip('/') + '/wp-login.php'
        status, body, _ = await session.get(login_url)
        if status == 200:
            findings.append(Finding(
                "Authentication",
                "medium",
                "wp-login.php is publicly accessible.",
                "Restrict access to wp-login.php by IP whitelisting or use a CAPTCHA plugin."
            ))
            # Check for evidence of rate limiting plugins
            if 'limit-login-attempts' not in body.lower() and 'wordfence' not in body.lower():
                findings.append(Finding(
                    "Authentication",
                    "high",
                    "No indication of brute-force protection on login page.",
                    "Install a plugin like Wordfence or Limit Login Attempts Reloaded."
                ))
        return findings