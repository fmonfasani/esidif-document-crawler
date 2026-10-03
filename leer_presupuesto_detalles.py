from pypdf import PdfReader
from pathlib import Path

# Archivos y páginas específicas a revisar para "web service"
archivos_revisar = [
    (r"data\classified\Programacion plurianual de gastos de inversion ppgi\Comprobante de Programacion Plurianual de Gastos de Inversion - PPGI.pdf", [3, 9, 12, 13, 19, 20, 24, 26]),
    (r"data\classified\Formulación presupuestaria\Guía para el ususario FOP versión pto preliminar.pdf", [15]),
    (r"data\classified\Presupuesto\e-SIDIF - Presupuesto - Aspectos generales.pdf", [14]),
    (r"data\classified\Presupuesto\e-SIDIF - Validación BAPIN - Guía de ayuda para usuarios.pdf", [5, 7, 11, 26])  # Muestra del documento
]

print("=" * 80)
print("LECTURA DETALLADA: REFERENCIAS A 'WEB SERVICE' EN PRESUPUESTO")
print("=" * 80)

for archivo_path, paginas in archivos_revisar:
    path = Path(archivo_path)

    if not path.exists():
        print(f"\nARCHIVO NO ENCONTRADO: {path.name}")
        continue

    print(f"\n\n{'=' * 80}")
    print(f"ARCHIVO: {path.name}")
    print(f"{'=' * 80}")

    try:
        with open(path, 'rb') as f:
            pdf_reader = PdfReader(f)

            for page_num in paginas:
                if page_num <= len(pdf_reader.pages):
                    page = pdf_reader.pages[page_num - 1]
                    text = page.extract_text()

                    print(f"\n>>> PAGINA {page_num}")
                    print("-" * 60)

                    # Buscar líneas con "web service"
                    lines = text.split('\n')
                    encontrado = False

                    for line in lines:
                        if 'web' in line.lower() and 'service' in line.lower():
                            print(line.strip())
                            encontrado = True
                        elif 'web' in line.lower():
                            print(line.strip())
                            encontrado = True

                    if not encontrado:
                        print("[Sin mención explícita de web service en esta página]")
                        print(f"\nPrimeras líneas de la página:")
                        for line in lines[:10]:
                            if line.strip():
                                print(line.strip())

    except Exception as e:
        print(f"ERROR: {e}")

print("\n\n" + "=" * 80)
print("FIN DE LECTURA DETALLADA")
print("=" * 80)
