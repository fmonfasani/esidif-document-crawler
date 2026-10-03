# MATRIZ DE AUTOMATIZACIÓN
## Presupuesto y Planes de Cuentas para SAP

**Fecha de análisis:** 2026-10-03  
**Basado en:** Documentos oficiales e-SIDIF verificados

---

## RESUMEN EJECUTIVO

```
✅ ALTO POTENCIAL DE AUTOMATIZACIÓN

Funcionalidades confirmadas:
├─ Importación de presupuesto vía Excel
├─ Validación automática de estructura
├─ Extracción de reportes contables
├─ Conciliación presupuesto ↔ contabilidad
└─ Integración con SAP FI/CO (requiere mapeo)

❌ LIMITACIÓN IMPORTANTE:
   └─ No hay web services para e-SIDIF
      → Requiere acceso GUI o RPA
```

---

## 1. AUTOMATIZACIÓN PRESUPUESTARIA

### 1.1 VALIDACIÓN DE TEMPLATES EXCEL

| Aspecto | Detalles |
|--------|----------|
| **Automatizar** | ✅ SÍ |
| **Complejidad** | 🟢 BAJA |
| **Esfuerzo** | 1-2 días |
| **Riesgo** | Bajo |

#### ¿Qué validar?

```python
# Pseudo-código: Validador de Template Excel

def validar_template_presupuesto(archivo_excel, componente):
    errores = []
    
    # 1. Validar que exista la hoja correcta
    if not existe_hoja(archivo_excel, componente):
        errores.append(f"No existe hoja {componente}")
    
    # 2. Validar campos obligatorios
    campos_obligatorios = ["PEX", "BAPIN"]
    for campo in campos_obligatorios:
        if campo not in archivo_excel.columnas:
            errores.append(f"Falta campo obligatorio: {campo}")
    
    # 3. Validar estructura de datos
    for fila in archivo_excel.datos:
        if not validar_pex(fila["PEX"]):
            errores.append(f"PEX inválido: {fila['PEX']}")
        if not validar_bapin(fila["BAPIN"]):
            errores.append(f"BAPIN inválido: {fila['BAPIN']}")
    
    # 4. Reportar resultados
    if errores:
        return {"estado": "RECHAZO", "errores": errores}
    else:
        return {"estado": "APROBADO", "errores": []}
```

#### Deliverables

1. **Validador Python**
   - Función que valida estructura
   - Reporte de errores
   - Archivo de log

2. **Documentación**
   - Qué campos son obligatorios
   - Formatos esperados
   - Ejemplos de archivos válidos

3. **Script de Testing**
   - Tests contra archivos válidos
   - Tests contra archivos inválidos

---

### 1.2 IMPORTACIÓN PRESUPUESTARIA - PREPARACIÓN DE DATOS

| Aspecto | Detalles |
|--------|----------|
| **Automatizar** | ✅ SÍ (parcial) |
| **Complejidad** | 🟡 MEDIA |
| **Esfuerzo** | 3-5 días |
| **Riesgo** | Medio |

#### ¿Qué se puede automatizar?

```
✅ SÍ:
├─ Generar archivos Excel en formato correcto
├─ Transformar datos desde SAP a formato e-SIDIF
├─ Validar datos antes de importar
├─ Aplicar políticas de importación
└─ Logging de importaciones

❌ NO (requiere GUI):
├─ Importación actual (requiere interfaz e-SIDIF)
└─ Selección de escenario (requiere decisión manual)
```

#### Arquitectura de Solución

```
DATOS ENTRADA                 PROCESAMIENTO              SALIDA
(SAP / Excel)                                           (e-SIDIF)
    │                              │                        │
    ├─ CO (Controlling)       ┌────────────────┐        ┌──────────┐
    ├─ FI (Finanzas)          │ ETL Process    │        │ Template │
    └─ PS (Proyectos)         │                │        │ Excel    │
                              │ 1. Validar     │        └──────────┘
                              │ 2. Transformar │
                              │ 3. Mapear      │
                              │ 4. Generar     │
                              └────────────────┘
                                    ↓
                              [Validador]
                                    ↓
                              [Aprobado/Rechazado]
```

#### Opciones de Automatización

**Opción A: Script de Transformación (RECOMENDADO)**

