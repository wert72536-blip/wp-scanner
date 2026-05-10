import asyncio
import logging
from utils.http import RateLimitedSession
from utils.helpers import normalize_url, get_domain
from detectors import detector_classes
from reporting.report import generate_report

logger = logging.getLogger(__name__)

async def run_scan(target_url: str, output_file: str = None, delay: float = 0.5):
    url = normalize_url(target_url)
    logger.info(f"Starting scan for {url}")

    async with RateLimitedSession(delay=delay) as session:
        # Fetch homepage
        status, html, headers = await session.get(url)
        if status == 0:
            logger.error("Failed to fetch homepage.")
            return None

        from urllib.parse import urlparse
        parsed = urlparse(url)

        # Instantiate all detectors
        detectors = [cls() for cls in detector_classes]
        all_findings = []

        # Run each detector concurrently (they may issue own requests)
        tasks = []
        for det in detectors:
            tasks.append(det.detect(session, url, parsed, html, headers))
        results = await asyncio.gather(*tasks)
        for findings_list in results:
            all_findings.extend(findings_list)

    report = generate_report(url, all_findings)
    if output_file:
        import json
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Report saved to {output_file}")
    return report