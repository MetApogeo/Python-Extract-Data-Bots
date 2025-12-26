"""
Funciones auxiliares para el bot RPA
Incluye: sanitización de nombres, cálculo de coordenadas, manejo de ADB
"""

import os
import re
import time
import unicodedata
import xml.etree.ElementTree as ET
from typing import Optional, List, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# === RUTA BASE DEL PROYECTO ===
# Obtener la ruta raíz del proyecto (donde está adb.exe)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Sube 2 niveles: script -> extraccion_curp -> raíz
ADB_PATH = PROJECT_ROOT / "adb.exe"

# Verificar que adb.exe existe
if not ADB_PATH.exists():
    logger.warning(f"⚠️  adb.exe no encontrado en: {ADB_PATH}")
    logger.warning("   Usando 'adb' del PATH del sistema")
    ADB_CMD = "adb"
else:
    ADB_CMD = str(ADB_PATH)


def sanitize_name(name: str) -> str:
    """
    Limpia el nombre para que sea un archivo válido en Windows
    - Quita acentos y caracteres especiales
    - Convierte ñ a n
    - Reemplaza espacios por guiones bajos
    - Todo en mayúsculas
    
    Ejemplo: "JOSÉ MARÍA LÓPEZ" -> "JOSE_MARIA_LOPEZ"
    """
    # Normalizar unicode para quitar acentos
    nfkd = unicodedata.normalize('NFKD', name)
    name_sin_acentos = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    
    # Reemplazar ñ por n
    name_sin_acentos = name_sin_acentos.replace('Ñ', 'N').replace('ñ', 'n')
    
    # Eliminar caracteres especiales (solo dejar letras, números, espacios y guiones)
    name_limpio = re.sub(r'[^\w\s-]', '', name_sin_acentos).strip().upper()
    
    # Reemplazar múltiples espacios/guiones por uno solo
    name_limpio = re.sub(r'[-\s]+', '_', name_limpio)
    
    return name_limpio


def calculate_center(bounds_str: str) -> Optional[str]:
    """
    Convierte bounds '[x1,y1][x2,y2]' a coordenadas centrales 'x y'
    
    Args:
        bounds_str: String con formato '[100,200][300,400]'
    
    Returns:
        String con coordenadas centrales 'x y' o None si el formato es inválido
    
    Ejemplo: '[100,200][300,400]' -> '200 300'
    """
    try:
        # Extraer los 4 números del formato [x1,y1][x2,y2]
        match = re.findall(r'\[(\d+),(\d+)\]', bounds_str)
        
        if len(match) == 2:
            x1, y1 = int(match[0][0]), int(match[0][1])
            x2, y2 = int(match[1][0]), int(match[1][1])
            
            # Calcular el centro
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            return f"{center_x} {center_y}"
        else:
            logger.warning(f"Formato de bounds inválido: {bounds_str}")
            return None
    except Exception as e:
        logger.error(f"Error al calcular centro de bounds '{bounds_str}': {e}")
        return None


def safe_adb_command(cmd: str, max_retries: int = 3) -> bool:
    """
    Ejecuta comando ADB con reintentos automáticos
    
    Args:
        cmd: Comando ADB a ejecutar (sin el prefijo 'adb')
        max_retries: Número máximo de reintentos
    
    Returns:
        True si el comando se ejecutó exitosamente, False si falló
    """
    # Agregar la ruta completa de adb al comando
    full_cmd = f"{ADB_CMD} {cmd}"
    
    for attempt in range(max_retries):
        try:
            result = os.system(full_cmd)
            if result == 0:
                return True
            
            logger.warning(f"Intento {attempt + 1}/{max_retries} falló para: {full_cmd}")
            time.sleep(2)  # Esperar antes de reintentar
            
        except Exception as e:
            logger.error(f"Error en intento {attempt + 1}: {e}")
            time.sleep(2)
    
    logger.error(f"Comando ADB falló después de {max_retries} intentos: {full_cmd}")
    return False


def adb_tap(coordenadas: str, delay: float = 1.5) -> bool:
    """
    Ejecuta un tap en las coordenadas especificadas y espera
    
    Args:
        coordenadas: String con formato 'x y'
        delay: Segundos a esperar después del tap
    
    Returns:
        True si el tap se ejecutó exitosamente
    """
    cmd = f"shell input tap {coordenadas}"
    success = safe_adb_command(cmd)
    
    if success:
        time.sleep(delay)
    
    return success