```python
# Transforma datos SAP → Formato e-SIDIF
input_sap = read_from_sap("CO", "presupuesto_2026")
data_transformed = transform_to_esidif(input_sap)
output_excel = write_excel_template(data_transformed)
validate_template(output_excel)  # ✅ Aprobado
```

**Pros:**
- Sin requiere GUI
- Rápido
- Repetible

**Contras:**
- Requiere acceso a datos SAP
- Mapeo inicial de campos

**Opción B: RPA (Robot Process Automation)**

```
┌─────────────────────────────────────────────┐
│           ROBOT RPA (UiPath / AA)          │
├─────────────────────────────────────────────┤
│                                             │
│ 1. Abre navegador → e-SIDIF                │
│ 2. Login automático                        │
│ 3. Navega a Importar Elemento              │
│ 4. Sube archivo Excel                      │
│ 5. Selecciona política de importación      │
│ 6. Ejecuta importación                     │
│ 7. Valida resultado                        │
│ 8. Genera reporte                          │
│                                             │
└─────────────────────────────────────────────┘
```

**Pros:**
- Automatización end-to-end
- No requiere cambios a e-SIDIF

**Contras:**
- Mayor complejidad
- Mantenimiento si e-SIDIF cambia interfaz
- Más lento que API

**Opción C: Híbrida (RECOMENDADO)**

```
┌──────────────────────┐
│ Script Python (ETL)  │  Prepara y valida archivos Excel
└──────────────────────┘
         ↓
┌──────────────────────┐
│ RPA (UiPath)         │  Importa en e-SIDIF automáticamente
└──────────────────────┘
         ↓
┌──────────────────────┐
│ Validador Final      │  Verifica que importación fue correcta
└──────────────────────┘
```

**Beneficios:**
- Python hace el trabajo pesado
- RPA solo hace lo que no se puede automatizar
- Combinación óptima de velocidad y robustez

---

### 1.3 INTEGRACIÓN CON SAP - PRESUPUESTO

| Aspecto | Detalles |
|--------|----------|
| **Automatizar** | ✅ SÍ |
| **Complejidad** | 🔴 ALTA |
| **Esfuerzo** | 2-3 semanas |
| **Riesgo** | Alto |

#### Mapeo Presupuesto SAP → e-SIDIF

```
SAP MODULES                    e-SIDIF PRESUPUESTO
│                              │
├─ CO (Controlling)            ├─ 5 Componentes
│  ├─ Centros de Costo    ───→ Aperturas Programáticas
│  ├─ Órdenes internas   ───→ Proyectos/Actividades
│  ├─ Cuenta Mayor        ───→ Objetos de Gasto (Incisos)
│  └─ Líneas presupuestarias  └─ Crédito
│
├─ FI (Finanzas)              ├─ Plan de Cuentas
│  ├─ Cuentas Mayores    ───→ Clasificador contable
│  └─ Análisis        ───→ Moneda, Jurisdicción
│
└─ PS (Proyectos)            └─ Física de Proyecto
   ├─ Proyecto         ───→ Proyecto presupuestario
   ├─ WBS Items       ───→ Actividades
   └─ Planificación   ───→ Física Proyecto
```

#### Campos a Mapear (Ejemplo Crédito)

| Campo SAP | Campo e-SIDIF | Transformación |
|-----------|--------------|-----------------|
| KOSTL | Aperturas Programáticas | Centro costo → Programa |
| AUFNR | Proyecto | Orden interna → ID Proyecto |
| SAKNR | Objeto de Gasto | Cuenta → Inciso (1-9) |
| WKGBTR | Crédito | Importe presupuestario |
| WAERS | Moneda | USD → 01, ARS → 00 |
| BUKRS | Ente Contable | Sociedad SAP → Ente e-SIDIF |

#### Desafíos

```
1. COMPLEJIDAD DE MAPEO
   └─ Un campo SAP puede mapear a múltiples campos e-SIDIF
   └─ Un campo e-SIDIF puede venir de múltiples campos SAP

2. DATOS INCOMPLETOS
   └─ SAP puede no tener toda información requerida
   └─ Requiere enriquecimiento con datos maestros

3. MÚLTIPLES POLÍTICAS
   └─ Reemplazar vs Acumular
   └─ Presupuesto base vs Modificaciones
   
4. AUDITORÍA
   └─ Rastreo de cambios
   └─ Reconciliación antes/después
```

