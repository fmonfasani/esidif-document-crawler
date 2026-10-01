from __future__ import annotations

import csv
import json
import re
import sqlite3
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def _clean(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


_SECTION_NAMES = {
    "administracion-de-permisos": "Administración de permisos",
    "bandeja-de-firmas": "Bandeja de firmas",
    "compras-y-gastos": "Compras y gastos",
    "conciliacion-bancaria": "Conciliación bancaria",
    "contabilidad": "Contabilidad",
    "deducciones-y-retenciones": "Deducciones y retenciones",
    "entes": "Entes",
    "fondos-rotatorios": "Fondos rotatorios",
    "ingresos-y-pagos-extraordinarios": "Ingresos y pagos extraordinarios",
    "inicio-de-ejercicio": "Inicio de ejercicio",
    "medidas-de-afectacion-patrimonial": "Medidas de afectación patrimonial",
    "pagos": "Pagos",
    "presupuesto": "Presupuesto",
    "programacion-financiera-trimestral": "Programación financiera trimestral",
    "recaudacion-internet-erecauda": "Recaudación Internet (eRECAUDA)",
    "recursos": "Recursos",
    "recursos-saf": "Recursos SAF",
    "unidades-descentralizadas": "Unidades descentralizadas",
    "formulacion-presupuestaria": "Formulación presupuestaria",
    "usabilidad-general": "Usabilidad general",
}

def _decode_pdf_escapes(value: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return bytes([int(match.group(1), 8)]).decode("cp1252", errors="replace")
    return re.sub(r"\\([0-7]{3})", replace, value)

def _normalize_title(value: str | None) -> str:
    value = _decode_pdf_escapes(_clean(value))
    value = re.sub(r"^\((?:Microsoft Word|Microsoft PowerPoint)\s*-\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\)\s*$", "", value)
    value = re.sub(r"\s+Página\s+\d+\s+de\s+\d+\s*$", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\.(?:docx?|pptx?)\s*$", "", value, flags=re.IGNORECASE)
    return _clean(value)

def _title_is_good(value: str | None) -> bool:
    title = _normalize_title(value)
    if len(title) < 8 or re.fullmatch(r"[\d\W_]+", title):
        return False
    lowered = title.casefold()
    return not any(x in lowered for x in ("microsoft word", "microsoft powerpoint"))

def infer_section(source_url: str | None) -> str:
    path = unquote(urlparse(source_url or "").path)
    marker = "/e-sidif/"
    if marker not in path.lower():
        return "Sin sección identificada"
    slug = path.lower().split(marker, 1)[1].split("/", 1)[0]
    return _SECTION_NAMES.get(slug, re.sub(r"[-_]+", " ", slug).capitalize())

def infer_document_type(*values: str | None) -> str:
    def ascii_fold(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value)
        return "".join(
            char for char in normalized if not unicodedata.combining(char)
        ).casefold()

    raw_text = " ".join(value or "" for value in values)
    text = " ".join(
        ascii_fold(_normalize_title(value))
        for value in values
        if value
    )

    raw_text_folded = ascii_fold(raw_text)

    if "guia" in text or "manual" in text:
        return "\u0047u\u00eda"

    if "procedimiento" in text:
        return "Procedimiento"

    if "instructivo" in text or "instructiva" in text:
        return "Instructivo"

    if "formulario" in text:
        return "Formulario"

    if "presentacion" in text or ".ppt" in raw_text_folded:
        return "Presentaci\u00f3n"

    if "documento tecnico" in text:
        return "Documento t\u00e9cnico"

    if "boletin" in text:
        return "Bolet\u00edn"

    return "Otro"


def infer_year(*values: str | None) -> int | None:
    for value in values:
        text = value or ""
        match = re.search(r"(?<!\d)((?:19|20)\d{2})(?!\d)", text)
        if match:
            return int(match.group(1))
    return None


def title_quality(title: str, source: str) -> str:
    if source in {"first_page", "link_text"} and _title_is_good(title):
        return "alta"
    if _title_is_good(title):
        return "media"
    return "baja"


def _first_text_title(text: str) -> str:
    lines = [_normalize_title(line) for line in text.splitlines()]
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
            result["pdf_title"] = _normalize_title(str(metadata.title or ""))
            result["pdf_author"] = _clean(str(metadata.author or ""))
            result["pdf_subject"] = _clean(str(metadata.subject or ""))
            result["pdf_creator"] = _clean(str(metadata.creator or ""))
        if reader.pages:
            text = reader.pages[0].extract_text() or ""
            result["text_extractable"] = bool(_clean(text))
            result["first_page_title"] = _first_text_title(text)
    except (OSError, PdfReadError, ValueError, TypeError) as exc:
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
        value = _normalize_title(value)
        if value and _title_is_good(value):
            return value, source
    for source, value in candidates:
        value = _normalize_title(value)
        if value:
            return value, source
    return "Sin título identificado", "fallback"


def build_catalog(db_path: str, output_dir: str) -> dict[str, int]:
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    try:
        rows = db.execute("SELECT * FROM documents ORDER BY title, filename").fetchall()
    finally:
        db.close()

    columns = list(rows[0].keys()) if rows else []
    records = []
    by_section: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        metadata = extract_pdf_metadata(row["local_path"])
        title, title_source = choose_title(row, columns, metadata)
        item = dict(row)
        item.update(metadata)
        item["catalog_title"] = title
        item["title_source"] = title_source
        item["title_quality"] = title_quality(title, title_source)
        item["section"] = infer_section(item.get("source_url"))
        item["document_type"] = infer_document_type(title, item.get("filename"), item.get("anchor_text"), item.get("title"))
        item["year"] = infer_year(item.get("filename"), title, item.get("source_url"))
        records.append(item)
        by_section[item["section"]].append(item)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "esidif_catalog.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = ["# Catálogo documental e-SIDIF", "", f"Documentos: {len(records)}", ""]
    for section in sorted(by_section, key=str.casefold):
        items = sorted(by_section[section], key=lambda x: x["catalog_title"].casefold())
        lines.extend([f"## {section}", ""])
        for item in items:
            lines.extend([
                f"### {item['catalog_title']}",
                f"- Tipo: {item['document_type']}",
                f"- Año: {item['year'] or 'N/D'}",
                f"- Calidad del título: {item['title_quality']}",
                f"- Archivo: {item.get('filename') or ''}",
                f"- URL: {item.get('url') or ''}",
                f"- Fuente: {item.get('source_url') or ''}",
                f"- Título detectado desde: {item['title_source']}",
                f"- Páginas: {item.get('page_count') if item.get('page_count') is not None else 'N/D'}",
                f"- SHA-256: {item.get('sha256') or ''}",
                "",
            ])

    (out / "esidif_catalog.md").write_text("\n".join(lines), encoding="utf-8")

    csv_path = out / "esidif_catalog.csv"
    csv_columns = [
        "catalog_title", "title_quality", "title_source", "section", "document_type", "year",
        "module", "filename", "url", "source_url", "mime_type", "size_bytes", "sha256",
        "local_path", "page_count", "pdf_title", "pdf_author", "pdf_subject", "pdf_creator",
        "first_page_title", "text_extractable", "metadata_error",
    ]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    section_dir = out / "by_section"
    section_dir.mkdir(exist_ok=True)
    for section, items in by_section.items():
        slug = re.sub(r"[^a-z0-9]+", "-", section.casefold()).strip("-") or "sin-seccion"
        section_lines = [f"# {section}", "", f"Documentos: {len(items)}", ""]
        for item in sorted(items, key=lambda x: x["catalog_title"].casefold()):
            section_lines.extend([
                f"## {item['catalog_title']}",
                f"- Tipo: {item['document_type']}",
                f"- Año: {item['year'] or 'N/D'}",
                f"- Archivo: {item.get('filename') or ''}",
                f"- URL: {item.get('url') or ''}",
                "",
            ])
        (section_dir / f"{slug}.md").write_text("\n".join(section_lines), encoding="utf-8")

    stats = {
        "documents": len(records),
        "sections": len(by_section),
        "document_types": dict(sorted(Counter(item["document_type"] for item in records).items())),
        "title_quality": dict(sorted(Counter(item["title_quality"] for item in records).items())),
        "years": dict(sorted(Counter(str(item["year"]) if item["year"] else "N/D" for item in records).items())),
    }
    (out / "statistics.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "documents": len(records),
        "sections": len(by_section),
        "metadata_errors": sum(bool(item.get("metadata_error")) for item in records),
        "text_extractable": sum(bool(item.get("text_extractable")) for item in records),
    }
