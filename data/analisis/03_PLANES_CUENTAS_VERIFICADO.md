# ANÁLISIS DETALLADO: PLANES DE CUENTAS e-SIDIF
## Reportes y Estados Contables

**Fuente:** Guía de Ayuda para el usuario – Reportes y Estados Contables.pdf  
**Total páginas:** 19  
**Páginas analizadas:** 2, 5, 7-9, 13-17  
**Fecha de análisis:** 2026-10-03

---

## 1. INTRODUCCIÓN - NUEVO MODELO CONTABLE

### Cambio Fundamental: De 6 a 11 Dígitos

La Contaduría General de la Nación (CGN) definió un **nuevo modelo contable** que acompaña cambios significativos:

```
MODELO ANTERIOR       →    NUEVO MODELO (e-SIDIF)
├─ 6 dígitos             ├─ 11 dígitos
├─ Desagregación         ├─ DESAGREGACIÓN MUCHO MAYOR
│  básica                │
└─ Pocos                 └─ MUCHOS clasificadores
   clasificadores           incorporados
```

### Plan de Cuentas e-SIDIF

```
ESTRUCTURA: 7 niveles × 11 dígitos

Ejemplo: 1.1.1.01.01.00.00

Desglose:
├─ Nivel 1: 1 (Clase de Cuenta)
├─ Nivel 2: 1 (Subclase)
├─ Nivel 3: 1 (Grupo)
├─ Nivel 4: 01 (Subgrupo)
├─ Nivel 5: 01 (Clasificador secundario)
├─ Nivel 6: 00 (Desagregación)
└─ Nivel 7: 00 (Desagregación final)

Descripción: "Cajas en Moneda Nacional"
```

---

## 2. CLASIFICADORES INCORPORADOS EN NUEVO MODELO

### Mejoras Respecto al Modelo Anterior

El nuevo modelo **enriquece la información contable** al incorporar:

#### 1. Cuenta Única del Tesoro (CUT)

```
Propósito: Distinguir operaciones CUT vs no-CUT

Valor:
├─ Sí: Operaciones de la Cuenta Única del Tesoro
└─ No: Operaciones fuera de CUT

Ejemplo de uso:
├─ Fondos en CUT vs fondos en tesorería
├─ Ingresos CUT vs otros ingresos
└─ Gastos CUT vs otros gastos
```

#### 2. Moneda de Operación

```
Propósito: Registrar transacciones en múltiples monedas

Clasificador por:
├─ Moneda Nacional (ARS)
├─ Dólar (USD)
├─ Euros (EUR)
└─ Otras monedas según operatoria

Ejemplo:
├─ 1.1.1.01.01.00.00 → Cajas en Moneda Nacional
├─ 1.1.1.01.01.00.01 → Cajas en Dólares
└─ 1.1.1.01.01.00.02 → Cajas en Euros
```

#### 3. Retenciones por Jurisdicción

```
Propósito: Desagregar retenciones fiscales por origen

Clasificación:
├─ Nacionales (Gobierno Nacional)
├─ Provinciales (Gobiernos Provinciales)
└─ Municipales (Gobiernos Municipales)

Ejemplo: Retención IVA Nacional vs Provincial vs Municipal
```

#### 4. Retenciones por Tributo

```
Propósito: Separar por tipo de impuesto retenido

Clasificación:
├─ IVA (Impuesto al Valor Agregado)
├─ Ganancias (Impuesto a la Ganancia)
└─ Ingresos Brutos (Impuesto a Ingresos Brutos)

Ejemplo: 
├─ Retención IVA Nacional
├─ Retención Ganancias Provincial
└─ Retención IB Municipal
```

#### 5. Datos Extracontables Auxiliares

```
Propósito: Enriquecer información con datos del comprobante

Datos auxiliares registrados:
├─ Beneficiario (quién recibe el pago)
├─ Cliente (quién origina la operación)
├─ Fuente de Financiamiento (de dónde viene)
└─ Identificador del Trámite (número de expediente)

Implicación:
└─ Contabilidad + Datos de comprobante = información completa
```

---

## 3. ESTRUCTURA DE 7 NIVELES - EJEMPLO PRÁCTICO

