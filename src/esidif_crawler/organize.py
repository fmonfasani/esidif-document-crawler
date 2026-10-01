from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any


_INVALID_WINDOWS_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_RESERVED_WINDOWS_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def _safe_component(value: str, fallback: str) -> str:
    value = (value or "").strip()
    value = _INVALID_WINDOWS_CHARS.sub(" ", value)
    value = re.sub(r"\s+", " ", value).strip(" .")
    if not value:
        return fallback
    if value.upper() in _RESERVED_WINDOWS_NAMES:
        value = f"_{value}"
    return value[:180].rstrip(" .") or fallback


def _unique_destination(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    counter = 2
    while True:
        candidate = path.with_name(f"{stem} ({counter}){suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize_catalog(
    catalog_path: str = "data/catalog/esidif_catalog.json",
    output_dir: str = "data/classified",
    mode: str = "copy",
) -> dict[str, Any]:
    catalog = Path(catalog_path)
    destination_root = Path(output_dir)

    if not catalog.exists():
        raise FileNotFoundError(f"No existe el catálogo: {catalog}")

    records = json.loads(catalog.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("El catálogo no contiene una lista de documentos")

    if mode not in {"copy", "move"}:
        raise ValueError("mode debe ser 'copy' o 'move'")

    counts: dict[str, int] = {}
    organized = 0
    missing = 0
    errors: list[str] = []

    for record in records:
        if not isinstance(record, dict):
            continue

        source = Path(record.get("local_path") or "")
        if not source.exists():
            missing += 1
            errors.append(f"Archivo no encontrado: {source}")
            continue

        section = _safe_component(
            str(record.get("section") or "Sin clasificación"),
            "Sin clasificación",
        )
        title = _safe_component(
            str(record.get("catalog_title") or ""),
            source.stem,
        )

        # Preserve the original PDF extension.
        extension = source.suffix.lower() or ".pdf"
        destination_dir = destination_root / section
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = _unique_destination(destination_dir / f"{title}{extension}")

        try:
            if mode == "move":
                shutil.move(str(source), str(destination))
            else:
                shutil.copy2(source, destination)
            organized += 1
            counts[section] = counts.get(section, 0) + 1
        except OSError as exc:
            errors.append(f"{source} -> {destination}: {exc}")

    result = {
        "documents": len(records),
        "organized": organized,
        "missing": missing,
        "errors": len(errors),
        "sections": counts,
        "output_dir": str(destination_root),
        "mode": mode,
    }

    report = destination_root / "_organization_report.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if errors:
        error_file = destination_root / "_organization_errors.txt"
        error_file.write_text("\n".join(errors), encoding="utf-8")

    return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Organiza los PDFs del catálogo por clasificación y título."
    )
    parser.add_argument(
        "--catalog",
        default="data/catalog/esidif_catalog.json",
        help="Catálogo JSON generado por el comando catalog.",
    )
    parser.add_argument(
        "--output",
        default="data/classified",
        help="Carpeta raíz de la clasificación.",
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Mueve los PDFs en lugar de copiarlos.",
    )
    args = parser.parse_args()

    result = organize_catalog(
        catalog_path=args.catalog,
        output_dir=args.output,
        mode="move" if args.move else "copy",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
