from pypdf import PdfReader
from pathlib import Path
import re

# Archivos a buscar
archivos_revisar = [
    r"data\classified\Presupuesto\e-SIDIF - Presupuesto - Aspectos generales.pdf",
    r"data\classified\Contabilidad\Cierre Contable.pdf",
    r"data\classified\Contabilidad\Guía de Ayuda para el usuario – Reportes y Estados Contables.pdf",
]

print("=" * 80)
print("BÚSQUEDA: PLANES DE CUENTAS / CHART OF ACCOUNTS")
print("=" * 80)

keywords = {
    "plan de cuenta": [],
    "catálogo de cuenta": [],
    "chart of account": [],
    "estructura contable": [],
    "cuenta contable": [],
    "clasificador contable": []
}

for archivo_path in archivos_revisar:
    path = Path(archivo_path)

    if not path.exists():
        print(f"\n❌ No encontrado: {path.name}")
        continue

    print(f"\n📄 Analizando: {path.name}")

    try:
        with open(path, 'rb') as f:
            reader = PdfReader(f)
            print(f"   Total páginas: {len(reader.pages)}")

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text().lower()

                for keyword in keywords.keys():
                    if keyword in text:
                        keywords[keyword].append((path.name, page_num + 1))

    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("RESULTADOS")
print("=" * 80)

encontrado = False
for keyword, matches in keywords.items():
    if matches:
        encontrado = True
        print(f"\n✅ {keyword.upper()}:")
        for archivo, pagina in matches:
            print(f"   - {archivo} (página {pagina})")

if not encontrado:
    print("\n⚠️ NO se encontraron referencias directas a Planes de Cuentas en los PDFs analizados")
    print("\nPróximo paso: Verificar en documento 'Inicio de Ejercicio - Presupuesto'")