def get_people_with_buttons(xml_path: str) -> List[Tuple[str, str]]:
    """
    Extrae nombres de personas y coordenadas de sus botones 'Visitar' desde el XML
    
    Estrategia: Buscar TextViews con nombres largos en mayúsculas,
    luego buscar el View clickable más cercano que contenga "Visitar"
    
    Args:
        xml_path: Ruta al archivo XML de la pantalla
    
    Returns:
        Lista de tuplas (nombre, coordenadas_boton)
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        people_buttons = []
        
        # Estrategia: Buscar todos los TextViews con nombres
        # Luego buscar Views clickables con "Visitar" que estén cerca
        
        # Primero, obtener todos los nombres potenciales
        nombres_encontrados = []
        for node in root.findall(".//node[@class='android.widget.TextView']"):
            text = node.get("text", "").strip()
            
            # Filtro: texto en mayúsculas, largo (>15 chars), con espacios
            if text and text.isupper() and len(text) >= 15 and ' ' in text:
                # Excluir textos del sistema
                if not any(keyword in text for keyword in ["Status", "HISTORIAL", "VISITA", "Registros", "Padron", "encontrados"]):
                    nombres_encontrados.append((text, node))
        
        logger.info(f"Nombres potenciales encontrados: {len(nombres_encontrados)}")
        
        # Ahora buscar botones "Visitar" clickables
        botones_visitar = []
        for node in root.findall(".//node[@class='android.view.View'][@clickable='true']"):
            # Verificar si contiene un TextView con "Visitar"
            for child in node.findall(".//node[@class='android.widget.TextView']"):
                if child.get("text", "").strip() == "Visitar":
                    bounds = node.get("bounds")
                    if bounds:
                        coords = calculate_center(bounds)
                        if coords:
                            botones_visitar.append((coords, node))
                            break
        
        logger.info(f"Botones 'Visitar' encontrados: {len(botones_visitar)}")
        
        # Emparejar nombres con botones (asumiendo que están en el mismo orden)
        min_length = min(len(nombres_encontrados), len(botones_visitar))
        
        for i in range(min_length):
            nombre = nombres_encontrados[i][0]
            coords = botones_visitar[i][0]
            people_buttons.append((nombre, coords))
            logger.info(f"✓ Emparejado: {nombre} -> {coords}")
        
        logger.info(f"Total emparejado: {len(people_buttons)} personas con botones")
        return people_buttons
        
    except Exception as e:
        logger.error(f"Error al parsear XML '{xml_path}': {e}", exc_info=True)
        return []


def dump_screen_xml(output_path: str = "screen.xml") -> bool:
    """
    Captura el XML de la pantalla actual usando uiautomator dump
    
    Args:
        output_path: Ruta local donde guardar el XML
    
    Returns:
        True si se capturó exitosamente
    """
    # Dump a la tablet
    if not safe_adb_command("shell uiautomator dump /sdcard/screen.xml"):
        return False
    
    # Pull a la PC
    if not safe_adb_command(f"pull /sdcard/screen.xml {output_path}"):
        return False
    
    # Verificar que el archivo existe y no está vacío
    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        logger.error(f"XML descargado está vacío o no existe: {output_path}")
        return False
    
    return True


def extraer_curp_de_xml(xml_path: str) -> Optional[str]:
    """
    Extrae el CURP del XML descargado
    
    Args:
        xml_path: Ruta al archivo XML
    
    Returns:
        String con el CURP o None si no se encuentra
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Buscar el nodo EditText que tiene el label "CURP"
        # En la estructura: primero hay un TextView con text="CURP", 
        # luego un EditText con el valor del CURP
        
        for node in root.findall(".//node[@class='android.widget.EditText']"):
            # Buscar si este EditText tiene un hijo TextView con text="CURP"
            for child in node.findall(".//node[@class='android.widget.TextView']"):
                if child.get("text", "").strip() == "CURP":
                    # El CURP está en el atributo text del EditText padre
                    curp = node.get("text", "").strip()
                    if curp and curp != "null" and len(curp) == 18:
                        logger.info(f"✓ CURP extraído: {curp}")
                        return curp
        
        # Método alternativo: buscar cualquier texto que parezca un CURP
        # CURP tiene 18 caracteres: 4 letras + 6 dígitos + 6 letras/dígitos + 2 dígitos
        curp_pattern = r'[A-Z]{4}\d{6}[A-Z0-9]{6}\d{2}'
        
        for node in root.findall(".//node"):
            text = node.get("text", "")
            match = re.search(curp_pattern, text)
            if match:
                curp = match.group(0)
                logger.info(f"✓ CURP extraído (patrón): {curp}")
                return curp
        
        logger.warning(f"No se encontró CURP en el XML: {xml_path}")
        return None
        
    except Exception as e:
        logger.error(f"Error al extraer CURP de '{xml_path}': {e}")
        return None


def verificar_xml_tiene_curp(xml_path: str) -> bool:
    """
    Verifica si el XML descargado contiene un CURP válido
    (Mantenida por compatibilidad, usa extraer_curp_de_xml internamente)
    
    Args:
        xml_path: Ruta al archivo XML
    
    Returns:
        True si contiene CURP
    """
    curp = extraer_curp_de_xml(xml_path)
    return curp is not None
