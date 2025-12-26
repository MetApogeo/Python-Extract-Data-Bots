#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para capturar pantalla y extraer nombres con CURPs
Uso: python capturar_curps.py
"""

import os
import json
import xml.etree.ElementTree as ET
import subprocess
import unicodedata
from pathlib import Path
from datetime import datetime

# Rutas - Script se ejecuta desde carpeta base scrcpy-win64-v3.3.4
SCRIPT_DIR = Path(__file__).parent.resolve()  # extraccion_citas_hechas/scripts/
PROJECT_DIR = SCRIPT_DIR.parent  # extraccion_citas_hechas/
JSON_FOLDER = PROJECT_DIR / "json"  # extraccion_citas_hechas/json/
SCREEN_XML = PROJECT_DIR / "screen_temp.xml"  # Temporal en extraccion_citas_hechas/

# Detectar ruta de ADB (en la carpeta raíz scrcpy)
ADB_PATH = PROJECT_DIR.parent / "adb.exe"
ADB_CMD = f'"{ADB_PATH}"' if ADB_PATH.exists() else "adb"


def sanitize_name(nombre):
    """Sanitiza el nombre para usar como nombre de archivo"""
    # Remover acentos
    nombre_sin_acentos = ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    )
    # Reemplazar espacios y caracteres especiales
    nombre_limpio = nombre_sin_acentos.replace(' ', '_').replace('Ñ', 'N').replace('ñ', 'n')
    # Remover caracteres no alfanuméricos
    nombre_limpio = ''.join(c for c in nombre_limpio if c.isalnum() or c == '_')
    return nombre_limpio.upper()


def capturar_pantalla():
    """Captura la pantalla actual usando ADB"""
    print("📸 Capturando pantalla...")
    
    # Dump XML
    cmd_dump = f"{ADB_CMD} shell uiautomator dump /sdcard/screen.xml"
    result = subprocess.run(cmd_dump, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error al capturar pantalla: {result.stderr}")
        return False
    
    # Pull XML
    cmd_pull = f"{ADB_CMD} pull /sdcard/screen.xml {SCREEN_XML}"
    result = subprocess.run(cmd_pull, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error al descargar XML: {result.stderr}")
        return False
    
    print("✅ Pantalla capturada")
    return True


def extraer_personas_con_curp(xml_file):
    """
    Extrae nombres y CURPs del XML
    
    Busca patrones como:
    - Nombre en TextView (inmediatamente antes del CURP)
    - "CURP: XXXXXXXXXXXXXXXX" en TextView siguiente
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        personas = []
        
        # Buscar todos los TextView
        textviews = root.findall(".//node[@class='android.widget.TextView']")
        
        for i, node in enumerate(textviews):
            text = node.get("text", "").strip()
            
            # Buscar si el texto empieza con "CURP:"
            if text.startswith("CURP:"):
                # Extraer el CURP (después de "CURP: ")
                curp = text.replace("CURP:", "").strip()
                
                # El nombre debe estar INMEDIATAMENTE antes (i-1)
                if i > 0:
                    nombre_node = textviews[i-1]
                    nombre_text = nombre_node.get("text", "").strip()
                    
                    # Validar que sea un nombre válido:
                    # - Tiene espacios (nombre completo)
                    # - Tiene letras
                    # - NO tiene números
                    # - NO contiene palabras clave
                    if (len(nombre_text) > 5 and 
                        ' ' in nombre_text and 
                        any(c.isalpha() for c in nombre_text) and
                        not any(c.isdigit() for c in nombre_text) and
                        not any(x in nombre_text.lower() for x in ['curp', 'folio', 'resultado', 'visita', 'bitácora', '#'])):
                        
                        personas.append({
                            'nombre': nombre_text,
                            'curp': curp
                        })
        
        return personas
        
    except Exception as e:
        print(f"❌ Error al leer XML: {e}")
        return []


def guardar_json(persona):
    """Guarda la persona como archivo JSON"""
    nombre_limpio = sanitize_name(persona['nombre'])
    ruta_json = JSON_FOLDER / f"{nombre_limpio}.json"
    
    # Crear carpeta si no existe
    JSON_FOLDER.mkdir(exist_ok=True)
    
    # Guardar JSON
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(persona, f, ensure_ascii=False, indent=2)
    
    return ruta_json


def main():
    print("="*60)
    print("CAPTURAR PANTALLA Y EXTRAER CURPs")
    print("="*60)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Capturar pantalla
    if not capturar_pantalla():
        print("\n❌ No se pudo capturar la pantalla")
        return
    
    # 2. Extraer personas
    print("\n🔍 Buscando personas con CURP...")
    personas = extraer_personas_con_curp(SCREEN_XML)
    
    if not personas:
        print("⚠️  No se encontraron personas con CURP en la pantalla")
        return
    
    print(f"✅ Encontradas {len(personas)} personas")
    
    # 3. Guardar cada persona
    print("\n💾 Guardando archivos JSON...")
    for persona in personas:
        ruta = guardar_json(persona)
        print(f"  ✅ {persona['nombre']}")
        print(f"     CURP: {persona['curp']}")
        print(f"     Archivo: {ruta.name}")
    
    # 4. Limpiar archivo temporal
    if os.path.exists(SCREEN_XML):
        os.remove(SCREEN_XML)
    
    print("\n" + "="*60)
    print(f"✅ Proceso completado: {len(personas)} personas guardadas")
    print("="*60)


if __name__ == "__main__":
    main()
