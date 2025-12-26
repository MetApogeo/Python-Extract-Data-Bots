# 📊 Sistema de Extracción de Datos XML

Sistema completo para extraer, procesar y analizar información de personas desde archivos XML de Android.

## 📁 Estructura del Proyecto

```
extraccion_python/
├── scripts/          # Scripts Python
│   ├── extract_all_views.py    # Extractor principal
│   ├── generar_excel.py         # Generador formato Excel
│   ├── analyze_personas.py      # Análisis interactivo
│   └── verificar_calidad.py     # Verificación de calidad
│
├── views/            # Archivos XML de entrada
│   ├── view1.xml
│   ├── view2.xml
│   └── ... (66 archivos)
│
├── json/             # Archivos JSON generados
│   ├── personas.json            # Datos completos
│   └── personas_excel.json      # Formato Excel
│
├── csv/              # Archivos CSV generados
│   ├── personas.csv             # Datos completos
│   └── personas_excel.csv       # Formato Excel
│
└── docs/             # Documentación
    ├── README_EXTRACTOR.md
    ├── INICIO_RAPIDO.md
    ├── FORMATO_EXCEL.md
    ├── RESUMEN_EXTRACCION.md
    └── PROYECTO_COMPLETADO.md
```

## 🚀 Inicio Rápido

### 1. Extracción Completa

```bash
cd scripts
python extract_all_views.py
```

**Genera:**

- `json/personas.json` - Todos los campos
- `csv/personas.csv` - Todos los campos en CSV

### 2. Formato Excel

```bash
cd scripts
python generar_excel.py
```

**Genera:**

- `json/personas_excel.json` - Formato simplificado
- `csv/personas_excel.csv` - Listo para Excel

### 3. Verificar Calidad

```bash
cd scripts
python verificar_calidad.py
```

### 4. Análisis Interactivo

```bash
cd scripts
python analyze_personas.py
```

## 📊 Datos Extraídos

### Campos Completos (personas.json)

- `nombre` - Nombre completo
- `inicial` - Inicial del nombre
- `status_persona` - Estado de la persona
- `tipo_persona` - Tipo (PAM, PCD)
- `status_cita` - Estado de la cita
- `direccion` - Dirección completa
- `telefono_1` - Teléfono principal
- `telefono_2` - Teléfono secundario
- `historial_clinico` - Estado del historial
- `num_visitas` - Número de visitas
- `archivo_origen` - Archivo XML de origen

### Formato Excel (personas_excel.csv)

| Columna   | Descripción                     |
| --------- | ------------------------------- |
| Nombre(s) | Nombre(s) separado              |
| Paterno   | Apellido paterno                |
| Materno   | Apellido materno                |
| Domicilio | Dirección completa              |
| Teléfono  | Teléfono principal              |
| No        | Estado: VISITADO / RECHAZO / NO |

## 📈 Estadísticas Actuales

- **Total:** 281 personas únicas
- **VISITADO:** 144 (51.2%)
- **RECHAZO:** 15 (5.3%)
- **NO:** 122 (43.4%)

## 🎯 Estado de Visita

### ✅ VISITADO

Personas con 1 o más visitas exitosas

### 🔴 RECHAZO

Personas que rechazaron la visita

### ⚪ NO

Personas que aún no han sido visitadas

## 📚 Documentación Completa

Consulta la carpeta `docs/` para documentación detallada:

- **README_EXTRACTOR.md** - Guía completa del extractor
- **INICIO_RAPIDO.md** - Guía de inicio rápido
- **FORMATO_EXCEL.md** - Detalles del formato Excel
- **RESUMEN_EXTRACCION.md** - Estadísticas detalladas
- **PROYECTO_COMPLETADO.md** - Resumen del proyecto

## 🔧 Requisitos

- Python 3.6+
- Módulos estándar (incluidos con Python):
  - `xml.etree.ElementTree`
  - `json`
  - `csv`
  - `html`
  - `re`
  - `pathlib`
  - `collections`

## 💡 Flujo de Trabajo

```
1. Colocar archivos XML en views/
2. Ejecutar extract_all_views.py
3. Ejecutar generar_excel.py
4. Usar personas_excel.csv en Excel
```

## ⚙️ Características

- ✅ Procesamiento masivo de 66 archivos XML
- ✅ Detección automática de duplicados
- ✅ Conserva el registro más completo
- ✅ Filtra registros incompletos
- ✅ Detecta visitas rechazadas
- ✅ Genera múltiples formatos de salida
- ✅ Validación de calidad de datos
- ✅ Análisis interactivo

## 📝 Notas

- Los archivos CSV usan codificación UTF-8 con BOM para compatibilidad con Excel
- Los duplicados se manejan automáticamente conservando el registro más completo
- Los registros incompletos (menos de 2 campos) se ignoran automáticamente

---

**Última actualización:** Diciembre 2024  
**Versión:** 1.0
