from collections import deque
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

from .browser import BrowserFallback
from .config import Config
from .discovery import extract_links, infer_module, is_allowed_document, is_allowed_page, page_title
from .http import HttpClient, polite_delay
from .models import DocumentRecord
from .storage import Storage, sha256_bytes


class Crawler:
    def __init__(self, config: Config, download: bool = False):
        self.config=config; self.download=download
        self.storage=Storage(config.storage.database)
        self.http=HttpClient(config.crawler.user_agent, config.crawler.timeout_seconds)
        self.seen=set(); self.queue=deque([(config.site.root_url,0,"")])
        Path(config.storage.documents_dir).mkdir(parents=True,exist_ok=True)
        Path(config.storage.pages_dir).mkdir(parents=True,exist_ok=True)

    async def run(self):
        pages=documents=downloaded=0
        browser=None
        try:
            while self.queue:
                url,depth,_source=self.queue.popleft()
                if url in self.seen or depth>self.config.site.max_depth: continue
                if not is_allowed_page(url,self.config.site.allowed_hosts,self.config.site.allowed_path_prefixes): continue
                self.seen.add(url); await polite_delay(self.config.crawler.delay_seconds)
                try:
                    response=await self.http.get(url)
                    content_type=response.headers.get("content-type","").lower()
                    if "text/html" not in content_type:
                        continue
                    html=response.text
                except Exception:
                    if not self.config.browser.enabled: raise
                    if browser is None:
                        browser=BrowserFallback(self.config.crawler.user_agent,self.config.browser.timeout_ms,self.config.browser.headless)
                        await browser.__aenter__()
                    html=await browser.fetch_html(url)

                pages+=1
                (Path(self.config.storage.pages_dir)/(sha256_bytes(url.encode())+".html")).write_text(html,encoding="utf-8")
                module=infer_module(html,url); title=page_title(html)
                for link in extract_links(html,url,depth+1,self.config.discovery.document_extensions):
                    if link.is_document:
                        if not is_allowed_document(link.url,self.config.site.allowed_hosts): continue
                        documents+=1
                        if self.download:
                            r=await self.http.get(link.url)
                            downloaded+=await self._save_document(link.url,url,r,title,link.anchor_text,module)
                        else:
                            self.storage.upsert(DocumentRecord(
                                url=link.url,canonical_url=link.url,source_url=url,title=title,
                                anchor_text=link.anchor_text,module=module,status="discovered",
                                last_seen=datetime.now(UTC)))
                    elif is_allowed_page(link.url,self.config.site.allowed_hosts,self.config.site.allowed_path_prefixes) and link.depth<=self.config.site.max_depth:
                        self.queue.append((link.url,link.depth,url))
            return {"pages":pages,"documents":documents,"downloaded":downloaded}
        finally:
            if browser: await browser.__aexit__(None,None,None)
            await self.http.close(); self.storage.close()

    async def _save_document(self,url,source,response,title="",anchor_text="",module=""):
        data=response.content
        if len(data)>self.config.discovery.max_document_size_mb*1024*1024:
            raise ValueError(f"Document exceeds size limit: {url}")
        digest=sha256_bytes(data)
        filename=Path(urlparse(url).path).name or f"{digest}.bin"
        destination=Path(self.config.storage.documents_dir)/digest[:2]/f"{digest}_{filename}"
        destination.parent.mkdir(parents=True,exist_ok=True); destination.write_bytes(data)
        self.storage.upsert(DocumentRecord(
            url=url,canonical_url=str(response.url),source_url=source,title=title,
            anchor_text=anchor_text,module=module,
            mime_type=response.headers.get("content-type","").split(";")[0],
            extension=Path(filename).suffix.lower(),filename=filename,size_bytes=len(data),
            sha256=digest,last_seen=datetime.now(UTC),status="downloaded",
            local_path=str(destination)))
        return 1