### Desglose Completo de 1.1.1.01.01.00.00

```
NIVEL 1 (Clase): 1 = ACTIVO
├── NIVEL 2 (Subclase): 1.1 = ACTIVO CORRIENTE
│   ├── NIVEL 3 (Grupo): 1.1.1 = DISPONIBILIDADES
│   │   ├── NIVEL 4 (Subgrupo): 1.1.1.01 = Cajas
│   │   │   ├── NIVEL 5 (Clasificador): 1.1.1.01.01 = Cajas de Tesorería
│   │   │   │   ├── NIVEL 6 (Desagregación): 1.1.1.01.01.00 = Por Moneda Nacional
│   │   │   │   │   └── NIVEL 7 (Final): 1.1.1.01.01.00.00 = Cajas en Moneda Nacional
```

### Jerarquía de Agregación

```
Nivel de Mayor Agregación   ← Menos detalle (Reportes de Alto Nivel)
│
├─ Nivel 4: Cuenta (1.1.1.01) → Para reportes ejecutivos
├─ Nivel 5: SubCuenta 1er O. (1.1.1.01.01) → Para reportes gerenciales
├─ Nivel 6: SubCuenta 2do O. (1.1.1.01.01.00) → Para análisis detallado
│
Nivel de Mayor Desagregación → Máximo detalle (Libro Mayor)
└─ Nivel 7: SubCuenta Anexa (1.1.1.01.01.00.00) → Para auditoría
```

---

## 4. REPORTES CONTABLES DISPONIBLES

### Archivos de e-SIDIF: Módulo Contabilidad General

El módulo ofrece **6 tipos de reportes**, cada uno con **4 versiones** (por nivel de desagregación):

---

## 4.1 BALANCE GENERAL

### Descripción
Estado financiero que muestra **Activos, Pasivos y Patrimonio Neto** a una fecha específica.

### Validación
> **Valida ecuación contable básica: A = P + PN**

Si ecuación no se cumple → Muestra leyenda de advertencia al pie

### 4 Versiones Disponibles

| Versión | Desagregación | Nivel | Ejemplo | Uso |
|---------|---------------|-------|---------|-----|
| **Cuenta** | 4 primeros niveles | 4 | 1.1.1.01 | Ejecutivo |
| **SubCuenta 1er O.** | 5 primeros niveles | 5 | 1.1.1.01.01 | Gerencial |
| **SubCuenta 2do O.** | 6 primeros niveles | 6 | 1.1.1.01.01.00 | Análisis |
| **SubCuenta Anexa** | 7 niveles (máximo) | 7 | 1.1.1.01.01.00.00 | Auditoría |

### Parámetros de Ejecución

```
Año Contable:           [2026]
Ente Contable:          [Seleccionar]
Código Entidad Emisora: [Una o múltiples]
Fecha Contable:         [Fecha/Hora]

Botón: APLICAR → Genera los 4 reportes
```

### Información en Cabecera
- Usuario emitente
- Fecha y hora de ejecución
- Fecha y hora de última extracción de datos

---

## 4.2 ESTADO DE RESULTADOS

### Descripción
Muestra **Ingresos, Gastos y Resultados** del período.

### Estructura
Similar a Balance General:
- 4 versiones (Cuenta → SubCuenta Anexa)
- Cada versión con diferente nivel de detalle

### Parámetros de Ejecución

```
Año Contable:           [2026]
Ente Contable:          [Seleccionar]
Código Entidad Emisora: [Una o múltiples]
Fecha Contable:         [Fecha/Hora]

Botón: APLICAR → Genera los 4 reportes
```

---

## 4.3 LIBRO MAYOR

### Descripción
Detalle **COMPLETO de débitos y créditos** de una cuenta contable para un ejercicio y período.

### Características
- ✅ Desagregación: **Nivel 7 (máximo)** - Cuenta imputable
- ✅ Información: Movimientos detallados por asiento
- ✅ Trazabilidad: Número de asiento, fecha, concepto
- ✅ Período: Rango de fechas (desde-hasta)

### Parámetros Obligatorios

