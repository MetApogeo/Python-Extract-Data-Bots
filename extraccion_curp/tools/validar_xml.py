#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validación para verificar la integridad de los XMLs descargados
Genera un reporte de:
- Total de XMLs descargados
- XMLs con CURP detectado
- XMLs corruptos o vacíos
- XMLs sin CURP
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def validar_xml(xml_path: str) -> dict:
    """
    Valida un archivo XML individual
    
    Returns:
        Dict con: {
            'valido': bool,
            'tiene_curp': bool,
            'curp': str o None,
            'error': str o None
        }
    """
    result = {
        'valido': False,
        'tiene_curp': False,
        'curp': None,
        'error': None
    }
    
    try:
        # Verificar que el archivo existe y no está vacío
        if not os.path.exists(xml_path):
            result['error'] = "Archivo no existe"
            return result
        
        if os.path.getsize(xml_path) == 0:
            result['error'] = "Archivo vacío"
            return result
        
        # Intentar parsear el XML
        tree = ET.parse(xml_path)
        root = tree.getroot()
        result['valido'] = True
        
        # Buscar CURP (18 caracteres: 4 letras + 6 dígitos + 6 letras/dígitos + 2 dígitos)
        curp_pattern = r'[A-Z]{4}\d{6}[A-Z0-9]{6}\d{2}'
        
        for node in root.findall(".//node"):
            text = node.get("text", "")
            match = re.search(curp_pattern, text)
            if match:
                result['tiene_curp'] = True
                result['curp'] = match.group(0)
                break
        
        return result
        
    except ET.ParseError as e:
        result['error'] = f"XML corrupto: {e}"
        return result
    except Exception as e:
        result['error'] = f"Error: {e}"
        return result


def main():
    """Función principal de validación"""
    print("="*80)
    print("VALIDACIÓN DE XMLs DESCARGADOS")
    print("="*80)
    
    xml_folder = "../xml"
    
    if not os.path.exists(xml_folder):
        print(f"\n❌ La carpeta {xml_folder} no existe")
        return
    
    # Obtener todos los XMLs
    xml_files = list(Path(xml_folder).glob("*.xml"))
    
    if not xml_files:
        print(f"\n⚠️  No se encontraron archivos XML en {xml_folder}")
        return
    
    print(f"\n📁 Encontrados {len(xml_files)} archivos XML")
    print("\n🔍 Validando...\n")
    
    # Contadores
    total = len(xml_files)
    validos = 0
    con_curp = 0
    sin_curp = 0
    corruptos = 0
    
    # Listas para reporte detallado
    xmls_sin_curp = []
    xmls_corruptos = []
    
    # Validar cada XML
    for xml_file in xml_files:
        resultado = validar_xml(str(xml_file))
        
        if not resultado['valido']:
            corruptos += 1
            xmls_corruptos.append({
                'nombre': xml_file.name,
                'error': resultado['error']
            })
        else:
            validos += 1
            if resultado['tiene_curp']:
                con_curp += 1
            else:
                sin_curp += 1
                xmls_sin_curp.append(xml_file.name)
    
    # Reporte
    print("="*80)
    print("RESUMEN")
    print("="*80)
    print(f"Total de archivos:        {total}")
    print(f"  ✅ Válidos:             {validos} ({validos/total*100:.1f}%)")
    print(f"  ❌ Corruptos/Vacíos:    {corruptos} ({corruptos/total*100:.1f}%)")
    print(f"\n  📋 Con CURP detectado:  {con_curp} ({con_curp/total*100:.1f}%)")
    print(f"  ⚠️  Sin CURP:           {sin_curp} ({sin_curp/total*100:.1f}%)")
    
    # Detalles de XMLs sin CURP
    if xmls_sin_curp:
        print(f"\n{'='*80}")
        print(f"XMLs SIN CURP DETECTADO ({len(xmls_sin_curp)}):")
        print("="*80)
        for nombre in xmls_sin_curp[:10]:  # Mostrar solo los primeros 10
            print(f"  - {nombre}")
        if len(xmls_sin_curp) > 10:
            print(f"  ... y {len(xmls_sin_curp) - 10} más")
    
    # Detalles de XMLs corruptos
    if xmls_corruptos:
        print(f"\n{'='*80}")
        print(f"XMLs CORRUPTOS O CON ERRORES ({len(xmls_corruptos)}):")
        print("="*80)
        for item in xmls_corruptos[:10]:
            print(f"  - {item['nombre']}: {item['error']}")
        if len(xmls_corruptos) > 10:
            print(f"  ... y {len(xmls_corruptos) - 10} más")
    
    print("\n" + "="*80)
    
    # Guardar reporte en archivo
    reporte_path = "../reporte_validacion.txt"
    with open(reporte_path, 'w', encoding='utf-8') as f:
        f.write("REPORTE DE VALIDACIÓN DE XMLs\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total: {total}\n")
        f.write(f"Válidos: {validos}\n")
        f.write(f"Corruptos: {corruptos}\n")
        f.write(f"Con CURP: {con_curp}\n")
        f.write(f"Sin CURP: {sin_curp}\n\n")
        
        if xmls_sin_curp:
            f.write("XMLs SIN CURP:\n")
            for nombre in xmls_sin_curp:
                f.write(f"  - {nombre}\n")
            f.write("\n")
        
        if xmls_corruptos:
            f.write("XMLs CORRUPTOS:\n")
            for item in xmls_corruptos:
                f.write(f"  - {item['nombre']}: {item['error']}\n")
    
    print(f"📄 Reporte guardado en: {reporte_path}")


if __name__ == '__main__':
    main()
