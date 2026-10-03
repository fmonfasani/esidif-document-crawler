from pypdf import PdfReader
from pathlib import Path

pdf_path = Path(r"data\classified\Formulación presupuestaria\Guía para el ususario FOP versión pto preliminar.pdf")

print("=" * 80)
print("EXTRACCIÓN DETALLADA: PÁGINAS CLAVE SOBRE IMPORTACIÓN Y ESTRUCTURA")
print("=" * 80)

with open(pdf_path, 'rb') as f:
    reader = PdfReader(f)

    # Páginas clave:
    # 10-15: Estructura y modalidad de incorporación de datos
    # 29: Objeto de gasto
    # 33: Clasificadores

    paginas_clave = [10, 11, 12, 13, 14, 15, 29, 33]

    for page_num in paginas_clave:
        if page_num <= len(reader.pages):
            page = reader.pages[page_num - 1]
            text = page.extract_text()

            print(f"\n{'=' * 80}")
            print(f"PÁGINA {page_num}")
            print(f"{'=' * 80}\n")
            print(text)
            print("\n")
