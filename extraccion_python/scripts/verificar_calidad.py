#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación de calidad de datos
Analiza personas.json y genera un reporte de calidad
"""

import json
from collections import Counter
from typing import List, Dict


def load_personas(filename: str = 'personas.json') -> List[Dict]:
    """Carga el archivo de personas"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def verificar_duplicados(personas: List[Dict]) -> Dict:
    """Verifica si hay nombres duplicados"""
    nombres = [p['nombre'] for p in personas]
    contador = Counter(nombres)
    duplicados = {nombre: count for nombre, count in contador.items() if count > 1}
    
    return {
        'total_nombres': len(nombres),
        'nombres_unicos': len(set(nombres)),
        'duplicados_encontrados': len(duplicados),
        'duplicados': duplicados
    }


def verificar_completitud(personas: List[Dict]) -> Dict:
    """Verifica la completitud de los campos"""
    campos = [
        'nombre', 'inicial', 'status_persona', 'tipo_persona',
        'status_cita', 'direccion', 'telefono_1', 'telefono_2',
        'historial_clinico', 'num_visitas', 'archivo_origen'
    ]
    
    completitud = {}
    
    for campo in campos:
        con_datos = sum(1 for p in personas if p.get(campo, '').strip())
        completitud[campo] = {
            'con_datos': con_datos,
            'sin_datos': len(personas) - con_datos,
            'porcentaje': (con_datos / len(personas) * 100) if personas else 0
        }
    
    return completitud


def verificar_telefonos(personas: List[Dict]) -> Dict:
    """Analiza los teléfonos"""
    con_tel1 = sum(1 for p in personas if p.get('telefono_1', '').strip())
    con_tel2 = sum(1 for p in personas if p.get('telefono_2', '').strip())
    con_ambos = sum(1 for p in personas if p.get('telefono_1', '').strip() and p.get('telefono_2', '').strip())
    sin_telefonos = sum(1 for p in personas if not p.get('telefono_1', '').strip() and not p.get('telefono_2', '').strip())
    
    return {
        'con_telefono_1': con_tel1,
        'con_telefono_2': con_tel2,
        'con_ambos_telefonos': con_ambos,
        'sin_telefonos': sin_telefonos,
        'al_menos_uno': con_tel1
    }


def verificar_archivos_origen(personas: List[Dict]) -> Dict:
    """Analiza la distribución por archivo de origen"""
    archivos = Counter(p.get('archivo_origen', 'desconocido') for p in personas)
    
    return {
        'total_archivos': len(archivos),
        'distribucion': dict(archivos.most_common()),
        'promedio_por_archivo': len(personas) / len(archivos) if archivos else 0,
        'archivo_con_mas': archivos.most_common(1)[0] if archivos else None,
        'archivo_con_menos': archivos.most_common()[-1] if archivos else None
    }


def buscar_inconsistencias(personas: List[Dict]) -> List[Dict]:
    """Busca posibles inconsistencias en los datos"""
    inconsistencias = []
    
    for i, persona in enumerate(personas):
        problemas = []
        
        # Verificar si tiene nombre pero no tipo
        if persona.get('nombre') and not persona.get('tipo_persona'):
            problemas.append('Sin tipo de persona')
        
        # Verificar si tiene visitas pero no historial
        if int(persona.get('num_visitas', 0)) > 0 and persona.get('historial_clinico') == 'SIN HISTORIAL':
            problemas.append('Tiene visitas pero sin historial')
        
        # Verificar si no tiene dirección
        if not persona.get('direccion', '').strip():
            problemas.append('Sin dirección')
        
        # Verificar teléfonos
        tel1 = persona.get('telefono_1', '').strip()
        tel2 = persona.get('telefono_2', '').strip()
        
        if tel1 and len(tel1) != 10:
            problemas.append(f'Teléfono 1 con longitud inválida: {len(tel1)} dígitos')
        
        if tel2 and len(tel2) != 10:
            problemas.append(f'Teléfono 2 con longitud inválida: {len(tel2)} dígitos')
        
        if problemas:
            inconsistencias.append({
                'indice': i,
                'nombre': persona.get('nombre'),
                'archivo': persona.get('archivo_origen'),
                'problemas': problemas
            })
    
    return inconsistencias


