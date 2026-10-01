from esidif_crawler.catalog import _first_text_title, choose_title


def test_first_text_title_prefers_short_heading():
    text = "\n\nMANUAL DE USUARIO\n\nEste documento describe el procedimiento completo."
    assert _first_text_title(text) == "MANUAL DE USUARIO"


def test_choose_title_uses_pdf_metadata_first():
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
    title, source = choose_title(row, columns, {"pdf_title": "Título del PDF"})
    assert title == "Título del PDF"
    assert source == "pdf_metadata"
