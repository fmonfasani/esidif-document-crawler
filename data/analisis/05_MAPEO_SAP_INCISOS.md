# MAPEO: 9 INCISOS PRESUPUESTARIOS e-SIDIF ↔ SAP FI/CO
## Documento de Relevamiento

**Fecha:** 2026-10-03  
**Etapa:** Relevamiento (Análisis)  
**Objetivo:** Identificar cómo los 9 incisos presupuestarios de e-SIDIF se mapean a módulos SAP

---

## 📋 LOS 9 INCISOS PRESUPUESTARIOS (e-SIDIF)

```
ESTRUCTURA PRESUPUESTARIA e-SIDIF
│
├─ 1. PERSONAL
│  └─ Gastos de personal
│
├─ 2. BIENES CONSUMO
│  └─ Bienes consumibles
│
├─ 3. SERVICIOS
│  └─ Servicios contratados
│
├─ 4. BIENES USO
│  └─ Bienes de uso (activos fijos)
│
├─ 5. TRANSFERENCIAS
│  └─ Transferencias a otras entidades
│
├─ 6. ACTIVOS FINANCIEROS
│  └─ Activos de naturaleza financiera
│
├─ 7. DEUDA
│  └─ Pago de deuda pública
│
├─ 8. OTROS
│  └─ Otros gastos no clasificados
│
└─ 9. FIGURATIVOS
   └─ Cuentas de orden (sin impacto en presupuesto real)
```

---

## 🔍 MÓDULOS SAP RELEVANTES

### 1. FI - Finanzas (Financial Accounting)

```
FI proporciona:
├─ Plan de Cuentas SAP
├─ Cuentas Mayores (GL: General Ledger)
├─ Gestión de Deudores/Acreedores
├─ Análisis de rentabilidad
└─ Reportes financieros
```

**Campos clave FI:**
- `SAKNR` = Número de Cuenta Mayor
- `KTO1` = Clase de Cuenta (Activo, Pasivo, Resultado)
- `WAERS` = Moneda
- `BUKRS` = Sociedad (Company Code)

---

### 2. CO - Controlling (Cost Accounting)

```
CO proporciona:
├─ Centros de Costo (Cost Centers)
├─ Órdenes Internas (Internal Orders)
├─ Elementos PEP (Proyectos)
├─ Contabilidad de Costos
└─ Análisis presupuestario
```

**Campos clave CO:**
- `KOSTL` = Centro de Costo
- `AUFNR` = Orden Interna
- `PSPID` = Elemento PEP (Project)
- `KTEXT` = Descripción

---

### 3. MM - Gestión de Materiales

```
MM proporciona:
├─ Catálogo de Materiales (Materiales)
├─ Stocks
├─ Órdenes de Compra
└─ Recepción de Bienes
```

**Campos clave MM:**
- `MATNR` = Número de Material
- `MATKL` = Clase de Material
- `MEINS` = Unidad de Medida

---

### 4. PS - Proyectos

```
PS proporciona:
├─ Estructura de Proyectos (WBS)
├─ Planificación de Proyectos
├─ Seguimiento de Costos
└─ Facturación de Proyectos
```

**Campos clave PS:**
- `PSPID` = ID de Proyecto
- `PSPNR` = Número interno de Proyecto
- `PBUKRS` = Sociedad del Proyecto

---

## 📊 MATRIZ DE MAPEO: INCISOS → SAP

### INCISO 1: PERSONAL

