from pathlib import Path

import yaml
from pydantic import BaseModel


class SiteConfig(BaseModel):
    root_url: str
    allowed_hosts: list[str]
    allowed_path_prefixes: list[str]
    max_depth: int = 12

class CrawlerConfig(BaseModel):
    user_agent: str
    timeout_seconds: float = 30
    max_retries: int = 4
    concurrency: int = 4
    delay_seconds: float = 0.5
    respect_robots_txt: bool = True

class BrowserConfig(BaseModel):
    enabled: bool = True
    headless: bool = True
    timeout_ms: int = 30000

class StorageConfig(BaseModel):
    data_dir: str = "data"
    database: str = "data/database/esidif.sqlite3"
    documents_dir: str = "data/documents"
    pages_dir: str = "data/pages"
    manifests_dir: str = "data/manifests"

class DiscoveryConfig(BaseModel):
    document_extensions: list[str]
    max_document_size_mb: int = 250

class Config(BaseModel):
    site: SiteConfig
    crawler: CrawlerConfig
    browser: BrowserConfig
    storage: StorageConfig
    discovery: DiscoveryConfig

def load_config(path: str = "config.yaml") -> Config:
    return Config.model_validate(yaml.safe_load(Path(path).read_text(encoding="utf-8")))
