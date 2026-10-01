import asyncio
from collections import deque
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from .config import Config
from .discovery import extract_links, is_allowed, page_title, infer_module
from .http import HttpClient, polite_delay
from .models import DocumentRecord
from .storage import Storage, sha256_bytes

class Crawler:
    def __init__(self, config: Config, download: bool = False):
        self.config=config; self.download=download; self.storage=Storage(config.storage.database)
        self.http=HttpClient(config.crawler.user_agent, config.crawler.timeout_seconds)
        self.seen=set(); self.queue=deque([(config.site.root_url,0,"")])
        Path(config.storage.documents_dir).mkdir(parents=True,exist_ok=True); Path(config.storage.pages_dir).mkdir(parents=True,exist_ok=True)
    async def run(self):
        pages=documents=downloaded=0
        try:
            while self.queue:
                url,depth,source=self.queue.popleft()
                if url in self.seen or depth>self.config.site.max_depth or not is_allowed(url,self.config.site.allowed_hosts,self.config.site.allowed_path_prefixes): continue
                self.seen.add(url); await polite_delay(self.config.crawler.delay_seconds)
                response=await self.http.get(url); content_type=response.headers.get("content-type","").lower()
                if "text/html" not in content_type and not url.endswith("/"):
                    documents+=1
                    if self.download: downloaded+=await self._save_document(url,source,response)
                    continue
                pages+=1; html=response.text
                (Path(self.config.storage.pages_dir)/(sha256_bytes(url.encode())+".html")).write_text(html,encoding="utf-8")
                module=infer_module(html,url); title=page_title(html)
                for link in extract_links(html,url,depth+1,self.config.discovery.document_extensions):
                    if not is_allowed(link.url,self.config.site.allowed_hosts,self.config.site.allowed_path_prefixes): continue
                    if link.is_document:
                        documents+=1
                        if self.download:
                            r=await self.http.get(link.url); downloaded+=await self._save_document(link.url,url,r,title,link.anchor_text,module)
                    elif link.depth<=self.config.site.max_depth: self.queue.append((link.url,link.depth,url))
            return {"pages":pages,"documents":documents,"downloaded":downloaded}
        finally:
            await self.http.close(); self.storage.close()
    async def _save_document(self,url,source,response,title="",anchor_text="",module=""):
        data=response.content
        if len(data)>self.config.discovery.max_document_size_mb*1024*1024: raise ValueError(f"Document exceeds size limit: {url}")
        digest=sha256_bytes(data); filename=Path(urlparse(url).path).name or f"{digest}.bin"
        destination=Path(self.config.storage.documents_dir)/digest[:2]/f"{digest}_{filename}"; destination.parent.mkdir(parents=True,exist_ok=True); destination.write_bytes(data)
        self.storage.upsert(DocumentRecord(url=url,canonical_url=str(response.url),source_url=source,title=title,anchor_text=anchor_text,module=module,mime_type=response.headers.get("content-type","").split(";")[0],extension=Path(filename).suffix.lower(),filename=filename,size_bytes=len(data),sha256=digest,last_seen=datetime.utcnow(),status="downloaded",local_path=str(destination)))
        return 1