```
e-SIDIF: 1. PERSONAL
│
├─ Descripción: Gastos de personal (sueldos, salarios, bonificaciones)
│
├─ Características en SAP:
│  ├─ Documento: ENTRADA DE NÓMINA
│  ├─ Módulo: HR (Gestión de RRHH) + FI
│  ├─ Cuentas destino: Cuenta de Gasto Personal
│  ├─ Centro de Costo: Obligatorio (asigna a área)
│  └─ Orden Interna: Opcional (si es proyecto)
│
├─ Mapeo de Campos SAP:
│  ├─ Empleado (PERNR) → Beneficiario
│  ├─ Centro de Costo (KOSTL) → Aperturas Programáticas
│  ├─ Orden Interna (AUFNR) → Proyecto/Actividad
│  ├─ Cuenta Mayor (SAKNR) → Objeto Gasto: Personal (Inciso 1)
│  ├─ Importe (WRBTR) → Crédito presupuestario
│  └─ Sociedad (BUKRS) → Ente Contable
│
├─ Cuentas Mayor típicas:
│  ├─ 6100 - Gastos de Personal
│  ├─ 6110 - Sueldos y Salarios
│  ├─ 6120 - Bonificaciones
│  └─ 6130 - Contribuciones Sociales
│
├─ Contabilización típica:
│  ├─ DEBE: 6110 (Gasto de Sueldos)
│  ├─ HABER: 2100 (Salarios por Pagar)
│  └─ Centro de Costo: [Área responsable]
│
└─ Flujo:
   HR procesa nómina
     ↓
   FI registra gasto en cuenta 6110
     ↓
   CO acumula por centro de costo
     ↓
   e-SIDIF recibe: Inciso 1, importe, área
```

**Validación en e-SIDIF:**
```
Suma(Nóminas en SAP) = Suma(Inciso 1 en e-SIDIF)
```

---

### INCISO 2: BIENES CONSUMO

```
e-SIDIF: 2. BIENES CONSUMO
│
├─ Descripción: Bienes consumibles (papel, útiles, combustible, etc.)
│
├─ Características en SAP:
│  ├─ Documento: FACTURA DE COMPRA / NOTA DE RECEPCIÓN
│  ├─ Módulo: MM (Materiales) + FI
│  ├─ Cuentas destino: Gasto de Bienes Consumo
│  ├─ Centro de Costo: Obligatorio
│  └─ Orden Interna: Opcional (si es proyecto)
│
├─ Mapeo de Campos SAP:
│  ├─ Material (MATNR) → Descripción bien
│  ├─ Centro de Costo (KOSTL) → Aperturas Programáticas
│  ├─ Orden Interna (AUFNR) → Proyecto/Actividad
│  ├─ Cuenta Mayor (SAKNR) → Objeto Gasto: Bienes Consumo (Inciso 2)
│  ├─ Importe (MENGE × NETPR) → Crédito presupuestario
│  ├─ Proveedor (LIFNR) → (información auxiliar)
│  └─ Sociedad (BUKRS) → Ente Contable
│
├─ Cuentas Mayor típicas:
│  ├─ 6200 - Gastos de Bienes Consumo
│  ├─ 6210 - Útiles de Oficina
│  ├─ 6220 - Combustibles
│  ├─ 6230 - Repuestos
│  └─ 6240 - Otros Consumibles
│
├─ Contabilización típica (Factura):
│  ├─ DEBE: 6210 (Útiles de Oficina)
│  ├─ DEBE: IVA Soportado (1700)
│  ├─ HABER: 2100 (Proveedores por Pagar)
│  └─ Centro de Costo: [Área responsable]
│
├─ Contabilización típica (Recepción):
│  ├─ DEBE: Stock (Activo)
│  ├─ HABER: Proveedores (Pasivo)
│  └─ MM actualiza stock
│
└─ Flujo:
   MM recibe pedido de compra
     ↓
   Proveedor envía bienes
     ↓
   MM recibe y registra entrada
     ↓
   FI registra factura (gasto o stock)
     ↓
   e-SIDIF recibe: Inciso 2, importe, area
```

**Validación en e-SIDIF:**
```
Suma(Facturas de Bienes en SAP) = Suma(Inciso 2 en e-SIDIF)
```

---

### INCISO 3: SERVICIOS

