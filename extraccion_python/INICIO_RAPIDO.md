# 🚀 Inicio Rápido

## Extracción Completa en 2 Pasos

### Paso 1: Extraer datos de XML

```bash
cd scripts
python extract_all_views.py
```

**Resultado:**

- ✅ `json/personas.json` - Datos completos
- ✅ `csv/personas.csv` - CSV con todos los campos

### Paso 2: Generar formato Excel

```bash
python generar_excel.py
```

**Resultado:**

- ✅ `json/personas_excel.json` - Formato simplificado
- ✅ `csv/personas_excel.csv` - **Listo para Excel**

## 📊 Abrir en Excel

1. Abre Excel
2. Archivo → Abrir → `csv/personas_excel.csv`
3. ¡Listo! Verás la tabla con:
   - Nombre(s)
   - Paterno
   - Materno
   - Domicilio
   - Teléfono
   - No (VISITADO/RECHAZO/NO)

## 🔍 Verificar Calidad

```bash
cd scripts
python verificar_calidad.py
```

## 📈 Análisis Interactivo

```bash
cd scripts
python analyze_personas.py
```

## 📚 Más Información

Consulta `docs/` para documentación completa.
