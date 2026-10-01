from esidif_crawler.catalog import (
    _decode_pdf_escapes,
    _first_text_title,
    _normalize_title,
    _title_is_good,
    choose_title,
    infer_document_type,
    infer_section,
    infer_year,
)


def test_first_text_title_prefers_short_heading():
    text = "\n\nMANUAL DE USUARIO\n\nEste documento describe el procedimiento completo."
    assert _first_text_title(text) == "MANUAL DE USUARIO"


def test_choose_title_rejects_bad_pdf_metadata():
    row = (
        "https://example.test/a.pdf",
        "https://example.test/a.pdf",
        "https://example.test/page",
        "Título de página",
        "Enlace",
        "Pagos",
        "application/pdf",
        ".pdf",
        "manual.pdf",
        100,
        "abc",
        "2026",
        "2026",
        "downloaded",
        "data/manual.pdf",
    )
    columns = [
        "url", "canonical_url", "source_url", "title", "anchor_text", "module",
        "mime_type", "extension", "filename", "size_bytes", "sha256",
        "first_seen", "last_seen", "status", "local_path",
    ]
    title, source = choose_title(
        row,
        columns,
        {"pdf_title": "1", "first_page_title": "Manual de usuario"},
    )
    assert title == "Manual de usuario"
    assert source == "first_page"


def test_decode_legacy_pdf_octal_escapes():
    assert _decode_pdf_escapes(r"Gu\355a para el usuario versi\363n") == "Guía para el usuario versión"


def test_normalize_word_title():
    title = "(Microsoft Word - Gu\355a para el usuario.doc)"
    assert _normalize_title(title) == "Guía para el usuario"
    assert _title_is_good(title)


def test_infer_section():
    url = "https://www.argentina.gob.ar/economia/sechacienda/dgsiaf/e-sidif/formulacion-presupuestaria"
    assert infer_section(url) == "Formulación presupuestaria"


def test_infer_document_type():
    assert infer_document_type("e-SIDIF - Guía de ayuda para usuarios") == "Guía"
    assert infer_document_type("Inicio de Ejercicio - Generalidades.pptx") == "Presentación"


def test_infer_year():
    assert infer_year("dgsiaf-2021_esidif_guia.pdf") == 2021
    assert infer_year("documento-sin-fecha.pdf") is None