```
e-SIDIF: 3. SERVICIOS
│
├─ Descripción: Servicios contratados (consultoría, limpieza, vigilancia, etc.)
│
├─ Características en SAP:
│  ├─ Documento: SOLICITUD DE SERVICIO / FACTURA DE SERVICIO
│  ├─ Módulo: MM (PS) + FI
│  ├─ Cuentas destino: Gasto de Servicios
│  ├─ Centro de Costo: Obligatorio
│  └─ Orden Interna: Obligatorio (servicios son proyectos)
│
├─ Mapeo de Campos SAP:
│  ├─ Material/Servicio (MATNR) → Tipo servicio
│  ├─ Centro de Costo (KOSTL) → Aperturas Programáticas
│  ├─ Orden Interna (AUFNR) → Proyecto/Servicio → CRÍTICO
│  ├─ Cuenta Mayor (SAKNR) → Objeto Gasto: Servicios (Inciso 3)
│  ├─ Importe (NETPR × MENGE) → Crédito presupuestario
│  ├─ Proveedor (LIFNR) → (información auxiliar)
│  └─ Sociedad (BUKRS) → Ente Contable
│
├─ Cuentas Mayor típicas:
│  ├─ 6300 - Gastos de Servicios
│  ├─ 6310 - Consultoría
│  ├─ 6320 - Vigilancia y Seguridad
│  ├─ 6330 - Limpieza
│  ├─ 6340 - Mantenimiento
│  └─ 6350 - Otros Servicios
│
├─ Contabilización típica:
│  ├─ DEBE: 6310 (Consultoría)
│  ├─ DEBE: IVA Soportado (1700)
│  ├─ HABER: 2100 (Proveedores por Pagar)
│  └─ Orden Interna: [Proyecto específico]
│
└─ Flujo:
   PS crea Orden Interna para servicio
     ↓
   MM crea solicitud de servicio
     ↓
   Proveedor entrega servicio
     ↓
   FI registra factura
     ↓
   CO acumula costo por orden interna
     ↓
   e-SIDIF recibe: Inciso 3, importe, proyecto
```

**Validación en e-SIDIF:**
```
Suma(Servicios en SAP) = Suma(Inciso 3 en e-SIDIF)
(Desglosado por proyecto)
```

---

### INCISO 4: BIENES USO (ACTIVOS FIJOS)

```
e-SIDIF: 4. BIENES USO
│
├─ Descripción: Bienes de uso (activos fijos, inmuebles, vehículos, equipos)
│
├─ Características en SAP:
│  ├─ Documento: ENTRADA DE ACTIVO FIJO
│  ├─ Módulo: AA (Activos Fijos) + FI
│  ├─ Cuentas destino: Activo (1200-1400)
│  ├─ Centro de Costo: Obligatorio
│  └─ Orden Interna: Opcional
│
├─ Mapeo de Campos SAP:
│  ├─ Activo (ANLN1 + ANLN2) → Identificador bien
│  ├─ Tipo Activo (ANLA) → Clase de bien
│  ├─ Centro de Costo (KOSTL) → Aperturas Programáticas
│  ├─ Orden Interna (AUFNR) → Proyecto (construcción, implementación)
│  ├─ Cuenta Mayor (SAKNR) → Clase Activo (1200-1400)
│  ├─ Importe (WERTV) → Costo de adquisición
│  ├─ Fecha (AKTIV) → Fecha de activación
│  └─ Sociedad (BUKRS) → Ente Contable
│
├─ Cuentas Mayor típicas:
│  ├─ 1200 - Bienes Muebles
│  ├─ 1210 - Vehículos
│  ├─ 1220 - Equipos Informáticos
│  ├─ 1230 - Mobiliario
│  ├─ 1300 - Inmuebles
│  └─ 1400 - Construcciones en Proceso
│
├─ Contabilización típica:
│  ├─ DEBE: 1210 (Vehículos) - Precio de compra
│  ├─ DEBE: IVA Soportado (1700)
│  ├─ HABER: 2100 (Proveedores por Pagar)
│  └─ Centro de Costo: [Área responsable]
│
├─ Depreciación posterior:
│  ├─ DEBE: 6400 (Gasto de Depreciación) - Mensual
│  ├─ HABER: 1220 (Depreciación Acumulada)
│  └─ Nota: Afecta a Inciso IMPLÍCITAMENTE (no es gasto directo)
│
└─ Flujo:
   MM/PS crea orden de compra de activo
     ↓
   Proveedor entrega activo
     ↓
   MM/AA recibe y activa en módulo AA
     ↓
   FI registra en cuenta de activo
     ↓
   AA calcula depreciación mensual
     ↓
   e-SIDIF recibe: Inciso 4 (inversión), gasto de depreciación implícita
```

**Validación en e-SIDIF:**
```
Suma(Activos Fijos adquiridos) = Suma(Inciso 4 en e-SIDIF)
Nota: Depreciación afecta incisos indirectamente
```

**⚠️ DESAFÍO:** Depreciación se registra como gasto pero es acumulativa en años

---

