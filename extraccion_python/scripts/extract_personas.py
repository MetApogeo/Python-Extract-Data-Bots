#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script mejorado para extraer información de personas desde view.xml
Extrae: nombre, status persona, status cita, dirección, teléfono, historial clínico y visitas
"""

import xml.etree.ElementTree as ET
import re
import json
import csv
from typing import List, Dict
import html


class PersonaExtractor:
    """Clase para extraer información de personas del XML de Android UI"""
    
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.personas: List[Dict[str, str]] = []
    
    def parse_info_text(self, text: str) -> Dict[str, str]:
        """
        Parsea el texto de información que contiene status y dirección
        """
        info = {
            'status_persona': '',
            'tipo_persona': '',
            'status_cita': '',
            'direccion': '',
            'telefono_1': '',
            'telefono_2': ''
        }
        
        # Decodificar entidades HTML
        text = html.unescape(text)
        
        # Dividir por saltos de línea
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Extraer Status persona
            if line.startswith('Status persona:'):
                match = re.search(r'Status persona:\s*(.+?)(?:\s*\((.+?)\))?$', line)
                if match:
                    info['status_persona'] = match.group(1).strip()
                    if match.group(2):
                        info['tipo_persona'] = match.group(2).strip()
            
            # Extraer Status cita
            elif line.startswith('Status cita:'):
                match = re.search(r'Status cita:\s*(.+)$', line)
                if match:
                    info['status_cita'] = match.group(1).strip()
            
            # Extraer dirección y teléfonos
            elif 'Col.' in line or 'Mun.' in line or 'Tel:' in line:
                # Separar dirección de teléfonos
                if 'Tel:' in line:
                    parts = line.split('Tel:')
                    info['direccion'] = parts[0].strip()
                    
                    # Extraer teléfonos
                    if len(parts) > 1:
                        telefonos = parts[1].strip().split('|')
                        telefonos = [t.strip() for t in telefonos if t.strip() and t.strip() != '0']
                        
                        if len(telefonos) > 0:
                            info['telefono_1'] = telefonos[0]
                        if len(telefonos) > 1:
                            info['telefono_2'] = telefonos[1]
                else:
                    info['direccion'] = line.strip()
        
        return info
    
    def parse_historial_text(self, text: str) -> Dict[str, str]:
        """
        Parsea el texto de historial clínico
        """
        historial_info = {
            'historial_clinico': '',
            'num_visitas': '0'
        }
        
        # Extraer estado del historial
        if 'SIN HISTORIAL CLINICO' in text:
            historial_info['historial_clinico'] = 'SIN HISTORIAL'
        elif 'HISTORIAL CLINICO COMPLETO' in text:
            historial_info['historial_clinico'] = 'COMPLETO'
        elif 'HISTORIAL CLINICO' in text:
            historial_info['historial_clinico'] = 'PARCIAL'
        
        # Extraer número de visitas
        match = re.search(r'(\d+)\s*VISITA', text)
        if match:
            historial_info['num_visitas'] = match.group(1)
        
        return historial_info
    
    def extract_personas(self):
        """Extrae todas las personas del XML"""
        try:
            # Parsear el XML
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            
            # Encontrar todos los TextView
            all_text_views = root.findall(".//node[@class='android.widget.TextView']")
            
            # Procesar secuencialmente
            i = 0
            while i < len(all_text_views):
                node = all_text_views[i]
                text = node.get('text', '').strip()
                
                # Buscar un nombre (texto largo en mayúsculas)
                if (text and text.isupper() and len(text) > 10 and ' ' in text and 
                    not text.startswith('Status') and 
                    not 'HISTORIAL' in text and
                    not 'VISITA' in text and
                    not text.startswith('Total:') and
                    not text.startswith('Regresar') and
                    not text.startswith('Agregar') and
                    not text.startswith('Inicio') and
                    not text.startswith('Programar') and
                    not text.startswith('Visitar') and
                    not text.startswith('Sincronizar')):
                    
                    # Crear nueva persona
                    persona = {
                        'nombre': text,
                        'inicial': '',
                        'status_persona': '',
                        'tipo_persona': '',
                        'status_cita': '',
                        'direccion': '',
                        'telefono_1': '',
                        'telefono_2': '',
                        'historial_clinico': '',
                        'num_visitas': '0'
                    }
                    
                    # Buscar los siguientes 3-4 TextViews que deberían contener:
                    # 1. Inicial (letra sola)
                    # 2. Info de status y dirección
                    # 3. Historial
                    
                    for j in range(i + 1, min(i + 5, len(all_text_views))):
                        next_text = all_text_views[j].get('text', '').strip()
                        
                        if not next_text:
                            continue
                        
                        # Inicial
                        if len(next_text) == 1 and next_text.isalpha() and next_text.isupper():
                            persona['inicial'] = next_text
                        
                        # Info de status
                        elif 'Status persona:' in next_text:
                            info = self.parse_info_text(next_text)
                            persona.update(info)
                        
                        # Historial
                        elif 'HISTORIAL' in next_text and 'VISITA' in next_text:
                            historial_info = self.parse_historial_text(next_text)
                            persona.update(historial_info)
                        
                        # Si encontramos otro nombre, salir
                        elif (next_text.isupper() and len(next_text) > 10 and ' ' in next_text):
                            break
                    
                    self.personas.append(persona)
                
                i += 1
            
            print(f"✓ Se extrajeron {len(self.personas)} personas del archivo XML")
            
        except Exception as e:
            print(f"✗ Error al parsear el XML: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def save_to_json(self, output_file: str = 'personas.json'):
        """Guarda los datos en formato JSON"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.personas, f, ensure_ascii=False, indent=2)
            print(f"✓ Datos guardados en {output_file}")
        except Exception as e:
            print(f"✗ Error al guardar JSON: {e}")
    
    def save_to_csv(self, output_file: str = 'personas.csv'):
        """Guarda los datos en formato CSV"""
        try:
            if not self.personas:
                print("✗ No hay datos para guardar")
                return
            
            fieldnames = [
                'nombre', 'inicial', 'status_persona', 'tipo_persona',
                'status_cita', 'direccion', 'telefono_1', 'telefono_2',
                'historial_clinico', 'num_visitas'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.personas)
            
            print(f"✓ Datos guardados en {output_file}")
        except Exception as e:
            print(f"✗ Error al guardar CSV: {e}")
    
    def print_summary(self):
        """Imprime un resumen de los datos extraídos"""
        if not self.personas:
            print("No se encontraron personas")
            return
        
        print("\n" + "="*80)
        print(f"RESUMEN DE EXTRACCIÓN")
        print("="*80)
        print(f"Total de personas: {len(self.personas)}")
        
        # Contar por tipo
        tipos = {}
        for p in self.personas:
            tipo = p.get('tipo_persona', 'SIN TIPO')
            if not tipo:
                tipo = 'SIN TIPO'
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        print(f"\nPor tipo de persona:")
        for tipo, count in sorted(tipos.items()):
            print(f"  - {tipo}: {count}")
        
        # Contar por status de cita
        status_citas = {}
        for p in self.personas:
            status = p.get('status_cita', 'SIN STATUS')
            if not status:
                status = 'SIN STATUS'
            status_citas[status] = status_citas.get(status, 0) + 1
        
        print(f"\nPor status de cita:")
        for status, count in sorted(status_citas.items()):
            print(f"  - {status}: {count}")
        
        # Contar historial clínico
        con_historial = sum(1 for p in self.personas if p.get('historial_clinico') == 'COMPLETO')
        sin_historial = sum(1 for p in self.personas if p.get('historial_clinico') == 'SIN HISTORIAL')
        
        print(f"\nHistorial clínico:")
        print(f"  - Con historial completo: {con_historial}")
        print(f"  - Sin historial: {sin_historial}")
        
        # Total de visitas
        total_visitas = sum(int(p.get('num_visitas', 0)) for p in self.personas)
        print(f"\nTotal de visitas registradas: {total_visitas}")
        
        print("\n" + "="*80)
        print("PRIMERAS 3 PERSONAS EXTRAÍDAS:")
        print("="*80)
        
        for i, persona in enumerate(self.personas[:3], 1):
            print(f"\n{i}. {persona['nombre']}")
            print(f"   Tipo: {persona['tipo_persona']}")
            print(f"   Status Persona: {persona['status_persona']}")
            print(f"   Status Cita: {persona['status_cita']}")
            print(f"   Dirección: {persona['direccion']}")
            print(f"   Teléfonos: {persona['telefono_1']} | {persona['telefono_2']}")
            print(f"   Historial: {persona['historial_clinico']} - {persona['num_visitas']} visita(s)")
        
        print("\n" + "="*80)


def main():
    """Función principal"""
    print("="*80)
    print("EXTRACTOR DE INFORMACIÓN DE PERSONAS - view.xml")
    print("="*80)
    
    # Archivo de entrada
    xml_file = 'view.xml'
    
    # Crear extractor
    extractor = PersonaExtractor(xml_file)
    
    # Extraer personas
    print(f"\nProcesando archivo: {xml_file}")
    extractor.extract_personas()
    
    # Mostrar resumen
    extractor.print_summary()
    
    # Guardar en diferentes formatos
    print("\n" + "="*80)
    print("GUARDANDO DATOS")
    print("="*80)
    
    extractor.save_to_json('personas.json')
    extractor.save_to_csv('personas.csv')
    
    print("\n✓ Proceso completado exitosamente")
    print("\nArchivos generados:")
    print("  - personas.json (formato JSON)")
    print("  - personas.csv (formato CSV para Excel)")


if __name__ == '__main__':
    main()
