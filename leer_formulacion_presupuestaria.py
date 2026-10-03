from pypdf import PdfReader
from pathlib import Path
import re

# PDF a analizar
pdf_path = Path(r"data\classified\Formulación presupuestaria\Guía para el ususario FOP versión pto preliminar.pdf")

if not pdf_path.exists():
    print(f"Archivo no encontrado: {pdf_path}")
else:
    print("=" * 80)
    print("LECTURA MANUAL: GUÍA PARA USUARIO FOP - FORMULACIÓN PRESUPUESTARIA")
    print("=" * 80)

    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        print(f"\nTotal de páginas: {len(reader.pages)}\n")

        # Buscar palabras clave relacionadas con:
        # - Plantillas
        # - Formatos
        # - Campos obligatorios
        # - Importación
        # - Estructura de datos

        keywords = {
            "plantilla": [],
            "formato": [],
            "campo obligatorio": [],
            "campo requerido": [],
            "importar": [],
            "archivo": [],
            "excel": [],
            "csv": [],
            "xml": [],
            "estructura": [],
            "datos": [],
            "validación": [],
            "restricción": [],
            "incisos": [],
            "clasificador": [],
            "categoría programática": [],
            "objeto de gasto": []
        }

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text().lower()

            for keyword in keywords.keys():
                if keyword in text:
                    keywords[keyword].append(page_num + 1)

        # Mostrar en qué páginas aparecen las palabras clave
        print("PALABRAS CLAVE ENCONTRADAS:")
        print("-" * 80)
        for keyword, pages in keywords.items():
            if pages:
                print(f"\n{keyword.upper()}: páginas {sorted(set(pages))}")

        print("\n" + "=" * 80)
        print("EXTRAYENDO CONTENIDO DE PÁGINAS CLAVE...")
        print("=" * 80)

        # Extraer las primeras 5 páginas completas para análisis manual
        for page_num in range(min(5, len(reader.pages))):
            page = reader.pages[page_num]
            text = page.extract_text()

            print(f"\n{'=' * 80}")
            print(f"PÁGINA {page_num + 1}")
            print(f"{'=' * 80}")
            print(text[:1500])  # Primeros 1500 caracteres
            print("\n[... contenido continuado ...]")
