#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar personas faltantes
Compara progreso.json con los archivos JSON existentes
"""

import os
import json
from pathlib import Path

# Rutas
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
PROGRESO_FILE = PROJECT_DIR / "progreso.json"
JSON_FOLDER = PROJECT_DIR / "json"


def sanitize_name(nombre):
    """Sanitiza el nombre igual que el bot"""
    import unicodedata
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


def main():
    print("="*60)
    print("BUSCAR PERSONAS FALTANTES")
    print("="*60)
    
    # Leer progreso.json
    with open(PROGRESO_FILE, 'r', encoding='utf-8') as f:
        progreso = json.load(f)
    
    personas_procesadas = set(progreso['procesados'])
    print(f"\n📋 Personas en progreso.json: {len(personas_procesadas)}")
    
    # Leer archivos JSON existentes
    json_files = list(JSON_FOLDER.glob("*.json"))
    nombres_con_archivo = set()
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                nombre = data.get('nombre', '')
                if nombre:
                    nombres_con_archivo.add(nombre)
        except Exception as e:
            print(f"⚠️  Error leyendo {json_file.name}: {e}")
    
    print(f"📂 Archivos JSON encontrados: {len(json_files)}")
    print(f"📝 Nombres únicos en JSONs: {len(nombres_con_archivo)}")
    
    # Encontrar faltantes
    faltantes = personas_procesadas - nombres_con_archivo
    
    if faltantes:
        print(f"\n❌ PERSONAS FALTANTES: {len(faltantes)}")
        print("="*60)
        for nombre in sorted(faltantes):
            nombre_archivo = sanitize_name(nombre)
            print(f"  - {nombre}")
            print(f"    Archivo esperado: {nombre_archivo}.json")
    else:
        print(f"\n✅ Todos los archivos están presentes")
    
    # Encontrar extras (archivos que no están en progreso.json)
    extras = nombres_con_archivo - personas_procesadas
    
    if extras:
        print(f"\n⚠️  ARCHIVOS EXTRA (no en progreso.json): {len(extras)}")
        print("="*60)
        for nombre in sorted(extras):
            print(f"  - {nombre}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
