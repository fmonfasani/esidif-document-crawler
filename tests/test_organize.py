from pathlib import Path

from esidif_crawler.organize import _safe_component, _unique_destination


def test_safe_component_removes_windows_invalid_chars():
    assert _safe_component('Título: "Guía"?.pdf', "fallback") == "Título Guía .pdf"


def test_safe_component_handles_empty():
    assert _safe_component("   ", "fallback") == "fallback"


def test_unique_destination(tmp_path: Path):
    first = tmp_path / "Guía.pdf"
    first.write_text("1", encoding="utf-8")
    assert _unique_destination(first).name == "Guía (2).pdf"