### INCISO 5: TRANSFERENCIAS

```
e-SIDIF: 5. TRANSFERENCIAS
│
├─ Descripción: Transferencias a otras entidades (subsidios, aportes, etc.)
│
├─ Características en SAP:
│  ├─ Documento: TRANSFERENCIA / PAGO
│  ├─ Módulo: FI + (HR si es a empleados)
│  ├─ Cuentas destino: Gasto de Transferencias (2600-2700)
│  ├─ Centro de Costo: Obligatorio
│  └─ Orden Interna: Opcional
│
├─ Mapeo de Campos SAP:
│  ├─ Beneficiario (BENE / BUKRS) → Entidad receptora
│  ├─ Centro de Costo (KOSTL) → Aperturas Programáticas
│  ├─ Cuenta Mayor (SAKNR) → Objeto Gasto: Transferencias (Inciso 5)
│  ├─ Importe (WRBTR) → Crédito presupuestario
│  ├─ Documento (BVORG) → Número de acto administrativo
│  └─ Sociedad (BUKRS) → Ente Contable origen
│
├─ Cuentas Mayor típicas:
│  ├─ 6500 - Transferencias Corrientes
│  ├─ 6510 - Subsidios a Instituciones
│  ├─ 6520 - Aportes a Fondos
│  ├─ 6600 - Transferencias de Capital
│  └─ 6610 - Aportes para Inversión
│
├─ Contabilización típica (Subsidio):
│  ├─ DEBE: 6510 (Subsidios)
│  ├─ HABER: 1100 (Banco) - al pagar
│  │ O HABER: 2100 (Proveedores) - al registrar
│  └─ Centro de Costo: [Entidad origen]
│
├─ Contabilización típica (Aporte):
│  ├─ DEBE: 6520 (Aportes a Fondos)
│  ├─ HABER: 1100 (Banco) - al pagar
│  └─ Orden Interna: [Proyecto conjunto si aplica]
│
└─ Flujo:
   Decisión política/presupuestaria
     ↓
   Se autoriza transferencia
     ↓
   FI registra compromiso (documento FI)
     ↓
   FI registra pago (cheque, transferencia)
     ↓
   Entidad receptora recibe fondos
     ↓
   e-SIDIF registra: Inciso 5, importe, beneficiario
```

**Validación en e-SIDIF:**
```
Suma(Transferencias pagadas en SAP) = Suma(Inciso 5 en e-SIDIF)
(Por beneficiario si es requerido)
```

---

### INCISO 6: ACTIVOS FINANCIEROS

```
e-SIDIF: 6. ACTIVOS FINANCIEROS
│
├─ Descripción: Activos de naturaleza financiera (inversiones, préstamos a terceros)
│
├─ Características en SAP:
│  ├─ Documento: INVERSIÓN / PRÉSTAMO
│  ├─ Módulo: TR (Tesorería) + FI
│  ├─ Cuentas destino: Activo Financiero (1500-1600)
│  ├─ Centro de Costo: Obligatorio
│  └─ Orden Interna: Opcional
│
├─ Mapeo de Campos SAP:
│  ├─ Inversión (ISIN / CUSIP) → Instrumento financiero
│  ├─ Centro de Costo (KOSTL) → Aperturas Programáticas
│  ├─ Cuenta Mayor (SAKNR) → Clase Activo Financiero
│  ├─ Importe (WERT) → Monto invertido
│  ├─ Fecha (DATS) → Fecha de inversión
│  ├─ Plazo (DATEN) → Fecha de vencimiento
│  └─ Sociedad (BUKRS) → Ente Contable
│
├─ Cuentas Mayor típicas:
│  ├─ 1500 - Inversiones Financieras Corto Plazo
│  ├─ 1510 - Valores Negociables
│  ├─ 1520 - Depósitos a Plazo
│  ├─ 1600 - Inversiones Largo Plazo
│  └─ 1610 - Préstamos Otorgados
│
├─ Contabilización típica (Inversión):
│  ├─ DEBE: 1510 (Valores Negociables)
│  ├─ HABER: 1100 (Banco) - al invertir
│  └─ Centro de Costo: [Área Tesorería]
│
├─ Intereses devengados:
│  ├─ DEBE: 1510 (Intereses por Cobrar)
│  ├─ HABER: 4100 (Ingreso por Intereses)
│  └─ Mensual
│
└─ Flujo:
   Decisión de invertir
     ↓
   TR negocia inversión
     ↓
   FI registra activo financiero
     ↓
   Periódicamente se reconocen intereses
     ↓
   Al vencer: se recupera principal
     ↓
   e-SIDIF recibe: Inciso 6 (inversión), ingresos (offset)
```

