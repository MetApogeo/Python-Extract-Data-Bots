#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir los archivos JSON de CURP a un archivo CSV

Lee todos los archivos JSON de la carpeta json/ y los convierte a un CSV
con dos columnas: nombre, CURP

Uso:
    python json_to_csv.py
"""

import os
import json
import csv
from pathlib import Path

# Rutas absolutas
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
JSON_FOLDER = PROJECT_DIR / "json"
CSV_FOLDER = PROJECT_DIR / "csv"
OUTPUT_CSV = CSV_FOLDER / "curps.csv"


def leer_json_files():
    """
    Lee todos los archivos JSON de la carpeta json/
    
    Returns:
        Lista de diccionarios con {nombre, curp}
    """
    datos = []
    
    if not JSON_FOLDER.exists():
        print(f"❌ Error: No existe la carpeta {JSON_FOLDER}")
        return datos
    
    # Obtener todos los archivos JSON
    json_files = list(JSON_FOLDER.glob("*.json"))
    
    if not json_files:
        print(f"⚠️  No se encontraron archivos JSON en {JSON_FOLDER}")
        return datos
    
    print(f"📂 Encontrados {len(json_files)} archivos JSON")
    
    # Leer cada archivo
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                nombre = data.get('nombre', '')
                curp = data.get('curp', '')
                
                # Solo agregar si tiene nombre (CURP puede ser None)
                if nombre:
                    datos.append({
                        'nombre': nombre,
                        'CURP': curp if curp else 'SIN CURP'
                    })
        
        except Exception as e:
            print(f"⚠️  Error al leer {json_file.name}: {e}")
    
    return datos


def guardar_csv(datos):
    """
    Guarda los datos en un archivo CSV
    
    Args:
        datos: Lista de diccionarios con {nombre, CURP}
    """
    # Crear carpeta csv si no existe
    CSV_FOLDER.mkdir(exist_ok=True)
    
    # Ordenar por nombre
    datos_ordenados = sorted(datos, key=lambda x: x['nombre'])
    
    # Escribir CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['nombre', 'CURP'])
        
        # Escribir encabezados
        writer.writeheader()
        
        # Escribir datos
        writer.writerows(datos_ordenados)
    
    print(f"✅ CSV guardado: {OUTPUT_CSV}")
    print(f"   Total de registros: {len(datos_ordenados)}")
    
    # Contar cuántos tienen CURP
    con_curp = sum(1 for d in datos_ordenados if d['CURP'] != 'SIN CURP')
    sin_curp = len(datos_ordenados) - con_curp
    
    print(f"   Con CURP: {con_curp}")
    print(f"   Sin CURP: {sin_curp}")


def main():
    """
    Función principal
    """
    print("="*60)
    print("CONVERTIR JSON A CSV")
    print("="*60)
    
    # Leer archivos JSON
    datos = leer_json_files()
    
    if not datos:
        print("❌ No hay datos para convertir")
        return
    
    # Guardar CSV
    guardar_csv(datos)
    
    print("="*60)
    print("✅ Conversión completada")
    print("="*60)


if __name__ == "__main__":
    main()
