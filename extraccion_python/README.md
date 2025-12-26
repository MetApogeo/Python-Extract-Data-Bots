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

El sistema extrae y estructura la siguiente información por cada persona encontrada:

- **Datos Personales**: Nombre, Inicial, Tipo (PAM/PCD).
- **Estado**: Status de persona, Status de cita.
- **Contacto**: Dirección completa, hasta 2 teléfonos.
- **Historial**: Estado del historial clínico, número de visitas.
- **Metadatos**: Archivo XML de origen.

> 📄 **Para ver un reporte detallado de una ejecución reciente**, consulta [docs/RESUMEN_EXTRACCION.md](docs/RESUMEN_EXTRACCION.md).
>
> 📋 **Para entender el formato exacto del Excel generado**, consulta [docs/FORMATO_EXCEL.md](docs/FORMATO_EXCEL.md).

## 📚 Documentación Completa

La carpeta `docs/` contiene guías detalladas para cada aspecto del sistema:

- **[README_EXTRACTOR.md](docs/README_EXTRACTOR.md)**: Documentación técnica profunda del script de extracción.
- **[PROYECTO_COMPLETADO.md](docs/PROYECTO_COMPLETADO.md)**: Reporte final de la extracción masiva (ejemplo de éxito).
- **[FORMATO_EXCEL.md](docs/FORMATO_EXCEL.md)**: Especificación de columnas y tipos de datos para el CSV/Excel.

## 🔧 Requisitos Técnicos

- **Python 3.6+**
- Módulos estándar únicamente (sin dependencias externas pesadas):
  - `xml.etree.ElementTree`, `json`, `csv`, `pathlib`, etc.

## 💡 Flujo de Trabajo Recomendado

1.  **Entrada**: Coloca tus archivos `view.xml` obtenidos de los dispositivos en la carpeta `views/`.
2.  **Procesamiento**: Ejecuta `scripts/extract_all_views.py` para procesar todo el lote.
3.  **Conversión**: El script generará automáticamente los JSON y CSV.
4.  **Análisis**: Usa `scripts/analyze_personas.py` para explorar los datos interactivamente.
5.  **Verificación**: Ejecuta `scripts/verificar_calidad.py` para asegurar la integridad de los datos.

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0
