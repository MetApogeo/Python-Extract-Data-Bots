# 🤖 Bot RPA - Extracción de CURP

Bot automatizado para extraer 526 registros de CURP desde tablet Android (Qtab_LTE) vía ADB.

## 📁 Estructura del Proyecto

```
extraccion_curp/
├── script/
│   ├── bot_padron.py       # ⭐ Script principal del bot
│   ├── config.py            # Configuración (delays, coordenadas)
│   ├── utils.py             # Funciones auxiliares
│   └── validar_xml.py       # Validación de XMLs descargados
├── xml/                     # XMLs descargados (generado)
├── docs/
│   ├── comandos.md          # Comandos ADB detallados
│   └── especificaciones.md  # Especificaciones técnicas
├── progreso.json            # Checkpoint (generado)
└── bot.log                  # Log de ejecución (generado)
```

## 🚀 Inicio Rápido

### Requisitos Previos

1. **Tablet conectada vía ADB**:

   ```bash
   adb devices
   ```

   Debe mostrar: `Qtab_LTE device`

2. **Python 3.6+** instalado

### Ejecución

```bash
cd script
python bot_padron.py
```

## ⚙️ Configuración

Edita `script/config.py` para ajustar:

- `TOTAL_OBJETIVO`: Número de registros a extraer (default: 526)
- `DELAY_CARGA_DATOS`: Espera después de "Iniciar visita" (default: 8s)
- `DELAY_SIGUIENTE`: Espera antes de capturar XML (default: 2s)

## 🔄 Flujo del Bot

1. **Aplicar Filtros**: Navega al padrón y aplica filtro "TODOS"
2. **Detectar Personas**: Captura XML de pantalla y extrae nombres + coordenadas de botones
3. **Procesar Persona**:
   - Clic en botón "Visitar" (coordenadas dinámicas)
   - Clic en "Iniciar visita" → Espera 8s
   - Clic en "Siguiente" → Espera 2s
   - Captura XML del CURP
   - Descarga a `xml/NOMBRE_PERSONA.xml`
   - Regresa al inicio
4. **Scroll**: Si no hay personas nuevas, hace scroll
5. **Checkpoint**: Guarda progreso cada 10 registros

## 📊 Características

### ✅ Coordenadas Dinámicas

- **NO usa coordenadas fijas** para los botones "Visitar"
- Extrae coordenadas desde el XML de la pantalla usando `bounds`
- Calcula el centro del botón automáticamente

### ✅ Sistema de Checkpoint

- Guarda progreso en `progreso.json`
- Si el bot se detiene, continúa desde donde quedó
- No reprocesa personas ya descargadas

### ✅ Manejo Robusto de Errores

- Reintentos automáticos en comandos ADB
- Validación de XMLs descargados
- Logging detallado en `bot.log`

### ✅ Sanitización de Nombres

- Quita acentos: `JOSÉ` → `JOSE`
- Quita ñ: `PEÑA` → `PENA`
- Reemplaza espacios: `JUAN PEREZ` → `JUAN_PEREZ.xml`

## 🧪 Validación

Después de ejecutar el bot, valida los XMLs descargados:

```bash
cd script
python validar_xml.py
```

Genera un reporte con:

- Total de XMLs descargados
- XMLs con CURP detectado
- XMLs corruptos o vacíos

## 📝 Logs

El bot genera logs detallados en `bot.log`:

```
2024-12-24 13:35:00 - INFO - 🤖 BOT RPA - EXTRACCIÓN DE CURP
2024-12-24 13:35:01 - INFO - Aplicando filtros...
2024-12-24 13:35:10 - INFO - 👥 Detectadas 5 personas en pantalla
2024-12-24 13:35:11 - INFO - 📝 Procesando (1/526): JUAN PEREZ LOPEZ
2024-12-24 13:35:25 - INFO -    ✅ Completado: JUAN_PEREZ_LOPEZ.xml
```

## 🛑 Detener el Bot

- **Ctrl+C**: Detiene el bot de forma segura
- El progreso se guarda automáticamente
- Al reiniciar, continúa desde donde quedó

## ⚠️ Notas Importantes

> [!WARNING] > **Coordenadas Dinámicas**: El bot extrae las coordenadas del botón "Visitar" de cada persona desde el XML. NO uses coordenadas fijas.

> [!IMPORTANT] > **Delays**: Los delays están configurados para Mérida (clima puede afectar velocidad). Ajusta en `config.py` si es necesario.

> [!TIP] > **Prueba Inicial**: Antes de ejecutar los 526 registros, prueba con 5 cambiando `TOTAL_OBJETIVO = 5` en `config.py`.

## 🔧 Troubleshooting

### "No se detectaron personas en la pantalla"

- Verifica que la tablet esté en la lista de personas
- Revisa que el filtro "TODOS" esté aplicado
- Aumenta `DELAY_FILTRO_CARGA` en `config.py`

### "Falló tap en botón Visitar"

- Verifica conexión ADB: `adb devices`
- Revisa que la función `get_people_with_buttons()` esté extrayendo coordenadas correctas

### "XML descargado pero sin CURP detectado"

- Verifica que la pantalla del CURP se haya cargado completamente
- Aumenta `DELAY_SIGUIENTE` en `config.py`

## 📚 Documentación Adicional

- `docs/comandos.md`: Comandos ADB detallados por fase
- `docs/especificaciones.md`: Especificaciones técnicas del proyecto

---

**Versión**: 1.0  
**Última actualización**: Diciembre 2024
