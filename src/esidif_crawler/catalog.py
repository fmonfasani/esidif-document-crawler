from __future__ import annotations

import csv
import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any

from pypdf import PdfReader


def _clean(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def _first_text_title(text: str) -> str:
    lines = [_clean(line) for line in text.splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return ""
    candidates = []
    for line in lines[:40]:
        if 3 <= len(line) <= 180 and len(line.split()) <= 24:
            candidates.append(line)
    return candidates[0] if candidates else lines[0][:180]


def extract_pdf_metadata(path: str | None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "pdf_title": "",
        "pdf_author": "",
        "pdf_subject": "",
        "pdf_creator": "",
        "first_page_title": "",
        "text_extractable": False,
        "page_count": None,
        "metadata_error": "",
    }
    if not path or not Path(path).exists():
        result["metadata_error"] = "local_file_not_found"
        return result
    try:
        reader = PdfReader(path)
        result["page_count"] = len(reader.pages)
        metadata = reader.metadata
        if metadata:
            result["pdf_title"] = _clean(str(metadata.title or ""))
            result["pdf_author"] = _clean(str(metadata.author or ""))
            result["pdf_subject"] = _clean(str(metadata.subject or ""))
            result["pdf_creator"] = _clean(str(metadata.creator or ""))
        if reader.pages:
            text = reader.pages[0].extract_text() or ""
            result["text_extractable"] = bool(_clean(text))
            result["first_page_title"] = _first_text_title(text)
    except Exception as exc:
        result["metadata_error"] = type(exc).__name__
    return result


def choose_title(row: sqlite3.Row | tuple, columns: list[str], metadata: dict[str, Any]) -> tuple[str, str]:
    record = dict(zip(columns, row))
    candidates = [
        ("pdf_metadata", metadata.get("pdf_title", "")),
        ("first_page", metadata.get("first_page_title", "")),
        ("link_text", record.get("anchor_text", "")),
        ("page_title", record.get("title", "")),
        ("filename", Path(record.get("filename", "")).stem),
    ]
    for source, value in candidates:
        value = _clean(value)
        if value:
            return value, source
    return "Sin título identificado", "fallback"


def build_catalog(db_path: str, output_dir: str) -> dict[str, int]:
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    try:
        rows = db.execute("SELECT * FROM documents ORDER BY module, title, filename").fetchall()
    finally:
        db.close()

    columns = list(rows[0].keys()) if rows else []
    records = []
    by_module: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        metadata = extract_pdf_metadata(row["local_path"])
        title, title_source = choose_title(row, columns, metadata)
        item = dict(row)
        item.update(metadata)
        item["catalog_title"] = title
        item["title_source"] = title_source
        records.append(item)
        by_module[item.get("module") or "Sin módulo identificado"].append(item)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "esidif_catalog.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = ["# Catálogo documental e-SIDIF", "", f"Documentos: {len(records)}", ""]
    for module in sorted(by_module, key=str.casefold):
        items = sorted(by_module[module], key=lambda x: x["catalog_title"].casefold())
        lines.extend([f"## {module}", ""])
        for item in items:
            lines.extend([
                f"### {item['catalog_title']}",
                f"- Archivo: \`{item.get('filename') or ''}\`",
                f"- URL: {item.get('url') or ''}",
                f"- Fuente: {item.get('source_url') or ''}",
                f"- Título detectado desde: \`{item['title_source']}\`",
                f"- Páginas: {item.get('page_count') if item.get('page_count') is not None else 'N/D'}",
                f"- SHA-256: \`{item.get('sha256') or ''}\`",
                "",
            ])

    (out / "esidif_catalog.md").write_text("\n".join(lines), encoding="utf-8")

    csv_path = out / "esidif_catalog.csv"
    csv_columns = [
        "catalog_title", "title_source", "module", "filename", "url", "source_url",
        "mime_type", "size_bytes", "sha256", "local_path", "page_count",
        "pdf_title", "pdf_author", "pdf_subject", "pdf_creator",
        "first_page_title", "text_extractable", "metadata_error",
    ]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    return {
        "documents": len(records),
        "modules": len(by_module),
        "metadata_errors": sum(bool(item.get("metadata_error")) for item in records),
        "text_extractable": sum(bool(item.get("text_extractable")) for item in records),
    }
