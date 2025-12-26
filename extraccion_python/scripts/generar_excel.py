#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para transformar personas.json al formato Excel
Separa nombres en: Nombre(s), Paterno, Materno
Calcula el estado de visita: VISITADO, RECHAZO, NO
"""

import json
import csv
from typing import Dict, List, Tuple


def separar_nombre(nombre_completo: str) -> Tuple[str, str, str]:
    """
    Separa el nombre completo en: Nombre(s), Paterno, Materno
    Ejemplo: "MARIA GUADALUPE LOPEZ PEREZ" -> ("MARIA GUADALUPE", "LOPEZ", "PEREZ")
    """
    partes = nombre_completo.strip().split()
    
    if len(partes) == 0:
        return ("", "", "")
    elif len(partes) == 1:
        return (partes[0], "", "")
    elif len(partes) == 2:
        return (partes[0], partes[1], "")
    elif len(partes) == 3:
        return (partes[0], partes[1], partes[2])
    else:
        # 4 o más partes: los últimos 2 son apellidos, el resto es nombre
        materno = partes[-1]
        paterno = partes[-2]
        nombres = " ".join(partes[:-2])
        return (nombres, paterno, materno)


def calcular_estado_visita(persona: Dict[str, str]) -> str:
    """
    Calcula el estado de visita según las reglas:
    - RECHAZO: si historial contiene "RECHAZADA" (PRIORIDAD)
    - VISITADO: si num_visitas >= 1 y no está rechazado
    - NO: si num_visitas == 0 y no está rechazado
    
    IMPORTANTE: Se verifica PRIMERO si está rechazado, porque las personas
    rechazadas también tienen visitas (las visitas rechazadas).
    """
    # Obtener datos
    historial_texto = persona.get('historial_clinico', '')
    num_visitas_str = persona.get('num_visitas', '0')
    
    # Convertir num_visitas a entero de forma segura
    try:
        num_visitas = int(num_visitas_str)
    except (ValueError, TypeError):
        num_visitas = 0
    
    # PRIORIDAD 1: Verificar si fue rechazado
    # Buscar "RECHAZ" en el campo historial_clinico o en cualquier campo de texto
    if 'RECHAZ' in historial_texto.upper():
        return "RECHAZO"
    
    # Buscar también en el texto completo del registro por si acaso
    texto_completo = str(persona).upper()
    if 'RECHAZ' in texto_completo:
        return "RECHAZO"
    
    # PRIORIDAD 2: Si tiene visitas y NO está rechazado, fue visitado
    if num_visitas >= 1:
        return "VISITADO"
    
    # PRIORIDAD 3: Si no tiene visitas y no fue rechazado
    return "NO"


def transformar_para_excel(personas: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Transforma los datos al formato Excel
    """
    personas_excel = []
    
    for persona in personas:
        # Separar nombre
        nombres, paterno, materno = separar_nombre(persona.get('nombre', ''))
        
        # Calcular estado de visita
        estado_visita = calcular_estado_visita(persona)
        
        # Obtener teléfono o asignar "SIN NUMERO"
        telefono = persona.get('telefono_1', '').strip()
        if not telefono:
            telefono = 'SIN NUMERO'
        
        # Crear registro para Excel
        persona_excel = {
            'Nombre(s)': nombres,
            'Paterno': paterno,
            'Materno': materno,
            'Domicilio': persona.get('direccion', ''),
            'Teléfono': telefono,
            'No': estado_visita
        }
        
        personas_excel.append(persona_excel)
    
    return personas_excel


def main():
    """Función principal"""
    print("="*80)
    print("GENERADOR DE FORMATO EXCEL")
    print("Transforma personas.json al formato de la tabla Excel")
    print("="*80)
    
    # Cargar datos originales
    try:
        with open('../json/personas.json', 'r', encoding='utf-8') as f:
            personas = json.load(f)
        print(f"\n✓ Cargadas {len(personas)} personas desde json/personas.json")
    except FileNotFoundError:
        print("\n✗ No se encontró json/personas.json")
        print("  Ejecuta primero extract_all_views.py")
        return
    except Exception as e:
        print(f"\n✗ Error al cargar personas.json: {e}")
        return
    
    # Transformar datos
    print("\n🔄 Transformando datos al formato Excel...")
    personas_excel = transformar_para_excel(personas)
    
    # Guardar JSON
    try:
        with open('../json/personas_excel.json', 'w', encoding='utf-8') as f:
            json.dump(personas_excel, f, ensure_ascii=False, indent=2)
        print(f"✓ Guardado json/personas_excel.json ({len(personas_excel)} registros)")
    except Exception as e:
        print(f"✗ Error al guardar JSON: {e}")
    
    # Guardar CSV
    try:
        fieldnames = ['Nombre(s)', 'Paterno', 'Materno', 'Domicilio', 'Teléfono', 'No']
        
        with open('../csv/personas_excel.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(personas_excel)
        
        print(f"✓ Guardado csv/personas_excel.csv ({len(personas_excel)} registros)")
    except Exception as e:
        print(f"✗ Error al guardar CSV: {e}")
    
    # Mostrar estadísticas
    print("\n" + "="*80)
    print("ESTADÍSTICAS")
    print("="*80)
    
    visitados = sum(1 for p in personas_excel if p['No'] == 'VISITADO')
    rechazos = sum(1 for p in personas_excel if p['No'] == 'RECHAZO')
    no_visitados = sum(1 for p in personas_excel if p['No'] == 'NO')
    
    print(f"Total de personas: {len(personas_excel)}")
    print(f"  - VISITADO: {visitados} ({visitados/len(personas_excel)*100:.1f}%)")
    print(f"  - RECHAZO: {rechazos} ({rechazos/len(personas_excel)*100:.1f}%)")
    print(f"  - NO: {no_visitados} ({no_visitados/len(personas_excel)*100:.1f}%)")
    
    print("\n✓ Archivos generados:")
    print("  - json/personas_excel.json")
    print("  - csv/personas_excel.csv (listo para abrir en Excel)")
    print("\n" + "="*80)


if __name__ == '__main__':
    main()