---

## 2. AUTOMATIZACIÓN CONTABLE (PLANES DE CUENTAS)

### 2.1 EXTRACCIÓN DE REPORTES

| Aspecto | Detalles |
|--------|----------|
| **Automatizar** | ✅ SÍ (parcial) |
| **Complejidad** | 🟡 MEDIA |
| **Esfuerzo** | 1-2 semanas |
| **Riesgo** | Bajo |

#### Opciones

**Opción A: RPA - Extraer vía GUI**

```
Robot:
├─ 1. Login a e-SIDIF
├─ 2. Navega a Reportes → Contabilidad
├─ 3. Balance General
│   ├─ Selecciona año, ente, fecha
│   ├─ Ejecuta
│   └─ Descarga en 4 niveles (Cuenta, SubC1, SubC2, SubC7)
├─ 4. Estado de Resultados
│   └─ (mismo proceso)
├─ 5. Libro Mayor
│   ├─ Por cada cuenta seleccionada
│   └─ Descarga
├─ 6. Cuadro 9
│   └─ Para conciliación
└─ 7. Guarda todo en carpeta centralizada
```

**Pros:** Automatización completa, sin cambios

**Contras:** Lento, frágil a cambios de interfaz

**Opción B: API (SI e-SIDIF lo soporta)**

```python
# Si e-SIDIF abre API en futuro
import esidif_api

reportes = {
    "balance_general": esidif_api.get_balance_general(
        ano=2026,
        ente="Ministerio",
        nivel=4  # Cuenta
    ),
    "estado_resultados": esidif_api.get_estado_resultados(
        ano=2026,
        ente="Ministerio",
        nivel=4
    ),
    "libro_mayor": esidif_api.get_libro_mayor(
        ano=2026,
        ente="Ministerio",
        cuenta="1.1.1.01.01.00.00"
    ),
    "cuadro9": esidif_api.get_cuadro9(
        ano=2026,
        ente="Ministerio"
    )
}
```

**Status actual:** ❌ NO DISPONIBLE

---

### 2.2 VALIDACIÓN DE INTEGRIDAD

| Aspecto | Detalles |
|--------|----------|
| **Automatizar** | ✅ SÍ |
| **Complejidad** | 🟢 BAJA |
| **Esfuerzo** | 2-3 días |
| **Riesgo** | Bajo |

#### Validaciones Automáticas

```python
def validar_integridad_contable(balance_general, estado_resultados, libro_mayor):
    """
    Validaciones automáticas de integridad contable
    """
    
    # 1. Ecuación contable: A = P + PN
    validar_ecuacion_fundamental(balance_general)
    
    # 2. Cuadro 9: Presupuesto ↔ Contabilidad
    validar_cuadro9(libro_mayor)
    
    # 3. Suma de cuentas = Suma de detalles (7 niveles)
    validar_jerarquia_cuentas(balance_general)
    
    # 4. Libro Mayor ↔ Balance General
    validar_consistencia_libro_mayor(libro_mayor, balance_general)
    
    # 5. Períodos contables
    validar_periodos_completos(estado_resultados)
    
    # 6. No hay cuentas duplicadas
    validar_sin_duplicados(estado_resultados)
    
    # Reporte de errores
    return {
        "estado": "APROBADO" | "RECHAZADO",
        "errores": [...],
        "advertencias": [...]
    }
```

---

### 2.3 CONCILIACIÓN PRESUPUESTO ↔ CONTABILIDAD

| Aspecto | Detalles |
|--------|----------|
| **Automatizar** | ✅ SÍ |
| **Complejidad** | 🟡 MEDIA |
| **Esfuerzo** | 1-2 semanas |
| **Riesgo** | Medio |

#### Matriz de Reconciliación

