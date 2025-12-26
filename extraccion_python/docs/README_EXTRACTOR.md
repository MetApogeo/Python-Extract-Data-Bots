# Extractor de Información de Personas - view.xml

Script en Python para extraer información de personas desde archivos XML de jerarquía de UI de Android.

## 📋 Descripción

Este script procesa archivos `view.xml` generados por herramientas de inspección de UI de Android (como UI Automator) y extrae información estructurada de personas, incluyendo:

- **Nombre completo**
- **Inicial**
- **Status de la persona** (ACTIVO, INACTIVO, etc.)
- **Tipo de persona** (PCD, PAM, etc.)
- **Status de cita** (PENDIENTE, COMPLETADA, etc.)
- **Dirección completa**
- **Teléfonos** (hasta 2 números)
- **Historial clínico** (COMPLETO, SIN HISTORIAL, PARCIAL)
- **Número de visitas**

## 🚀 Uso

### Requisitos

- Python 3.6 o superior
- No requiere librerías externas (solo usa módulos estándar de Python)

### Ejecución

1. Asegúrate de tener el archivo `view.xml` en el mismo directorio que el script
2. Ejecuta el script:

```bash
python extract_personas.py
```

### Salida

El script genera dos archivos:

1. **`personas.json`** - Formato JSON con toda la información estructurada
2. **`personas.csv`** - Formato CSV compatible con Excel

## 📊 Ejemplo de Salida

### JSON

```json
[
  {
    "nombre": "ABEL ADAM MAURICIO HERNANDEZ",
    "inicial": "A",
    "status_persona": "ACTIVO",
    "tipo_persona": "PCD",
    "status_cita": "PENDIENTE",
    "direccion": "73 DIAG X 24 Y 26 #, Col. COLONIA VICENTE SOLIS, Mun. MERIDA, Edo. YUCATAN,",
    "telefono_1": "9991575037",
    "telefono_2": "",
    "historial_clinico": "SIN HISTORIAL",
    "num_visitas": "0"
  }
]
```

### Resumen en Consola

El script también muestra un resumen estadístico:

```
================================================================================
RESUMEN DE EXTRACCIÓN
================================================================================
Total de personas: 6

Por tipo de persona:
  - PAM: 3
  - PCD: 2
  - SIN TIPO: 1

Por status de cita:
  - PENDIENTE: 5
  - SIN STATUS: 1

Historial clínico:
  - Con historial completo: 1
  - Sin historial: 4

Total de visitas registradas: 1
```

## 🔧 Personalización

### Cambiar el archivo de entrada

Edita la variable `xml_file` en la función `main()`:

```python
xml_file = 'tu_archivo.xml'
```

### Cambiar los nombres de salida

Modifica las llamadas a los métodos de guardado:

```python
extractor.save_to_json('mi_salida.json')
extractor.save_to_csv('mi_salida.csv')
```

## 🔍 Análisis de Datos

Una vez extraídos los datos, puedes usar el script `analyze_personas.py` para filtrar y analizar la información:

```bash
python analyze_personas.py
```

### Funcionalidades del Analizador

El script interactivo te permite:

1. **Ver estadísticas generales** - Resumen completo con porcentajes
2. **Filtrar por tipo** - Separar PCD, PAM, etc.
3. **Filtrar por status de cita** - PENDIENTE, COMPLETADA, etc.
4. **Filtrar por historial** - Con o sin historial clínico
5. **Filtrar por visitas** - Personas que tienen visitas registradas
6. **Filtrar por teléfonos** - Sin teléfono o con 2 teléfonos
7. **Buscar por nombre** - Búsqueda parcial de nombres
8. **Guardar resultados filtrados** - Exportar subconjuntos en JSON y CSV

### Ejemplo de Uso

```
MENÚ DE ANÁLISIS DE PERSONAS
================================================================================

1.  Ver estadísticas generales
2.  Filtrar por tipo de persona (PCD/PAM)
3.  Filtrar por status de cita
...

Selecciona una opción: 2
Ingresa el tipo (PCD/PAM): PCD

Mostrando 2 de 2 personas:
--------------------------------------------------------------------------------

1. ABEL ADAM MAURICIO HERNANDEZ
   Tipo: PCD
   Status Cita: PENDIENTE
   Tel: 9991575037
   Historial: SIN HISTORIAL - 0 visita(s)

¿Guardar resultados? (s/n): s
✓ Guardados 2 registros en:
  - personas_tipo_pcd.json
  - personas_tipo_pcd.csv
```

## 📝 Estructura del Código

### extract_personas.py

- **`PersonaExtractor`**: Clase principal que maneja la extracción
  - `parse_info_text()`: Parsea información de status y dirección
  - `parse_historial_text()`: Parsea información de historial clínico
  - `extract_personas()`: Método principal de extracción
  - `save_to_json()`: Guarda datos en formato JSON
  - `save_to_csv()`: Guarda datos en formato CSV
  - `print_summary()`: Muestra resumen estadístico

### analyze_personas.py

- **`PersonaAnalyzer`**: Clase para análisis y filtrado
  - `filter_by_tipo()`: Filtra por tipo de persona
  - `filter_by_status_cita()`: Filtra por status de cita
  - `filter_con_historial()`: Filtra personas con historial completo
  - `filter_sin_historial()`: Filtra personas sin historial
  - `search_by_name()`: Búsqueda por nombre
  - `get_estadisticas()`: Genera estadísticas detalladas
  - `save_filtered()`: Guarda resultados filtrados

## ⚠️ Notas

- El script asume que el XML sigue la estructura de UI Automator de Android
- Los nombres deben estar en MAYÚSCULAS para ser detectados
- El script decodifica automáticamente entidades HTML (como `&#10;` para saltos de línea)
- Si una persona no tiene toda la información, los campos faltantes quedarán vacíos

## 🐛 Solución de Problemas

### No se extraen personas

- Verifica que el archivo `view.xml` existe en el directorio
- Asegúrate de que el XML contiene nodos `<node class="android.widget.TextView">`

### Información incompleta

- Algunos campos pueden estar vacíos si no se encuentran en el XML
- Revisa que el formato del texto en el XML coincida con los patrones esperados

### Error de encoding

- El script usa UTF-8 por defecto
- Para CSV, usa UTF-8 con BOM para compatibilidad con Excel

## 📄 Licencia

Este script es de uso libre para propósitos educativos y de desarrollo.

## 👤 Autor

Creado para extraer información de la aplicación de Bienestar (com.bienestar.gob.mx)

---

**Última actualización**: Diciembre 2025
