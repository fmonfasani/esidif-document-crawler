from pypdf import PdfReader
from pathlib import Path
import re
from collections import defaultdict

# Buscar en carpetas específicas
presupuesto_dirs = [
    r"data\classified\Presupuesto",
    r"data\classified\Formulación presupuestaria",
    r"data\classified\Modificacion presupuestaria y programacion de la ejecucion mppe",
    r"data\classified\Programacion de la ejecucion fisica pef",
    r"data\classified\Programacion plurianual de gastos de inversion ppgi",
    r"data\classified\Contabilidad"
]

# Patrones a buscar
patrones_clave = {
    "automatizar": r"automatiza|automatico|autom",
    "manual": r"\bmanual",
    "procesos": r"proceso|procedimiento",
    "validacion": r"validacion|validar",
    "restriccion": r"restriccion|no se puede|no es posible|limitacion",
    "integracion": r"integracion|integra|vincula",
    "web service": r"web\s*service|api|endpoint",
    "entrada datos": r"ingreso|entrada|carga de datos|ingresar",
    "consulta": r"consulta|reporte|informe",
    "error": r"error|fallo|problema|inconsistencia"
}

print("=" * 80)
print("ANALISIS: PRESUPUESTO Y PLANES DE CUENTAS")
print("=" * 80)
print()

resultados = defaultdict(lambda: defaultdict(list))

for dir_path in presupuesto_dirs:
    path = Path(dir_path)
    if not path.exists():
        continue

    print(f"\nProcesando: {path.name}")
    print("-" * 60)

    pdf_files = list(path.glob("*.pdf"))
    print(f"PDFs encontrados: {len(pdf_files)}")

    for pdf_file in pdf_files:
        try:
            with open(pdf_file, 'rb') as f:
                pdf_reader = PdfReader(f)
                num_pages = len(pdf_reader.pages)

                for page_idx in range(num_pages):
                    page = pdf_reader.pages[page_idx]
                    text = page.extract_text().lower()

                    for patron_nombre, patron_regex in patrones_clave.items():
                        if re.search(patron_regex, text):
                            resultados[pdf_file.name][patron_nombre].append(page_idx + 1)

        except Exception as e:
            print(f"  Error en {pdf_file.name}: {e}")

# IMPRIMIR RESULTADOS
print("\n" + "=" * 80)
print("PATRONES ENCONTRADOS")
print("=" * 80)

if not resultados:
    print("\nNO SE ENCONTRARON PATRONES CLAVE EN LOS DOCUMENTOS")
else:
    for archivo in sorted(resultados.keys()):
        patrones = resultados[archivo]
        if patrones:
            print(f"\n{archivo}")
            print(f"  Patrones encontrados: {list(patrones.keys())}")
            for patron, paginas in sorted(patrones.items()):
                print(f"    - {patron}: paginas {set(paginas)}")

print("\n" + "=" * 80)
print("RESUMEN")
print("=" * 80)

patron_counts = defaultdict(int)
for archivo in resultados:
    for patron in resultados[archivo]:
        patron_counts[patron] += 1

print("\nOcurrencias de patrones clave:")
for patron in sorted(patron_counts.keys(), key=lambda x: patron_counts[x], reverse=True):
    print(f"  {patron}: {patron_counts[patron]} archivos")

print("\nNOTA: Este script solo identifica PRESENCIA de palabras clave.")
print("Revisar manualmente para entender contexto.")
