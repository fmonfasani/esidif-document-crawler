# ANÁLISIS DETALLADO: PRESUPUESTO - GUÍA FOP e-SIDIF
## Formulación Presupuestaria

**Fuente:** Guía para el Usuario FOP versión pto preliminar.pdf  
**Total páginas:** 45  
**Páginas analizadas:** 10-15, 29, 33  
**Fecha de análisis:** 2026-10-03

---

## 1. COMPONENTES DEL ESCENARIO PRESUPUESTARIO

### Los 5 Componentes

Al abrir un Escenario FOP, se estructura en **5 componentes independientes**:

```
Escenario FOP
├── 1. CRÉDITO
│   └── Base de asignaciones presupuestarias
├── 2. RECURSO
│   └── Fuentes de financiamiento
├── 3. FÍSICA DE PROGRAMA
│   └── Metas programáticas
├── 4. FÍSICA DE PROYECTO
│   └── Metas de proyectos específicos
└── 5. FINANCIERA DE PROYECTO
    └── Financiamiento de proyectos
```

### Regla Fundamental de Importación

> **La importación siempre actúa sobre la componente en la cual estamos posicionados (foco del cursor)**

Esto significa:
- ✅ Si seleccionas "Crédito" → importa datos a Crédito
- ✅ Si seleccionas "Recurso" → importa datos a Recurso
- ⚠️ Cada componente tiene su propia estructura de datos

---

## 2. MODALIDADES DE INCORPORACIÓN DE DATOS

### Acceso a Importación

**Menú:** `Entidad > Importar Elemento`

El sistema ofrece **2 modalidades principales:**

---

## 2.1 IMPORTAR DESDE ESCENARIO FOP (INTERNO)

### Descripción
Permite importar datos desde cualquier escenario disponible en el Sistema para la SAF (Secretaría de Asuntos Fiscales).

**Caso especial:** ONP (Oficina Nacional de Presupuesto) brinda escenario de referencia con datos del crédito vigente.

### Flujo de 6 Pasos

```
PASO 1: Seleccionar modalidad
        ↓
PASO 2: Indicar opción (Crédito/Recurso/Física Programa/etc.)
        ↓
PASO 3: Buscar escenario fuente
        ↓
PASO 4: Seleccionar escenario encontrado
        ↓
PASO 5: Aplicar filtros y criterios
        ↓
PASO 6: Elegir política de importación
```

### Paso 5: Filtros y Criterios

**Campos de Filtro:**
- Permite seleccionar segmentos de datos
- Crítico para importar parcialmente

**Criterios de Origen del Saldo (3 opciones):**

| Criterio | Significado |
|----------|-------------|
| **Saldo Inicial** | Usa saldo de inicio de período |
| **Saldo Final** | Usa saldo de cierre de período |
| **Saldo Final a Etapa** | Usa saldo a una etapa específica |

### Paso 6: Políticas de Importación (4 Opciones Mutualmente Excluyentes)

#### 1. Agregar o Reemplazar
```
Si elemento ORIGEN existe en DESTINO:
    → Borra físicamente elemento DESTINO
    → Importa elemento ORIGEN

Si NO existe en DESTINO:
    → Solo importa ORIGEN
```
**Uso:** Sincronización total, sobrescribir todo

#### 2. Agregar o Ignorar
```
Si elemento ORIGEN existe en DESTINO:
    → Ignora elemento ORIGEN
    → Mantiene DESTINO intacto

Si NO existe en DESTINO:
    → Importa ORIGEN
```
**Uso:** Preservar datos locales existentes

#### 3. Agregar o Acumular ⭐
```
Si elemento ORIGEN existe en DESTINO:
    → SUMA cantidad_origen + cantidad_destino
    → Almacena resultado en DESTINO

Si NO existe en DESTINO:
    → Importa ORIGEN
```
**Uso:** Consolidación de presupuestos de múltiples fuentes
**Ejemplo:** Presupuesto base + presupuesto adicional

#### 4. Agregar o Igualar
```
Si elemento ORIGEN existe en DESTINO:
    → Ajusta DESTINO para igualarlo al valor ORIGEN

Si NO existe en DESTINO:
    → Importa ORIGEN
```
**Uso:** Sincronización de valores, mantener target

### Opción Especial: "Con Recarga"

```
Si selecciona "Con recarga":
    → Impactarán los importes en columna "Ajuste"
    → Se suma al Saldo Inicial General (de constitución)
```

