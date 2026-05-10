import asyncio
import aiohttp
import logging
import time
from typing import Optional, Tuple
from urllib.parse import urlparse   

logger = logging.getLogger(__name__)

class RateLimitedSession:
    """Manages aiohttp session with per-domain rate limiting."""
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self._last_request: dict[str, float] = {}
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=15),
            headers={'User-Agent': 'WPScanner/2.0 (Security Audit)'}
        )
        return self

    async def __aexit__(self, *args):
        if self._session:
            await self._session.close()

    async def _throttle(self, domain: str):
        now = time.monotonic()
        last = self._last_request.get(domain, 0)
        diff = now - last
        if diff < self.delay:
            await asyncio.sleep(self.delay - diff)
        self._last_request[domain] = time.monotonic()

    async def get(self, url: str, **kwargs) -> Tuple[int, str, dict]:
        domain = urlparse(url).netloc   
        await self._throttle(domain)
        try:
            async with self._session.get(url, **kwargs) as resp:
                body = await resp.text()
                return resp.status, body, dict(resp.headers)
        except Exception as e:
            logger.warning(f"Request failed for {url}: {e}")
            return 0, '', {}