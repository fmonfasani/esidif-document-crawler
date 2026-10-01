import hashlib
import json
import sqlite3
from pathlib import Path
from .models import DocumentRecord

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
 id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE NOT NULL, canonical_url TEXT NOT NULL,
 source_url TEXT NOT NULL, title TEXT, anchor_text TEXT, module TEXT, mime_type TEXT,
 extension TEXT, filename TEXT, size_bytes INTEGER, sha256 TEXT, first_seen TEXT NOT NULL,
 last_seen TEXT NOT NULL, status TEXT NOT NULL, local_path TEXT
);
CREATE INDEX IF NOT EXISTS idx_documents_sha256 ON documents(sha256);
CREATE INDEX IF NOT EXISTS idx_documents_module ON documents(module);
"""

class Storage:
    def __init__(self, db_path: str):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.executescript(SCHEMA)
    def upsert(self, record: DocumentRecord) -> None:
        self.conn.execute("""INSERT INTO documents
        (url,canonical_url,source_url,title,anchor_text,module,mime_type,extension,filename,size_bytes,sha256,first_seen,last_seen,status,local_path)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(url) DO UPDATE SET
        canonical_url=excluded.canonical_url, source_url=excluded.source_url, title=excluded.title,
        anchor_text=excluded.anchor_text, module=excluded.module, mime_type=excluded.mime_type,
        extension=excluded.extension, filename=excluded.filename, size_bytes=excluded.size_bytes,
        sha256=excluded.sha256, last_seen=excluded.last_seen, status=excluded.status, local_path=excluded.local_path""",
        (record.url,record.canonical_url,record.source_url,record.title,record.anchor_text,record.module,record.mime_type,record.extension,record.filename,record.size_bytes,record.sha256,record.first_seen.isoformat(),record.last_seen.isoformat(),record.status,record.local_path))
        self.conn.commit()
    def close(self):
        self.conn.close()

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def export_manifest(storage: Storage, output: str) -> int:
    rows = storage.conn.execute("SELECT * FROM documents ORDER BY module, title").fetchall()
    columns = [d[0] for d in storage.conn.execute("SELECT * FROM documents LIMIT 0").description]
    records = [dict(zip(columns, row)) for row in rows]
    path = Path(output); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(records)
