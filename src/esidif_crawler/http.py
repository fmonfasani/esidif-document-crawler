import asyncio

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


class HttpClient:
    def __init__(self, user_agent: str, timeout: float = 30):
        self.client = httpx.AsyncClient(timeout=timeout, follow_redirects=True, headers={"User-Agent": user_agent, "Accept": "*/*"})
    @retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=0.5, max=8))
    async def get(self, url: str) -> httpx.Response:
        response = await self.client.get(url); response.raise_for_status(); return response
    async def close(self):
        await self.client.aclose()

async def polite_delay(seconds: float):
    if seconds > 0: await asyncio.sleep(seconds)
