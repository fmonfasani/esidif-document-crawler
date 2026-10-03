from pypdf import PdfReader
from pathlib import Path

pdf_path = Path(r"data\classified\Contabilidad\Guía de Ayuda para el usuario – Reportes y Estados Contables.pdf")

print("=" * 80)
print("EXTRACCIÓN: PLANES DE CUENTAS - REPORTES Y ESTADOS CONTABLES")
print("=" * 80)

with open(pdf_path, 'rb') as f:
    reader = PdfReader(f)

    # Páginas que hablan sobre planes/cuentas contables
    paginas_clave = [2, 5, 7, 8, 9, 13, 14, 15, 16, 17]

    for page_num in paginas_clave:
        if page_num <= len(reader.pages):
            page = reader.pages[page_num - 1]
            text = page.extract_text()

            print(f"\n{'=' * 80}")
            print(f"PÁGINA {page_num}")
            print(f"{'=' * 80}\n")
            print(text)
            print("\n")
