#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para reiniciar el caché del bot
Borra progreso.json y todos los archivos JSON descargados
"""

import os
from pathlib import Path

# Rutas absolutas
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
PROGRESO_FILE = PROJECT_DIR / "progreso.json"
JSON_FOLDER = PROJECT_DIR / "json"

print("="*60)
print("REINICIAR CACHÉ DEL BOT")
print("="*60)

# Borrar progreso.json
if PROGRESO_FILE.exists():
    os.remove(PROGRESO_FILE)
    print(f"✅ Borrado: {PROGRESO_FILE}")
else:
    print(f"⚠️  No existe: {PROGRESO_FILE}")

# Borrar JSONs
if JSON_FOLDER.exists():
    json_files = list(JSON_FOLDER.glob("*.json"))
    if json_files:
        for json_file in json_files:
            os.remove(json_file)
        print(f"✅ Borrados {len(json_files)} archivos JSON")
    else:
        print(f"⚠️  No hay JSONs para borrar")
else:
    print(f"⚠️  No existe carpeta: {JSON_FOLDER}")

print("\n✅ Caché reiniciado completamente")
print("="*60)