```
Año Contable:              [2026]
Ente Contable:             [Seleccionar] ✅ OBLIGATORIO
Código Entidad Emisora:    [Seleccionar] ✅ OBLIGATORIO
Fecha Contable:            [Fecha/Hora] ✅ OBLIGATORIO
Fecha desde:               [Desde]
Fecha hasta:               [Hasta]

FILTRO Cuenta Contable:
├─ Por defecto: 1.1.1.01.01.00.00 (Cajas Moneda Nacional)
├─ Opción 1: Seleccionar de lista desplegable
│   └─ Muestra hasta 5 cuentas
│   └─ Con scroll para desplazar
├─ Opción 2: Usar "Más / Buscar..." para búsqueda avanzada
│   └─ Refinar búsqueda por parámetros
│   └─ Mover seleccionadas a "seleccionado"
└─ Soporta búsqueda múltiple (varias cuentas)

Botón: APLICAR → Genera Libro Mayor
```

### Búsqueda Inteligente de Cuentas

#### Operadores

```
NOMBRE (atributo de búsqueda):

├─ "Empieza por" (valor por defecto)
│  └─ Ejemplo: "2.2.1"
│     Resultado: Cuentas de deudas comerciales (comienzan con 2.2.1)
│
├─ "Contiene"
│  └─ Ejemplo: "amort"
│     Resultado: TODAS las cuentas con "amort" en descripción
│     Nota: Pueden ser de Activo (amortización de bienes)
│            O de Gastos (amortización como gasto)
│
└─ "Termina en" (inverso a "empieza por")
   └─ Ejemplo: "00.00"
      Resultado: Cuentas que terminan en esa secuencia
```

#### Interfaz de Búsqueda

```
┌─────────────────────────┬─────────────────────────┐
│   DISPONIBLES           │    SELECCIONADO         │
│                         │                         │
│  [Cuenta 1]             │  [Cuenta A] → [Flecha↓] │
│  [Cuenta 2] → [Flecha↑] │  [Cuenta B]             │
│  [Cuenta 3]             │                         │
│                         │                         │
│  [Más/Buscar...]        │                         │
│                         │                         │
└─────────────────────────┴─────────────────────────┘

Botones de movimiento:
├─ Flecha derecha: Pasar de disponibles a seleccionado
├─ Flecha izquierda: Quitar de seleccionado
└─ APLICAR: Ejecutar reporte
```

### Información en Reporte

```
Columnas:
├─ Cuenta Contable
├─ Asiento (Ejercicio, Período, Número)
├─ Fecha Contable
├─ Entidad Emisora
├─ Auxiliares Contables
│  ├─ Entidad emisora del comprobante
│  ├─ Número y número SIDIF del comprobante
│  ├─ Entidad emisora
│  └─ Descripción del asiento
└─ Movimiento (Débito o Crédito)

En cabecera:
├─ Usuario emitente
├─ Fecha y hora de ejecución
└─ Fecha y hora de última extracción de datos
```

---

## 4.4 RESUMEN AGREGADO DE REGISTROS CONTABLES

### Descripción
Expone **movimientos presupuestarios y extrapresupuestarios POR CUENTA**, consolidado.

### Columnas del Reporte

```
├─ Código Cuenta Contable
├─ Descripción Cuenta
├─ Debe Inicial
├─ Haber Inicial
├─ Debe Presupuestario
├─ Haber Presupuestario
├─ Debe Extrapresupuestario
├─ Haber Extrapresupuestario
├─ Debe Saldo (Final)
└─ Haber Saldo (Final)

Disponible en 4 niveles de desagregación
```

### Parámetros

```
Año Contable:           [2026]
Ente Contable:          [Seleccionar] ✅ OBLIGATORIO
Fecha Contable:         [Fecha/Hora]
Fecha hasta:            [Hasta] ✅ OBLIGATORIO

Botón: APLICAR → Genera 4 reportes (por nivel)
```

### Exportación

```
Desplazando con scroll derecha:
├─ Botón: IMPRIMIR
└─ Botón: EXPORTAR (→ archivo)

Permite obtener información según:
└─ Nivel de desagregación que requiera el usuario
```

---

## 4.5 RESUMEN ANALÍTICO DE REGISTROS CONTABLES

