from pypdf import PdfReader
from pathlib import Path
import re
from collections import defaultdict

presupuesto_dirs = [
    r"data\classified\Presupuesto",
    r"data\classified\Formulación presupuestaria",
    r"data\classified\Modificacion presupuestaria y programacion de la ejecucion mppe",
    r"data\classified\Programacion de la ejecucion fisica pef",
    r"data\classified\Programacion plurianual de gastos de inversion ppgi",
    r"data\classified\Contabilidad"
]

# Patrones REALES para automatización
patrones_automatizables = {
    "plantillas": r"plantilla|template",
    "importar": r"importar|import|carga|upload|subir|cargar",
    "excel": r"excel|xls|xlsx",
    "csv": r"csv|delimitado",
    "xml": r"xml",
    "archivo": r"archivo|fichero|file",
    "formato": r"formato|estructura|campos|columnas",
    "datos_entrada": r"datos de entrada|ingreso de datos|carga de datos",
    "sincronizacion": r"sincroniz|alineacion|consistencia",
    "validacion_automatica": r"valida automatica|validacion automatica",
    "campo_obligatorio": r"campo obligatorio|campo requerido|campo mandatorio"
}

print("=" * 80)
print("BUSQUEDA: ELEMENTOS AUTOMATIZABLES EN PRESUPUESTO Y CUENTAS")
print("=" * 80)

resultados = defaultdict(lambda: defaultdict(list))
archivos_procesados = 0

for dir_path in presupuesto_dirs:
    path = Path(dir_path)
    if not path.exists():
        continue

    pdf_files = list(path.glob("*.pdf"))

    for pdf_file in pdf_files:
        archivos_procesados += 1
        try:
            with open(pdf_file, 'rb') as f:
                pdf_reader = PdfReader(f)

                for page_idx in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_idx]
                    text = page.extract_text().lower()

                    for patron_nombre, patron_regex in patrones_automatizables.items():
                        if re.search(patron_regex, text):
                            resultados[pdf_file.name][patron_nombre].append((page_idx + 1, text[:200]))

        except:
            pass

print(f"\nArchivos analizados: {archivos_procesados}")
print(f"Archivos con elementos automatizables: {len(resultados)}\n")

# RESULTADOS
if resultados:
    print("\nARCHIVOS CON ELEMENTOS AUTOMATIZABLES:")
    print("=" * 80)

    for archivo in sorted(resultados.keys()):
        elementos = resultados[archivo]
        print(f"\n{archivo}")

        for elemento in sorted(elementos.keys()):
            ocurrencias = elementos[elemento]
            paginas = list(set([p[0] for p in ocurrencias]))
            print(f"  {elemento}: paginas {sorted(paginas)}")

print("\n" + "=" * 80)
print("RESUMEN DE AUTOMATIZABLES")
print("=" * 80)

elemento_counts = defaultdict(int)
for archivo in resultados:
    for elemento in resultados[archivo]:
        elemento_counts[elemento] += 1

if elemento_counts:
    print("\nElementos encontrados:")
    for elemento in sorted(elemento_counts.keys(), key=lambda x: elemento_counts[x], reverse=True):
        print(f"  {elemento}: {elemento_counts[elemento]} archivos")
else:
    print("\nNO se encontraron elementos tipicamente automatizables")
    print("(plantillas, formatos de archivo, importación, etc.)")
