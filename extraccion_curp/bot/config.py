"""
Configuración centralizada del bot RPA
Todos los delays, coordenadas y parámetros configurables
"""

from pathlib import Path

# === RUTAS BASE ===
# Obtener la ruta del script actual
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent  # extraccion_curp/

# === OBJETIVO ===
TOTAL_OBJETIVO = 230

# === DELAYS (en segundos) ===
DELAY_CARGA_DATOS = 8      # Espera después de "Iniciar visita" para que carguen datos
DELAY_SIGUIENTE = 2         # Espera después de "Siguiente" para que cargue pantalla CURP
DELAY_TAP_DEFAULT = 1     # Delay por defecto entre taps
DELAY_FILTRO_CARGA = 1      # Espera después de aplicar filtro para que cargue lista
DELAY_SCROLL = 1.5            # Espera después de hacer scroll

# === COORDENADAS FIJAS (Menú Principal) ===
# Estas coordenadas son FIJAS y siempre las mismas
BTN_INICIO = "92 1155"
BTN_VISITAR_MENU = "259 208"  # Solo para entrar al padrón desde menú principal
BTN_FILTRO = "723 242"
BTN_VALOR_TODOS = "463 516"
BTN_TODOS_OPCION = "329 688"  # Opción "Sin visita" en el filtro
BTN_APLICAR_FILTRO = "476 221"

# === COORDENADAS DE FLUJO INTERNO ===
# Estas se usan DESPUÉS de hacer clic en el botón "Visitar" de una persona
BTN_INICIAR_VISITA = "648 157"
BTN_SIGUIENTE = "694 1063"

# === COMANDO DE SCROLL ===
SCROLL_COMMAND = "adb shell input swipe 290 1055 290 400 1100"

# === RUTAS (ABSOLUTAS) ===
FOLDER_XML = str(PROJECT_DIR / "xml")
FOLDER_JSON = str(PROJECT_DIR / "json")
CHECKPOINT_FILE = str(PROJECT_DIR / "progreso.json")
LOG_FILE = str(PROJECT_DIR / "bot.log")
SCREEN_XML_TEMP = "screen.xml"
CURP_XML_TEMP = "/sdcard/temp_curp.xml"

# === CONFIGURACIÓN ADB ===
MAX_RETRIES_ADB = 3
ADB_TIMEOUT = 10

# === FILTROS DE DETECCIÓN DE NOMBRES ===
MIN_NOMBRE_LENGTH = 15      # Mínimo de caracteres para considerar un texto como nombre
NOMBRE_DEBE_TENER_ESPACIOS = True  # Los nombres deben tener espacios
