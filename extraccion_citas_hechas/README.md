# Extracción de CURPs de Citas Hechas

Script simple para capturar la pantalla de "VISITAS" y extraer nombres con CURPs.

## Uso

1. Asegúrate de que la tablet esté conectada y en la pantalla de visitas
2. Desde la carpeta base `scrcpy-win64-v3.3.4`, ejecuta:

```bash
python extraccion_citas_hechas/scripts/capturar_curps.py
```

3. El script hará:
   - Captura de pantalla con ADB
   - Lectura del XML
   - Búsqueda de nombres y CURPs
   - Guardado de cada persona como JSON en `json/`

## Estructura

```
extraccion_citas_hechas/
├── scripts/
│   └── capturar_curps.py    # Script principal
├── json/                     # JSONs generados (nombre + CURP)
└── README.md                 # Este archivo
```

## Ejemplo de salida

Cada archivo JSON contiene:

```json
{
  "nombre": "ADDA RUTH LUGO LEAL",
  "curp": "LULA630713MYNGLDA04"
}
```

## Notas

- Este NO es un bot, es un script de una sola ejecución
- Ejecuta el script cada vez que quieras capturar la pantalla actual
- Los archivos JSON se guardan con el nombre sanitizado de la persona