```
9 INCISOS PRESUPUESTARIOS       CUENTAS CONTABLES (7 NIVELES)
                                │
├─ 1. Personal              ────┤─ Gasto Personal (2.5.1.x.x.x.x)
├─ 2. Bienes Consumo        ────┤─ Gasto Bienes (2.5.2.x.x.x.x)
├─ 3. Servicios             ────┤─ Gasto Servicios (2.5.3.x.x.x.x)
├─ 4. Bienes Uso            ────┤─ Activo Fijo (1.2.1.x.x.x.x)
├─ 5. Transferencias        ────┤─ Gasto/Pasivo Transferencias
├─ 6. Activos Financieros   ────┤─ Activo Financiero (1.2.2.x.x.x.x)
├─ 7. Deuda                 ────┤─ Pasivo Deuda (2.1.x.x.x.x.x)
├─ 8. Otros                 ────┤─ Gasto/Activo Otros
└─ 9. Figurativos           ────┤─ Cuentas de Orden (8.x.x.x.x.x.x)

Validación: Suma(Incisos 1-7) = Suma(Cuentas 2.5.x.x.x.x.x)
            Suma(Crédito) = Suma(Activos - Pasivos - PN)
```

#### Algoritmo de Conciliación

```python
def reconciliar_presupuesto_contabilidad(presupuesto, contabilidad):
    """
    Conciliar presupuesto con contabilidad automáticamente
    """
    
    # 1. Mapeo de incisos a cuentas
    mapa = {
        "1_Personal": "2.5.1.*.*.*.*",
        "2_Bienes_Consumo": "2.5.2.*.*.*.*",
        # ... etc
    }
    
    # 2. Sumar por lado presupuestario
    totales_presupuestarios = {}
    for inciso in presupuesto.incisos:
        totales_presupuestarios[inciso] = sum(presupuesto[inciso])
    
    # 3. Sumar por lado contable (usando Cuadro 9)
    totales_contables = {}
    for inciso, patron in mapa.items():
        totales_contables[inciso] = sum(
            contabilidad.cuentas_que_coinciden(patron)
        )
    
    # 4. Comparar y encontrar diferencias
    diferencias = {}
    for inciso in totales_presupuestarios:
        presup = totales_presupuestarios[inciso]
        contab = totales_contables[inciso]
        if presup != contab:
            diferencias[inciso] = {
                "presupuesto": presup,
                "contabilidad": contab,
                "diferencia": presup - contab
            }
    
    # 5. Reporte
    return {
        "reconciliados": len(totales_presupuestarios) - len(diferencias),
        "diferencias": diferencias,
        "total_diferencia": sum(d["diferencia"] for d in diferencias.values())
    }
```

---

## 3. INTEGRACIÓN SAP FI/CO

### 3.1 MAPEO SAP FI/CO ↔ e-SIDIF

| Aspecto | Detalles |
|--------|----------|
| **Automatizar** | ✅ SÍ (parcial) |
| **Complejidad** | 🔴 ALTA |
| **Esfuerzo** | 2-3 semanas |
| **Riesgo** | Alto |

#### Estructura de Mapeo

```
SAP FI (Finanzas)               e-SIDIF CONTABILIDAD
│                               │
├─ Plan de Cuentas SAP     ────→ Plan de Cuentas e-SIDIF
│  ├─ 1000-1999 (Activo)         ├─ 1.x.x.xx.xx.xx.xx
│  ├─ 2000-2999 (Pasivo)         ├─ 2.x.x.xx.xx.xx.xx
│  └─ 3000-9999 (PN/Gasto/Ingr)  └─ 3.x.x.xx.xx.xx.xx
│
├─ Centros de Costo (KOSTL)  ──→ Aperturas Programáticas
│
├─ Órdenes Internas (AUFNR)  ──→ Proyectos
│
├─ Elementos PEP (PSPID)     ──→ Categorías Programáticas
│
└─ Análisis de rentabilidad   ──→ Moneda, Jurisdicción
```

#### Desafíos de Mapeo

```
❌ PROBLEMA 1: Estructura de Cuentas
   SAP usa 4-6 dígitos
   e-SIDIF usa 11 dígitos (7 niveles)
   → Requiere expansión de código SAP

❌ PROBLEMA 2: Clasificadores
   SAP: Centro de costo, orden interna
   e-SIDIF: Aperturas programáticas, moneda, jurisdicción
   → Requiere enriquecimiento de datos

❌ PROBLEMA 3: Múltiples entidades
   SAP: Una sociedad (BUKRS) puede mapear a múltiples entes e-SIDIF
   e-SIDIF: Un ente puede recibir datos de múltiples sociedades SAP
   → Requiere matriz de mapeo N:M

❌ PROBLEMA 4: Validaciones de negocio
   SAP valida según reglas SAP
   e-SIDIF valida según reglas CGN
   → Pueden ser incompatibles
```