### Descripción
Similar a Resumen Agregado pero **incluye movimientos de ejercicios anteriores**.

### Diferencia vs. Resumen Agregado

```
AGREGADO:        Año actual solamente
                 └─ Debe/Haber inicial, presupuestario, extrap.

ANALÍTICO:       Año actual + AÑOS ANTERIORES
                 ├─ Debe/Haber inicial
                 ├─ Debe/Haber PRESUPUESTARIO (P) año actual
                 ├─ Debe/Haber EXTRAPRESUPUESTARIO (E) año actual
                 ├─ Debe/Haber Presupuestario EJERCICIOS ANTERIORES (R)
                 ├─ Debe/Haber Extrapresupuestario EJERCICIOS ANTERIORES (X)
                 └─ Debe/Haber Saldo (Final)
```

### Columnas

```
Significado de columnas:
├─ (P): Presupuestario
├─ (E): Extrapresupuestario
├─ (R): Resultado ejercicio anterior (Resalted years)
├─ (X): Extrapresupuestario de ejercicios anteriores
└─ Saldo: Total consolidado
```

### Parámetros

```
Año Contable:           [2026]
Ente Contable:          [Seleccionar]
Fecha Contable:         [Fecha/Hora]
Fecha hasta:            [Hasta]

Botón: APLICAR → Genera 4 reportes
```

---

## 4.6 CUADRO 9 - COMPATIBILIDAD DE ESTADOS CONTABLES ⭐

### Propósito

> **Chequear la CONSISTENCIA entre estados contables de la entidad y registros presupuestarios del Sistema Integrado de Información Financiera (SIIF)**

### Validación

```
El Cuadro 9 verifica que:

├─ Activo (contable) = Activo (presupuestario)
├─ Pasivo (contable) = Pasivo (presupuestario)
├─ Patrimonio Neto (contable) = PN (presupuestario)
├─ Recursos (contable) = Recursos (presupuestario)
└─ Gastos (contable) = Gastos (presupuestario)

Si hay diferencias:
└─ Las expone claramente para investigación
```

### Nivel de Desagregación

```
Desagregación: HASTA 4to nivel (Cuenta)
NO incluye SubCuentas de mayor detalle
```

### Columnas de Importes

```
├─ Balance General Cierre Ejercicio Anterior
├─ Flujos Presupuestarios Ejercicio Actual
├─ Flujos Extrapresupuestarios Ejercicio Actual
├─ Flujos Totales Ejercicio Actual
└─ Balance General Cierre Ejercicio Actual
```

### Parámetros

```
Año Contable:           [2026]
Ente Contable:          [Seleccionar]
Fecha Contable:         [Fecha/Hora]
Fecha hasta:            [Hasta]

Botón: APLICAR → Genera Cuadro 9
```

---

## 5. INTEGRACIÓN PRESUPUESTO ↔ CONTABILIDAD

### Arquitectura Fundamental

```
SISTEMA e-SIDIF

MÓDULO PRESUPUESTARIO              MÓDULO CONTABLE
│                                   │
├─ Presupuesto                      │
├─ Carga de Anteproyectos           │
├─ Modificaciones Presupuestarias   │
├─ Programación de Ejecución        │
│                                   │
└──→ COMPROBANTE PRESUPUESTARIO ────→ ASIENTO CONTABLE
                                    └─ Plan de Cuentas
                                    └─ Auxiliares contables
```

### Flujo de Datos

```
COMPROBANTE PRESUPUESTARIO contiene:
├─ Beneficiario
├─ Cliente
├─ Fuente de Financiamiento
├─ Identificador del Trámite
└─ Datos presupuestarios

        ↓
        
SE GENERA ASIENTO CONTABLE que incluye:
├─ Datos presupuestarios ORIGINALES
├─ Datos extracontables AUXILIARES (beneficiario, cliente, etc.)
└─ Contabilización en Plan de Cuentas (7 niveles)

        ↓
        
ENRIQUECIMIENTO: Contabilidad combina datos presupuestarios
                 + datos auxiliares = información más rica
```

### Principio Clave

```
🔴 UNIDIRECCIONAL: Presupuesto → Contabilidad

NO EXISTE sincronización inversa:
- Cambios presupuestarios generan nuevos asientos contables
- Cambios contables NO modifican presupuesto
- La contabilidad es DERIVADA del presupuesto
```

