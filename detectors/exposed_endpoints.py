from core.base_detector import BaseDetector, Finding

class ExposedEndpoints(BaseDetector):
    ENDPOINTS = {
        'xmlrpc.php': 'XML-RPC endpoint enabled. Can be used for brute force and DDoS attacks.',
        'wp-json/wp/v2/users': 'REST API user endpoint may expose usernames.',
        'wp-json/': 'REST API is public.',
        'wp-admin/admin-ajax.php': 'Admin AJAX endpoint exposed (normal but worth noting).',
    }

    async def detect(self, session, url, parsed_url, html, headers):
        findings = []
        for path, desc in self.ENDPOINTS.items():
            full = url.rstrip('/') + '/' + path
            status, _, _ = await session.get(full)
            if status == 200:
                sev = 'medium' if 'users' in path else 'low'
                findings.append(Finding(
                    "Exposed Endpoints",
                    sev,
                    f"Endpoint {path} is publicly accessible: {desc}",
                    "Disable XML-RPC if not needed, restrict REST API, and block user enumeration."
                ))
            elif status in (405, 401, 403):
                # Still exposed but not fully accessible
                if path == 'xmlrpc.php':
                    findings.append(Finding(
                        "Exposed Endpoints",
                        "low",
                        "xmlrpc.php exists but access is restricted.",
                        "Consider disabling completely via plugin or firewall rule."
                    ))
        return findings