**Validación en e-SIDIF:**
```
Suma(Inversiones en SAP) = Suma(Inciso 6 en e-SIDIF)
Nota: Requiere reconciliación con ingresos financieros
```

**⚠️ DESAFÍO:** Puede tener componentes de ingresos (intereses)

---

### INCISO 7: DEUDA

```
e-SIDIF: 7. DEUDA
│
├─ Descripción: Pago de deuda pública (capital + intereses)
│
├─ Características en SAP:
│  ├─ Documento: PAGO DE DEUDA / ACREEDOR
│  ├─ Módulo: FI (Acreedores) + TR (Tesorería)
│  ├─ Cuentas destino: Pasivo (2000-2300)
│  ├─ Centro de Costo: Obligatorio
│  └─ Orden Interna: Opcional
│
├─ Mapeo de Campos SAP:
│  ├─ Deudor/Acreedor (LIFNR) → Entidad a la que se debe
│  ├─ Centro de Costo (KOSTL) → Aperturas Programáticas
│  ├─ Cuenta Mayor (SAKNR) → Clase Pasivo
│  ├─ Importe Total (WRBTR) → Pago realizado
│  ├─ Desglose:
│  │  ├─ Capital (KAPITAL) → Principal
│  │  ├─ Intereses (ZINS) → Gastos financieros
│  │  └─ Otros (AUTRES) → Comisiones
│  └─ Sociedad (BUKRS) → Ente Contable
│
├─ Cuentas Mayor típicas:
│  ├─ 2000 - Deuda a Largo Plazo
│  ├─ 2100 - Deuda a Corto Plazo
│  ├─ 6700 - Gastos Financieros
│  ├─ 6710 - Intereses de Deuda
│  └─ 6720 - Comisiones Financieras
│
├─ Contabilización típica (Pago de Deuda):
│  ├─ DEBE: 2000 (Deuda Largo Plazo) - Capital
│  ├─ DEBE: 6710 (Intereses) - Gastos
│  ├─ HABER: 1100 (Banco) - Pago total
│  └─ Acreedor: [Entidad prestamista]
│
├─ Contabilización de devengamiento (mensual):
│  ├─ DEBE: 6710 (Intereses)
│  ├─ HABER: 2100 (Intereses por Pagar)
│  └─ Mensual hasta próximo pago
│
└─ Flujo:
   Deuda contraída en período anterior
     ↓
   Mensualmente se reconocen intereses
     ↓
   En fecha de pago se registra total
     ↓
   Se paga desde tesorería
     ↓
   Se reducen pasivos
     ↓
   e-SIDIF recibe: Inciso 7 (desembolso), Inciso 3 (intereses como gasto)
```

**Validación en e-SIDIF:**
```
Suma(Pagos de Deuda en SAP) = Suma(Inciso 7 en e-SIDIF)
Nota: Incluye capital + intereses
Desglose recomendado en reportes
```

**⚠️ DESAFÍO CRÍTICO:** Separar capital de intereses para categorización correcta

---

### INCISO 8: OTROS

```
e-SIDIF: 8. OTROS
│
├─ Descripción: Otros gastos no clasificados en incisos 1-7
│
├─ Características en SAP:
│  ├─ Documento: VARIOS (depende del tipo)
│  ├─ Módulo: FI + (otros si aplica)
│  ├─ Cuentas destino: Gasto Varios
│  ├─ Centro de Costo: Obligatorio
│  └─ Orden Interna: Depende
│
├─ Ejemplos de gastos Inciso 8:
│  ├─ Indemnizaciones a empleados
│  ├─ Daños y perjuicios pagados
│  ├─ Gastos judiciales
│  ├─ Castigos (bienes obsoletos)
│  ├─ Ajustes contables
│  └─ Imprevistos
│
├─ Cuentas Mayor típicas:
│  ├─ 6800 - Gastos Varios
│  ├─ 6810 - Indemnizaciones
│  ├─ 6820 - Gastos Judiciales
│  ├─ 6830 - Castigos de Bienes
│  └─ 6840 - Otros
│
├─ Contabilización típica:
│  ├─ DEBE: 6810 (Indemnización)
│  ├─ HABER: 1100 (Banco) o 2100 (Acreedor)
│  └─ Centro de Costo: [Área responsable]
│
└─ Flujo:
   Evento no planificado / gasto extraordinario
     ↓
   Se requiere aprobación
     ↓
   FI registra documento
     ↓
   Se paga desde tesorería
     ↓
   e-SIDIF recibe: Inciso 8, importe, descripción
```

