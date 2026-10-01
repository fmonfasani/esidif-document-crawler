# e-SIDIF Document Crawler

Crawler documental reproducible para descubrir, inventariar, descargar y validar documentación pública de e-SIDIF.

Principios: HTTP-first, Playwright fallback, provenance, idempotencia, SQLite y manifest JSON.

## Quick start

    python -m venv .venv
    pip install -e ".[dev]"
    playwright install chromium
    python -m esidif_crawler audit
    python -m esidif_crawler crawl --download

Origen: https://www.argentina.gob.ar/economia/sechacienda/dgsiaf/e-sidif/

## Modos

- audit: descubre páginas y documentos sin descargar binarios.
- crawl: descubre y opcionalmente descarga.
- export: exporta el inventario SQLite a JSON.

Los datos generados viven en data/ y están excluidos del control de versiones.

Los documentos descargados siguen perteneciendo a sus titulares y fuentes respectivas.
