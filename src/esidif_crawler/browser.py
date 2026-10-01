from playwright.async_api import async_playwright


class BrowserFallback:
    def __init__(self, user_agent: str, timeout_ms: int = 30000, headless: bool = True):
        self.user_agent=user_agent; self.timeout_ms=timeout_ms; self.headless=headless
        self._pw=None; self._browser=None
    async def __aenter__(self):
        self._pw=await async_playwright().start()
        self._browser=await self._pw.chromium.launch(headless=self.headless)
        return self
    async def __aexit__(self,*args):
        if self._browser: await self._browser.close()
        if self._pw: await self._pw.stop()
    async def fetch_html(self,url: str) -> str:
        page=await self._browser.new_page(user_agent=self.user_agent)
        try:
            await page.goto(url,wait_until="networkidle",timeout=self.timeout_ms)
            return await page.content()
        finally:
            await page.close()