**Validación en e-SIDIF:**
```
Suma(Gastos Otros en SAP) = Suma(Inciso 8 en e-SIDIF)
Nota: Requiere seguimiento detallado por tipo
```

**⚠️ NOTA:** Inciso 8 debe minimizarse. Preferible clasificar correctamente en incisos 1-7

---

### INCISO 9: FIGURATIVOS

```
e-SIDIF: 9. FIGURATIVOS
│
├─ Descripción: Cuentas de orden (no afectan presupuesto real)
│
├─ Características en SAP:
│  ├─ Documento: ASIENTO DE ORDEN
│  ├─ Módulo: FI (Cuentas de Orden)
│  ├─ Cuentas destino: 8.x.x.x.x.x.x (Orden)
│  ├─ Centro de Costo: Obligatorio
│  └─ Orden Interna: Opcional
│
├─ Ejemplos de Figurativos:
│  ├─ Bienes en custodia
│  ├─ Garantías otorgadas/recibidas
│  ├─ Compromisos contingentes
│  ├─ Responsabilidades
│  ├─ Contingencias
│  └─ Documentos por cobrar/pagar
│
├─ Cuentas Mayor típicas:
│  ├─ 8000 - Bienes en Custodia
│  ├─ 8100 - Garantías Otorgadas
│  ├─ 8200 - Garantías Recibidas
│  ├─ 8300 - Compromisos Contingentes
│  └─ 8400 - Responsabilidades
│
├─ Contabilización típica (Garantía):
│  ├─ DEBE: 8100 (Garantía Otorgada)
│  ├─ HABER: 8100 (Contrapartida de orden)
│  └─ Nota: NO afecta activo/pasivo real
│
└─ Flujo:
   Evento que requiere seguimiento (no es gasto)
     ↓
   Se registra en cuenta de orden
     ↓
   Se reporta por transparencia
     ↓
   Cuando se resuelve, se reversa asiento
     ↓
   e-SIDIF recibe: Inciso 9, solo para información
```

**Validación en e-SIDIF:**
```
Inciso 9 NO afecta presupuesto real
Solo reporte de situación patrimonial contingente
```

**⚠️ NOTA:** Inciso 9 no debe impactar en cálculos de ejecución presupuestaria

---

## 📊 TABLA CONSOLIDADA DE MAPEO

| Inciso | Descripción | Módulo SAP | Cuenta Mayor Típica | Centro Costo | Orden Interna |
|--------|------------|-----------|-------------------|--------------|---------------|
| **1** | Personal | HR/FI | 6100-6130 | ✅ Obligatorio | ❌ Opcional |
| **2** | Bienes Consumo | MM/FI | 6200-6240 | ✅ Obligatorio | ❌ Opcional |
| **3** | Servicios | MM/PS/FI | 6300-6350 | ✅ Obligatorio | ✅ Obligatorio |
| **4** | Bienes Uso | AA/FI | 1200-1400 | ✅ Obligatorio | ❌ Opcional |
| **5** | Transferencias | FI | 6500-6600 | ✅ Obligatorio | ❌ Opcional |
| **6** | Activos Financieros | TR/FI | 1500-1600 | ✅ Obligatorio | ❌ Opcional |
| **7** | Deuda | FI/TR | 2000-2100, 6710 | ✅ Obligatorio | ❌ Opcional |
| **8** | Otros | FI | 6800-6840 | ✅ Obligatorio | ❌ Opcional |
| **9** | Figurativos | FI | 8000-8400 | ✅ Obligatorio | ❌ Opcional |

---

## 🔄 FLUJO INTEGRAL: SAP → e-SIDIF