**Caso: Importar de años anteriores**

Si importa Física o Financiera de escenario FOP del **año anterior**:
- Opción "Desfasaje de columnas" desplaza períodos
- Mueve datos al período correspondiente en nuevo escenario
- Con acumulación: suma último ejercicio ejecutado al acumulado nuevo

---

## 2.2 IMPORTAR DESDE ARCHIVOS EXCEL ⭐ CLAVE PARA AUTOMATIZACIÓN

### Descripción
Permite cargar datos directamente desde archivos Excel manteniendo estructura de Templates.

### Requisitos Obligatorios

```
✅ OBLIGATORIO:
   ├─ Respetar estructura de datos de Templates DEFINIDOS
   ├─ Tener PEX en el template (dato obligatorio)
   ├─ Tener BAPIN en el template (dato obligatorio)
   ├─ Templates DEBEN estar ACTUALIZADOS
   └─ Un archivo Excel POR CADA COMPONENTE

⚠️ IMPORTANTE:
   └─ Debe posicionarse en la componente antes de importar
```

### Flujo de 3 Pasos

```
PASO 1: Seleccionar "Importar desde archivos Excel"
        ↓
PASO 2: Indicar opción (componente)
        ↓
PASO 3: Buscar y seleccionar archivo Excel
        ↓
        [Sistema valida estructura automáticamente]
        ↓
        [Importa si estructura es correcta]
```

### Campos Obligatorios en Templates

| Campo | Descripción | Obligatorio |
|-------|-------------|-----------|
| **PEX** | Especificación | ✅ SÍ |
| **BAPIN** | Clasificador | ✅ SÍ |
| [Otros campos] | Según componente | Depende |

### Arquitectura de Archivos

```
├─ Template_Crédito.xlsx
├─ Template_Recurso.xlsx
├─ Template_Física_Programa.xlsx
├─ Template_Física_Proyecto.xlsx
└─ Template_Financiera_Proyecto.xlsx

Notas:
- 5 archivos diferentes (uno por componente)
- NO se pueden consolidar en un solo archivo
- Estructura debe coincidir exactamente
```

---

## 3. ESTRUCTURA DE VISTAS Y FILTROS

### Aperturas Programáticas - Nomenclatura

El sistema permite definir **vistas parciales** usando notación de patrones:

#### Ejemplo: Programa 1 Completo
```
Patrón: 1.*.*.*.* 

Significa:
└─ Programa 1
   └─ Todos los Subprogramas (*)
      └─ Todas las Actividades (*)
         └─ Todos los Proyectos (*)
            └─ Todas las Obras (*)
```

#### Ejemplo: Programa 1, Actividad 2 Específica
```
Patrón: 1.*.*.2.* 

Significa:
└─ Programa 1
   └─ Todos los Subprogramas (*)
      └─ Todas las Actividades (*)
         └─ Actividad 2 específica
            └─ Todos los Proyectos (*)
```

### Filtros Combinados

```
Es posible hacer filtros COMBINADOS:
└─ Programa 1
   ├─ Objeto 1
   ├─ Fuente 1.1
   └─ Moneda 1

Resultado: Datos muy específicos según múltiples criterios
```

---

## 4. CAMPOS DISPONIBLES PARA AJUSTES Y OPERACIONES

### (Página 33 - Ajustes de Escenarios)

#### Campos de Clasificadores (Seteo solo)

```
Estos campos se pueden SETEAR (reemplazar):
├─ Agrupamiento Institucional
├─ Servicio
├─ Aperturas Programática
├─ Ubicación Geográfica
├─ Objeto del Gasto
├─ Fuente de Financiamiento
└─ Moneda

Operación: Seteo Clasificador (reemplaza valor)
```

#### Campos Numéricos (Múltiples operaciones)

```
Estos campos soportan CÁLCULOS:
├─ Crédito Ajuste
└─ Saldo Final

Operaciones disponibles:
├─ Suma (+)
├─ Resta (-)
├─ Multiplicación (×)
├─ División (÷)
├─ Distribución uniforme (÷ en partes iguales)
└─ Seteo (=)
```

---

## 5. VALIDACIONES AUTOMÁTICAS

### Validación de Estructura

> **El sistema, en forma lógica, actúa validando la estructura de los datos y campos de cada componente.**

Esto significa:
- ✅ Valida que columnas coincidan
- ✅ Valida que tipos de datos sean correctos
- ✅ Valida campos obligatorios (PEX, BAPIN)
- ❌ Rechaza si estructura no coincide