def generar_reporte():
    """Genera un reporte completo de calidad de datos"""
    print("="*80)
    print("REPORTE DE CALIDAD DE DATOS - personas.json")
    print("="*80)
    
    # Cargar datos
    try:
        personas = load_personas()
        print(f"\n✓ Archivo cargado exitosamente")
        print(f"  Total de registros: {len(personas)}")
    except FileNotFoundError:
        print("\n✗ No se encontró el archivo personas.json")
        print("  Ejecuta primero extract_all_views.py")
        return
    except Exception as e:
        print(f"\n✗ Error al cargar el archivo: {e}")
        return
    
    # Verificar duplicados
    print("\n" + "="*80)
    print("1. VERIFICACIÓN DE DUPLICADOS")
    print("="*80)
    
    duplicados = verificar_duplicados(personas)
    print(f"  Total de nombres: {duplicados['total_nombres']}")
    print(f"  Nombres únicos: {duplicados['nombres_unicos']}")
    
    if duplicados['duplicados_encontrados'] > 0:
        print(f"\n  ⚠ ADVERTENCIA: Se encontraron {duplicados['duplicados_encontrados']} nombres duplicados:")
        for nombre, count in duplicados['duplicados'].items():
            print(f"    - {nombre}: {count} veces")
    else:
        print(f"\n  ✓ No se encontraron duplicados")
    
    # Verificar completitud
    print("\n" + "="*80)
    print("2. COMPLETITUD DE CAMPOS")
    print("="*80)
    
    completitud = verificar_completitud(personas)
    
    print(f"\n{'Campo':<20} {'Con Datos':<12} {'Sin Datos':<12} {'%':<8}")
    print("-"*80)
    
    for campo, stats in completitud.items():
        print(f"{campo:<20} {stats['con_datos']:<12} {stats['sin_datos']:<12} {stats['porcentaje']:>6.1f}%")
    
    # Verificar teléfonos
    print("\n" + "="*80)
    print("3. ANÁLISIS DE TELÉFONOS")
    print("="*80)
    
    telefonos = verificar_telefonos(personas)
    print(f"  Con teléfono 1: {telefonos['con_telefono_1']} ({telefonos['con_telefono_1']/len(personas)*100:.1f}%)")
    print(f"  Con teléfono 2: {telefonos['con_telefono_2']} ({telefonos['con_telefono_2']/len(personas)*100:.1f}%)")
    print(f"  Con ambos teléfonos: {telefonos['con_ambos_telefonos']} ({telefonos['con_ambos_telefonos']/len(personas)*100:.1f}%)")
    print(f"  Sin teléfonos: {telefonos['sin_telefonos']} ({telefonos['sin_telefonos']/len(personas)*100:.1f}%)")
    print(f"  Al menos un teléfono: {telefonos['al_menos_uno']} ({telefonos['al_menos_uno']/len(personas)*100:.1f}%)")
    
    # Verificar archivos origen
    print("\n" + "="*80)
    print("4. DISTRIBUCIÓN POR ARCHIVO DE ORIGEN")
    print("="*80)
    
    archivos = verificar_archivos_origen(personas)
    print(f"  Total de archivos procesados: {archivos['total_archivos']}")
    print(f"  Promedio de personas por archivo: {archivos['promedio_por_archivo']:.1f}")
    
    if archivos['archivo_con_mas']:
        print(f"  Archivo con más personas: {archivos['archivo_con_mas'][0]} ({archivos['archivo_con_mas'][1]} personas)")
    if archivos['archivo_con_menos']:
        print(f"  Archivo con menos personas: {archivos['archivo_con_menos'][0]} ({archivos['archivo_con_menos'][1]} personas)")
    
    # Buscar inconsistencias
    print("\n" + "="*80)
    print("5. BÚSQUEDA DE INCONSISTENCIAS")
    print("="*80)
    
    inconsistencias = buscar_inconsistencias(personas)
    
    if inconsistencias:
        print(f"\n  ⚠ Se encontraron {len(inconsistencias)} registros con posibles inconsistencias:")
        
        for inc in inconsistencias[:10]:  # Mostrar solo las primeras 10
            print(f"\n  Registro #{inc['indice']} - {inc['nombre']} ({inc['archivo']})")
            for problema in inc['problemas']:
                print(f"    • {problema}")
        
        if len(inconsistencias) > 10:
            print(f"\n  ... y {len(inconsistencias) - 10} más")
    else:
        print(f"\n  ✓ No se encontraron inconsistencias")
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE CALIDAD")
    print("="*80)
    
    score = 100
    
    if duplicados['duplicados_encontrados'] > 0:
        score -= 20
        print("  ⚠ Duplicados encontrados (-20 puntos)")
    
    if telefonos['sin_telefonos'] > len(personas) * 0.1:
        score -= 10
        print("  ⚠ Más del 10% sin teléfonos (-10 puntos)")
    
    if inconsistencias:
        score -= min(len(inconsistencias), 30)
        print(f"  ⚠ {len(inconsistencias)} inconsistencias encontradas (-{min(len(inconsistencias), 30)} puntos)")
    
    print(f"\n  📊 Puntuación de calidad: {score}/100")
    
    if score >= 90:
        print("  ✅ Excelente calidad de datos")
    elif score >= 70:
        print("  ✓ Buena calidad de datos")
    elif score >= 50:
        print("  ⚠ Calidad aceptable, revisar inconsistencias")
    else:
        print("  ✗ Calidad baja, se requiere revisión")
    
    print("\n" + "="*80)


if __name__ == '__main__':
    generar_reporte()