```
┌─────────────────────────────────────────────────────────────────┐
│                     SISTEMAS OPERATIVOS SAP                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  HR (Nómina)          MM (Materiales)        PS (Proyectos)     │
│  └─ Documentos Nómina └─ Pedidos de compra  └─ Órdenes         │
│  └─ Sueldos/Salarios  └─ Recepción bienes   └─ Planificación   │
│  └─ Bonificaciones    └─ Facturas           └─ Proyectos       │
│                                                                   │
│  AA (Activos Fijos)   TR (Tesorería)        FI (Finanzas)      │
│  └─ Activos          └─ Inversiones        └─ Maestro Cuentas  │
│  └─ Depreciación     └─ Deuda              └─ Asientos         │
│  └─ Baja de activos  └─ Flujos de caja     └─ Reportes        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
         ┌──────────────────────────────────────┐
         │  LAYER DE INTEGRACIÓN (ETL)          │
         ├──────────────────────────────────────┤
         │                                      │
         │  1. Extracción de Documentos        │
         │     └─ Por tipo (nómina, factura)   │
         │                                      │
         │  2. Clasificación por Inciso        │
         │     └─ Mapeo cuentas SAP → incisos │
         │                                      │
         │  3. Agregación por Componente       │
         │     └─ Crédito, Recurso, etc.       │
         │                                      │
         │  4. Validación de Integridad        │
         │     └─ Sumas, referencias           │
         │                                      │
         │  5. Generación de Templates         │
         │     └─ Excel para cada componente   │
         │                                      │
         └──────────────────────────────────────┘
                            ↓
         ┌──────────────────────────────────────┐
         │    e-SIDIF PRESUPUESTO               │
         ├──────────────────────────────────────┤
         │                                      │
         │  ├─ 5 Componentes Escenario         │
         │  │  ├─ Crédito (Incisos 1-8)       │
         │  │  ├─ Recurso (Fuentes)            │
         │  │  ├─ Física Programa              │
         │  │  ├─ Física Proyecto              │
         │  │  └─ Financiera Proyecto          │
         │  │                                   │
         │  ├─ 9 Incisos Presupuestarios      │
         │  │  ├─ 1. Personal                  │
         │  │  ├─ 2. Bienes Consumo           │
         │  │  ├─ 3. Servicios                │
         │  │  ├─ 4. Bienes Uso               │
         │  │  ├─ 5. Transferencias           │
         │  │  ├─ 6. Activos Financieros      │
         │  │  ├─ 7. Deuda                    │
         │  │  ├─ 8. Otros                    │
         │  │  └─ 9. Figurativos              │
         │  │                                   │
         │  └─ Reportes de Ejecución          │
         │                                      │
         └──────────────────────────────────────┘
```

---

## ⚠️ DESAFÍOS IDENTIFICADOS

### 1. Mapeo Inciso 3 (Servicios) ↔ SAP

**Problema:**
- Servicios en SAP pueden ser:
  - Órdenes Internas (PS)
  - Materiales tipo Servicio (MM)
  - Facturas simples (FI)

**Solución:**
- Definir estándar: Todos los servicios → Órdenes Internas obligatorias
- Centro de Costo como referencia secundaria

### 2. Separación Inciso 7 (Deuda) - Capital vs Intereses

**Problema:**
- En SAP se registra pago total (capital + intereses)
- En e-SIDIF deben separarse:
  - Capital → Inciso 7
  - Intereses → Inciso 3 (Servicios)

**Solución:**
- En FI, crear estructura de deuda con tabla de amortización
- ETL debe desglosar automáticamente en carga

### 3. Inciso 4 (Bienes Uso) - Depreciación

**Problema:**
- Depreciación es gasto mensual
- Pero se registra en módulo AA automáticamente
- ¿Qué inciso afecta?

**Solución:**
- Depreciación → Inciso 3 (Servicios) o Inciso 8 (Otros)
- Recomendación: Crear Inciso específico o acumular en Servicios

### 4. Inciso 6 (Activos Financieros) - Intereses Ganados

**Problema:**
- Inversión es Inciso 6 (gasto)
- Intereses ganados son ingresos (contrastan)

**Solución:**
- Registrar inversión como Inciso 6 (gasto/uso de recursos)
- Intereses como ingresos aparte (offset)