#### Solución Propuesta

```
┌─────────────────────────────────────────────────────┐
│         CAPA DE INTEGRACIÓN SAP → e-SIDIF           │
├─────────────────────────────────────────────────────┤
│                                                       │
│  SAP Extracción                                     │
│  ├─ FI: Asientos contables                          │
│  ├─ CO: Órdenes, centros de costo                   │
│  └─ PS: Proyectos                                   │
│         │                                            │
│         ↓                                            │
│  Transformación (ETL)                               │
│  ├─ Expansión de cuentas: 4 dígitos → 11 dígitos   │
│  ├─ Mapeo de centros costo → programas              │
│  ├─ Enriquecimiento con clasificadores             │
│  └─ Validación de integridad                        │
│         │                                            │
│         ↓                                            │
│  Generación de Templates Excel (componentes)        │
│  ├─ Crédito (presupuesto)                          │
│  ├─ Recurso (fuente de financiamiento)             │
│  ├─ Física Programa                                 │
│  ├─ Física Proyecto                                 │
│  └─ Financiera Proyecto                             │
│         │                                            │
│         ↓                                            │
│  Importación a e-SIDIF                              │
│  ├─ Validación de estructura (Scripts)              │
│  ├─ Importación automática (RPA)                    │
│  └─ Validación de resultado                         │
│         │                                            │
│         ↓                                            │
│  Verificación Cruzada                               │
│  ├─ Cuadro 9: Reconciliación                        │
│  ├─ Balance General: A = P + PN                     │
│  └─ Reporte de excepciones                          │
│                                                       │
└─────────────────────────────────────────────────────┘
```

---

## RESUMEN DE ESFUERZOS

### Por Funcionalidad

| Funcionalidad | Complejidad | Días | Costo |
|---------------|------------|------|-------|
| **Validador Templates** | 🟢 Baja | 1-2 | Bajo |
| **Extractor de Reportes** | 🟡 Media | 3-5 | Medio |
| **Validador de Integridad** | 🟢 Baja | 2-3 | Bajo |
| **Conciliación Presupuesto ↔ Contabilidad** | 🟡 Media | 5-7 | Medio |
| **Mapeo SAP → e-SIDIF** | 🔴 Alta | 10-14 | Alto |
| **RPA Importación Presupuestaria** | 🟡 Media | 5-7 | Medio |
| **RPA Extracción Reportes** | 🟡 Media | 3-5 | Medio |
| **TOTAL (Stack Completo)** | 🔴 Alta | 30-45 | Alto |

### Cronograma Recomendado

```
FASE 1 (Semana 1-2):
├─ Validador Templates
├─ Extractor de Reportes
└─ Validador de Integridad
   → 6-10 días de trabajo

FASE 2 (Semana 3-4):
├─ Conciliación Presupuesto ↔ Contabilidad
├─ RPA Importación
└─ RPA Extracción
   → 13-19 días de trabajo

FASE 3 (Semana 5-6):
├─ Mapeo SAP → e-SIDIF
├─ Testing con datos reales
└─ Documentación
   → 10-14 días de trabajo

TOTAL: 6 semanas / 30-45 días
```

---

## RECOMENDACIONES FINALES

### ✅ COMENZAR CON (Alto Valor, Bajo Riesgo)

1. **Validador de Templates Excel**
   - Previene errores antes de importar
   - ROI inmediato
   - Complejidad baja

2. **Extractor de Reportes (RPA)**
   - Automatiza tareas repetitivas
   - Libera tiempo del personal
   - Poco riesgo

3. **Validador de Integridad**
   - Detecta inconsistencias automáticamente
   - Calidad de datos
   - Bajo esfuerzo

### 🔮 FUTURO (Cuando e-SIDIF abra APIs)

1. **APIs de e-SIDIF** (Esperar comunicación oficial CGN)
   - Reemplazaría RPA
   - Más confiable
   - Mejor rendimiento

2. **Integración nativa SAP ↔ e-SIDIF**
   - Síncronización en tiempo real
   - Conciliación automática
   - Mayor complejidad

---

**Documento preparado por:** Análisis de Documentación Oficial e-SIDIF  
**Metodología:** Lectura manual sin asumir información  
**Confiabilidad:** Alta (basado en documentos oficiales CGN)