### Mapeo Fundamental

**Los 9 incisos presupuestarios deben mapear a las cuentas contables:**

```
9 INCISOS PRESUPUESTARIOS          PLAN DE CUENTAS (7 NIVELES)
│                                   │
├─ 1. Personal                  ──→ Cuentas de Gasto/Pasivo
├─ 2. Bienes Consumo            ──→ Cuentas de Gasto/Activo
├─ 3. Servicios                 ──→ Cuentas de Gasto
├─ 4. Bienes Uso                ──→ Cuentas de Activo Fijo
├─ 5. Transferencias            ──→ Cuentas de Gasto/Pasivo
├─ 6. Activos Financieros       ──→ Cuentas de Activo
├─ 7. Deuda                     ──→ Cuentas de Pasivo
├─ 8. Otros                     ──→ Cuentas Varias
└─ 9. Figurativos               ──→ Cuentas Orden
```

---

## 6. ✅ QUÉ SE PUEDE AUTOMATIZAR

### Confirmado en Documento

| Funcionalidad | Posible | Nivel |
|---------------|--------|-------|
| **Búsqueda de cuentas por nombre** | ✅ SÍ | Operadores: empieza, contiene, termina |
| **Extracción de reportes** | ✅ SÍ | 6 tipos × 4 niveles = 24 combinaciones |
| **Validación A = P + PN** | ✅ SÍ | Automática en Balance General |
| **Conciliación Cuadro 9** | ✅ SÍ | Automática, expone diferencias |
| **Exportación a archivos** | ✅ SÍ | Cada reporte tiene opción export |
| **Cálculos contables** | ✅ SÍ | Suma, resta, consolidación automática |
| **Filtros por Ente/Período** | ✅ SÍ | Múltiples parámetros |

### NO es Posible (Limitación de e-SIDIF)

| Funcionalidad | Posible | Razón |
|---------------|--------|-------|
| **API de reportes** | ❌ NO | e-SIDIF no expone WS de reportes |
| **Actualización de cuentas** | ❌ NO | Plan de Cuentas es administrado por CGN |
| **Creación de cuentas custom** | ❌ NO | Estructura centralizada en e-SIDIF |
| **Modificación de reportes** | ❌ NO | Reportes predefinidos por CGN |

---

## 7. PRÓXIMOS PASOS - VERIFICACIÓN NECESARIA

### Investigación Recomendada

1. **📊 Descargar ejemplos reales de reportes**
   - Balance General de un ente
   - Estado de Resultados
   - Cuadro 9 completo

2. **🔍 Analizar Cuadro 9 real**
   - ¿Dónde típicamente hay diferencias?
   - ¿Cuáles son los ajustes típicos?

3. **🔗 Mapeo específico Presupuesto → Contabilidad**
   - ¿Cuál inciso presupuestario mapea a cuál cuenta?
   - ¿Hay cuentas que reciben múltiples incisos?

4. **💾 Investigar exportación de datos**
   - ¿Qué formato soporta (Excel, CSV, PDF)?
   - ¿Se pueden extraer datos raw o solo reportes?

5. **🔐 Entender seguridad y acceso**
   - ¿Cuáles roles pueden extraer cada reporte?
   - ¿Hay auditoría de extracciones?

---

## CONCLUSIÓN

**El Plan de Cuentas e-SIDIF es una estructura robusta de 7 niveles que permite análisis a múltiples grados de desagregación.**

Fortalezas:
- ✅ Validaciones automáticas (A = P + PN)
- ✅ Trazabilidad completa (Libro Mayor detallado)
- ✅ Conciliación integrada (Cuadro 9)
- ✅ Múltiples reportes analíticos

Limitaciones:
- ❌ Sin APIs programáticas
- ❌ Acceso solo vía GUI de e-SIDIF

Oportunidad para SAP:
- 🔄 Integración unidireccional: e-SIDIF → SAP FI/CO
- 📊 Sincronización de reportes contables
- ✅ Validación cruzada automática

**Próximo documento:** Matriz de automatización y mapeo a SAP
