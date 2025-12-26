# 🚀 Guía Rápida - Extractor de Personas

## Inicio Rápido

### 1. Extraer datos del XML

```bash
python extract_personas.py
```

**Salida:**

- `personas.json` - Datos en formato JSON
- `personas.csv` - Datos en formato CSV (compatible con Excel)

### 2. Analizar y filtrar datos

```bash
python analyze_personas.py
```

**Opciones disponibles:**

- Estadísticas generales
- Filtrar por tipo (PCD/PAM)
- Filtrar por status de cita
- Filtrar por historial clínico
- Buscar por nombre
- Y más...

## 📊 Datos Extraídos

Cada persona incluye:

| Campo               | Descripción          | Ejemplo                                            |
| ------------------- | -------------------- | -------------------------------------------------- |
| `nombre`            | Nombre completo      | ABEL ADAM MAURICIO HERNANDEZ                       |
| `inicial`           | Inicial del nombre   | A                                                  |
| `status_persona`    | Estado de la persona | ACTIVO                                             |
| `tipo_persona`      | Tipo de persona      | PCD, PAM                                           |
| `status_cita`       | Estado de la cita    | PENDIENTE                                          |
| `direccion`         | Dirección completa   | 73 DIAG X 24 Y 26 #, Col. COLONIA VICENTE SOLIS... |
| `telefono_1`        | Teléfono principal   | 9991575037                                         |
| `telefono_2`        | Teléfono secundario  | 9992340851                                         |
| `historial_clinico` | Estado del historial | COMPLETO, SIN HISTORIAL                            |
| `num_visitas`       | Número de visitas    | 0, 1, 2...                                         |

## 📁 Archivos del Proyecto

```
📂 scrcpy-win64-v3.3.4/
├── 📄 view.xml                    # Archivo XML de entrada
├── 🐍 extract_personas.py         # Script principal de extracción
├── 🐍 analyze_personas.py         # Script de análisis interactivo
├── 📋 README_EXTRACTOR.md         # Documentación completa
├── 📋 INICIO_RAPIDO.md           # Esta guía
├── 📊 personas.json               # Salida: datos en JSON
└── 📊 personas.csv                # Salida: datos en CSV
```

## 💡 Ejemplos de Uso

### Filtrar personas tipo PCD

```python
from analyze_personas import PersonaAnalyzer

analyzer = PersonaAnalyzer()
pcd_personas = analyzer.filter_by_tipo('PCD')
analyzer.save_filtered(pcd_personas, 'solo_pcd')
```

### Buscar por nombre

```python
analyzer = PersonaAnalyzer()
resultados = analyzer.search_by_name('ABEL')
analyzer.print_personas(resultados)
```

### Obtener estadísticas

```python
analyzer = PersonaAnalyzer()
stats = analyzer.get_estadisticas()
print(f"Total: {stats['total']}")
print(f"Con historial: {stats['por_historial']['COMPLETO']}")
```

## 🔧 Requisitos

- Python 3.6+
- No requiere librerías externas

## ❓ Ayuda

Para más información, consulta:

- `README_EXTRACTOR.md` - Documentación completa
- Ejecuta los scripts con `-h` o `--help` (próximamente)

## 📞 Soporte

Si encuentras algún problema:

1. Verifica que `view.xml` existe en el directorio
2. Asegúrate de ejecutar primero `extract_personas.py`
3. Revisa que el XML tenga la estructura esperada

---

**Creado para:** Aplicación Bienestar (com.bienestar.gob.mx)  
**Fecha:** Diciembre 2025