### 5. Centro de Costo vs Aperturas Programáticas

**Problema:**
- SAP usa Centro de Costo (KOSTL)
- e-SIDIF usa Aperturas Programáticas (Programa.Subprograma.Actividad.Proyecto.Obra)
- Mapeo N:M complejo

**Solución:**
- Crear tabla de mapeo: Centro Costo ↔ Apertura Programática
- Mantener tabla actualizada
- En carga, expandir de KOSTL a aperturas

### 6. Múltiples Sociedades SAP → Un Ente e-SIDIF

**Problema:**
- ENACOM puede tener múltiples sociedades SAP
- Pero un ente en e-SIDIF
- ¿Cómo consolidar?

**Solución:**
- Definir matriz de consolidación
- En ETL, sumar gastos de todas las sociedades
- Reportar por componente

---

## ✅ RECOMENDACIONES PARA RELEVAMIENTO

### Fase 1: Diagnóstico de SAP (Semana 1-2)

**Preguntas a responder:**

1. **Estructura Organizacional**
   - ¿Cuántas sociedades (BUKRS) tiene ENACOM?
   - ¿Cuántos centros de costo (KOSTL)?
   - ¿Cuántas órdenes internas (AUFNR) activas?

2. **Plan de Cuentas SAP**
   - ¿Cuentas mayores activas (SAKNR) por rango?
   - ¿Definición de cada rango de cuentas?
   - ¿Existe documentación?

3. **Transacciones Típicas**
   - ¿Cómo se registra nómina (HR)?
   - ¿Cómo se registran facturas (MM)?
   - ¿Cómo se registran servicios (PS)?
   - ¿Cómo se registra deuda (TR)?

4. **Documentos**
   - ¿Qué tipos de documento existen?
   - ¿Con qué frecuencia se crean?
   - ¿Flujo de aprobación?

### Fase 2: Mapeo de Incisos (Semana 3-4)

**Trabajar con equipo SAP para:**

1. Crear matriz de Cuentas Mayor SAP → Incisos
2. Crear matriz de Centros de Costo → Aperturas Programáticas
3. Definir estándares de registro
4. Documentar excepciones

### Fase 3: Validación (Semana 5)

**Testing del mapeo:**

1. Extraer datos históricos de SAP
2. Aplicar mapeo
3. Comparar con presupuesto e-SIDIF existente
4. Ajustar reglas si hay discrepancias

---

## 📋 LISTA DE VERIFICACIÓN PARA RELEVAMIENTO

### Información a Recopilar

```
□ Plan de Cuentas SAP (todas las cuentas)
□ Catálogo de Centros de Costo
□ Catálogo de Órdenes Internas
□ Tabla de Materiales/Servicios
□ Estructura de Proyectos (WBS)
□ Tabla de Sociedades
□ Tabla de Acreedores/Deudores
□ Políticas de contabilización
□ Flujos de procesos por tipo de documento
□ Documentación de deuda pública
□ Documentación de activos fijos
□ Documentación de inversiones
□ Ejemplo de asientos contables reales
□ Últimas 3 cierres de año
□ Reportes de presupuesto históricos
```

### Contactos Necesarios

```
□ Responsable Módulo FI
□ Responsable Módulo CO
□ Responsable Módulo HR
□ Responsable Módulo MM
□ Responsable Módulo PS
□ Responsable Módulo AA
□ Responsable Módulo TR
□ Analista de Tesorería
□ Responsable de Presupuesto
□ Responsable de Auditoría
```

---

## 🎯 PRÓXIMOS DOCUMENTOS A CREAR

**Después de completar este relevamiento:**

1. `06_SAP_ESTRUCTURA_ENACOM.md` - Documentar estructura SAP específica de ENACOM
2. `07_MATRIZ_MAPEO_FINAL.md` - Mapeo definitivo Incisos ↔ SAP
3. `08_ETL_ESPECIFICACION.md` - Especificación de transformación de datos
4. `09_VALIDACION_TESTS.md` - Plan de testing del mapeo

---

**Documento preparado por:** Análisis para Etapa de Relevamiento  
**Estado:** BORRADOR (pendiente información de SAP ENACOM)  
**Próximo paso:** Recolectar información de equipo SAP de ENACOM
