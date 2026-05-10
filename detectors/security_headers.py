from core.base_detector import BaseDetector, Finding

class SecurityHeaders(BaseDetector):
    HEADERS = {
        'Content-Security-Policy': {'missing_sev': 'high', 'rec': 'Define a strict CSP to prevent XSS.'},
        'Strict-Transport-Security': {'missing_sev': 'high', 'rec': 'Enable HSTS with max-age >= 1 year.'},
        'X-Frame-Options': {'missing_sev': 'medium', 'rec': 'Set X-Frame-Options to DENY or SAMEORIGIN.'},
        'X-Content-Type-Options': {'missing_sev': 'medium', 'rec': 'Add X-Content-Type-Options: nosniff.'},
        'Referrer-Policy': {'missing_sev': 'low', 'rec': 'Set a restrictive Referrer-Policy.'},
        'Permissions-Policy': {'missing_sev': 'low', 'rec': 'Limit browser feature permissions.'},
    }

    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        headers_lower = {k.lower(): v for k, v in headers.items()}
        for header, meta in self.HEADERS.items():
            if header.lower() not in headers_lower:
                findings.append(Finding(
                    "Security Headers",
                    meta['missing_sev'],
                    f"Missing security header: {header}.",
                    meta['rec']
                ))
        # Also check HTTPS redirection
        if not url.startswith('https://'):
            findings.append(Finding(
                "Security Headers",
                "critical",
                "Site does not enforce HTTPS.",
                "Redirect all HTTP traffic to HTTPS and enable HSTS."
            ))
        return findings