### Sin Web Services

> **⚠️ TODO vía interfaz manual - NO hay web services para presupuesto**

Implicaciones:
- ❌ No hay APIs REST
- ❌ No hay importación automática sin interfaz
- ✅ Importación Excel requiere acción manual en GUI
- ✅ Pero Excel permite **preparar datos offline**

---

## 6. CICLO PRESUPUESTARIO vs. CARGA DE DATOS

### Las 5 Fases del Ciclo

```
CICLO PRESUPUESTARIO
│
├─ FASE 1: FORMULACIÓN
│  └─ Organismos crean "Anteproyectos"
│     └─ [AQUÍ se cargan datos via FOP - Excel o manual]
│
├─ FASE 2: DISCUSIÓN Y APROBACIÓN
│  └─ Congreso aprueba el presupuesto
│     └─ [Se congela para aprobación]
│
├─ FASE 3: EJECUCIÓN
│  └─ Se dicta "Decisión Administrativa"
│  └─ Se asignan "cuotas de ejecución"
│     └─ [Se pueden hacer modificaciones - MPPE]
│
├─ FASE 4: EVALUACIÓN Y CONTROL
│  └─ Análisis trimestral de ejecución
│     └─ [Se extraen reportes]
│
└─ FASE 5: RENDICIÓN DE CUENTAS
   └─ CGN cierre presupuestario y contable
      └─ [Se genera contabilidad final]
```

### Información Trimestral

- **Frecuencia:** Trimestral
- **Vía:** Interfaz e-SIDIF
- **Tipo:** Todo ingreso es presupuestario

---

## 7. ✅ QUÉ SE PUEDE AUTOMATIZAR

### Confirmado en Documento

| Funcionalidad | Posible | Cómo |
|---------------|--------|------|
| **Validación de Templates Excel** | ✅ SÍ | Verificar estructura antes de importar |
| **Preparación offline de datos Excel** | ✅ SÍ | Generar archivos con estructura correcta |
| **Importación de múltiples archivos** | ✅ SÍ | Script que importa archivo por componente |
| **Aplicación de políticas** | ✅ SÍ | Seleccionar automáticamente acumular/reemplazar |
| **Filtros programáticos** | ✅ SÍ | Patrones 1.*.*.*.* |
| **Operaciones en columnas** | ✅ SÍ | Suma, resta, mult, div, seteo |
| **Exportación de datos** | ✅ SÍ | Extraer escenarios para análisis |

### NO es Posible (Limitación de e-SIDIF)

| Funcionalidad | Posible | Razón |
|---------------|--------|-------|
| **API web service presupuesto** | ❌ NO | e-SIDIF no tiene WS para presupuesto |
| **Importación sin GUI** | ❌ NO | Requiere interfaz manual |
| **Automatización 100% silent** | ❌ NO | Requiere interacción en GUI |

---

## 8. PRÓXIMOS PASOS - VERIFICACIÓN NECESARIA

### Alta Prioridad

1. **📄 Obtener un Template Excel real**
   - ¿Cuáles columnas exactamente?
   - ¿En qué orden?
   - ¿Hojas separadas?

2. **📋 Documentar restricciones de validación**
   - ¿Qué caracteres se permiten?
   - ¿Qué rangos de valores?
   - ¿Qué interdependencias?

3. **🔧 Crear validador de Templates**
   - Verificar estructura
   - Verificar PEX y BAPIN presentes
   - Reporte de errores antes de importar

### Media Prioridad

4. **📊 Extraer ejemplos reales**
   - De escenarios que funcionan
   - Entender patrones de datos

5. **🔀 Mapear 5 componentes**
   - ¿Cómo se relacionan?
   - ¿Hay orden de carga?
   - ¿Hay validaciones entre componentes?

### Baja Prioridad

6. **📈 Análisis de historial**
   - Cambios trimestral
   - Modificaciones presupuestarias
   - Patrones de crecimiento

---

## CONCLUSIÓN

**La Formulación Presupuestaria en e-SIDIF permite IMPORTACIÓN DESDE EXCEL con structure validada automáticamente.**

Esto abre la puerta a:
- ✅ Preparación de datos offline
- ✅ Validación previa a carga
- ✅ Migración desde sistemas anteriores
- ✅ Integración con SAP (si se preparan Templates)

**Próximo documento:** Planes de Cuentas - Estructura y reportes contables
