#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar CURPs en archivos JSON
Encuentra archivos JSON que tengan CURP null, vacío o "SIN CURP"
"""

import os
import json
from pathlib import Path

# Rutas
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
JSON_FOLDER = PROJECT_DIR / "json"


def main():
    print("="*60)
    print("VERIFICAR CURPs EN ARCHIVOS JSON")
    print("="*60)
    
    # Leer archivos JSON
    json_files = list(JSON_FOLDER.glob("*.json"))
    print(f"\n📂 Total de archivos JSON: {len(json_files)}")
    
    sin_curp = []
    con_curp = []
    errores = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                nombre = data.get('nombre', 'DESCONOCIDO')
                curp = data.get('curp')
                
                # Verificar si tiene CURP válido
                if curp is None or curp == '' or curp == 'SIN CURP':
                    sin_curp.append({
                        'archivo': json_file.name,
                        'nombre': nombre,
                        'curp': curp
                    })
                else:
                    con_curp.append({
                        'archivo': json_file.name,
                        'nombre': nombre,
                        'curp': curp
                    })
        
        except Exception as e:
            errores.append({
                'archivo': json_file.name,
                'error': str(e)
            })
    
    # Mostrar resultados
    print(f"\n✅ Con CURP válido: {len(con_curp)}")
    print(f"❌ Sin CURP: {len(sin_curp)}")
    
    if errores:
        print(f"⚠️  Errores al leer: {len(errores)}")
    
    # Mostrar detalles de los que no tienen CURP
    if sin_curp:
        print("\n" + "="*60)
        print("ARCHIVOS SIN CURP:")
        print("="*60)
        for item in sin_curp:
            print(f"\n📄 {item['archivo']}")
            print(f"   Nombre: {item['nombre']}")
            print(f"   CURP: {item['curp']}")
    else:
        print("\n🎉 ¡Todos los archivos tienen CURP válido!")
    
    # Mostrar errores si hay
    if errores:
        print("\n" + "="*60)
        print("ERRORES:")
        print("="*60)
        for item in errores:
            print(f"\n📄 {item['archivo']}")
            print(f"   Error: {item['error']}")
    
    print("\n" + "="*60)
    print("RESUMEN:")
    print(f"  Total: {len(json_files)}")
    print(f"  Con CURP: {len(con_curp)}")
    print(f"  Sin CURP: {len(sin_curp)}")
    print(f"  Errores: {len(errores)}")
    print("="*60)


if __name__ == "__main__":
    main()
