#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extraer información de MÚLTIPLES archivos view.xml
Procesa todos los archivos XML en la carpeta 'views/' y consolida los datos
"""

import xml.etree.ElementTree as ET
import re
import json
import csv
import html
import os
from typing import List, Dict
from pathlib import Path


class PersonaExtractor:
    """Clase para extraer información de personas del XML de Android UI"""
    
    def __init__(self):
        self.personas: List[Dict[str, str]] = []
    
    def parse_info_text(self, text: str) -> Dict[str, str]:
        """Parsea el texto de información que contiene status y dirección"""
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
                if 'Tel:' in line:
                    parts = line.split('Tel:')
                    info['direccion'] = parts[0].strip()
                    
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
        """Parsea el texto de historial clínico"""
        historial_info = {
            'historial_clinico': '',
            'num_visitas': '0'
        }
        
        # Detectar si hay visitas rechazadas (PRIORIDAD)
        if 'RECHAZADA' in text.upper():
            historial_info['historial_clinico'] = 'RECHAZADO'
        # Detectar tipo de historial
        elif 'SIN HISTORIAL CLINICO' in text:
            historial_info['historial_clinico'] = 'SIN HISTORIAL'
        elif 'HISTORIAL CLINICO COMPLETO' in text:
            historial_info['historial_clinico'] = 'COMPLETO'
        elif 'SIN HISTORIAL' in text:
            historial_info['historial_clinico'] = 'SIN HISTORIAL'
        elif 'HISTORIAL CLINICO' in text:
            historial_info['historial_clinico'] = 'PARCIAL'
        
        # Extraer número de visitas
        match = re.search(r'(\d+)\s*VISITA', text)
        if match:
            historial_info['num_visitas'] = match.group(1)
        
        return historial_info
    
    def extract_from_file(self, xml_file: str) -> List[Dict[str, str]]:
        """Extrae personas de un archivo XML específico"""
        personas_file = []
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            all_text_views = root.findall(".//node[@class='android.widget.TextView']")
            
            i = 0
            while i < len(all_text_views):
                node = all_text_views[i]
                text = node.get('text', '').strip()
                
                # Buscar un nombre
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
                        'num_visitas': '0',
                        'archivo_origen': os.path.basename(xml_file)
                    }
                    
                    # Buscar información adicional en los siguientes TextViews
                    for j in range(i + 1, min(i + 5, len(all_text_views))):
                        next_text = all_text_views[j].get('text', '').strip()
                        
                        if not next_text:
                            continue
                        
                        if len(next_text) == 1 and next_text.isalpha() and next_text.isupper():
                            persona['inicial'] = next_text
                        
                        elif 'Status persona:' in next_text:
                            info = self.parse_info_text(next_text)
                            persona.update(info)
                        
                        elif 'HISTORIAL' in next_text and 'VISITA' in next_text:
                            historial_info = self.parse_historial_text(next_text)
                            persona.update(historial_info)
                        
                        elif (next_text.isupper() and len(next_text) > 10 and ' ' in next_text):
                            break
                    
                    personas_file.append(persona)
                
                i += 1
            
            return personas_file
            
        except Exception as e:
            print(f"  ✗ Error al procesar {xml_file}: {e}")
            return []
    
    def is_record_complete(self, persona: Dict[str, str]) -> bool:
        """
        Verifica si un registro tiene suficiente información para ser considerado válido.
        Un registro es válido si tiene al menos: nombre + 2 campos adicionales con datos
        """
        campos_con_datos = 0
        
        # Lista de campos importantes (excluyendo nombre y archivo_origen)
        campos_importantes = [
            'status_persona', 'tipo_persona', 'status_cita', 
            'direccion', 'telefono_1', 'historial_clinico'
        ]
        
        for campo in campos_importantes:
            if persona.get(campo, '').strip():
                campos_con_datos += 1
        
        # Requiere al menos 2 campos con datos además del nombre
        return campos_con_datos >= 2
    
    def count_filled_fields(self, persona: Dict[str, str]) -> int:
        """Cuenta cuántos campos tienen datos en un registro"""
        campos_importantes = [
            'status_persona', 'tipo_persona', 'status_cita', 
            'direccion', 'telefono_1', 'telefono_2', 'historial_clinico', 'num_visitas'
        ]
        
        count = 0
        for campo in campos_importantes:
            if persona.get(campo, '').strip():
                count += 1
        return count
    
    def find_duplicate_index(self, persona: Dict[str, str], existing_personas: List[Dict[str, str]]) -> int:
        """
        Busca si una persona ya existe en la lista y retorna su índice.
        Retorna -1 si no existe.
        """
        nombre = persona.get('nombre', '').strip()
        for idx, existing in enumerate(existing_personas):
            if existing.get('nombre', '').strip() == nombre:
                return idx
        return -1
    
    def extract_all_from_directory(self, directory: str = 'views', remove_duplicates: bool = True):
        """Extrae personas de todos los archivos XML en un directorio"""
        
        # Verificar que el directorio existe
        if not os.path.exists(directory):
            print(f"✗ El directorio '{directory}' no existe")
            print(f"  Creando directorio '{directory}'...")
            os.makedirs(directory)
            print(f"  ✓ Directorio creado. Coloca tus archivos XML allí y vuelve a ejecutar el script.")
            return
        
        # Buscar todos los archivos XML
        xml_files = sorted(Path(directory).glob('*.xml'))
        
        if not xml_files:
            print(f"✗ No se encontraron archivos XML en '{directory}'")
            print(f"  Coloca tus archivos view1.xml, view2.xml, etc. en la carpeta '{directory}'")
            return
        
        print(f"📂 Encontrados {len(xml_files)} archivo(s) XML en '{directory}'")
        print("="*80)
        
        total_personas_encontradas = 0
        registros_incompletos = 0
        duplicados_reemplazados = 0
        duplicados_ignorados = 0
        
        for xml_file in xml_files:
            print(f"\n📄 Procesando: {xml_file.name}")
            personas_file = self.extract_from_file(str(xml_file))
            
            if personas_file:
                total_personas_encontradas += len(personas_file)
                nuevas = 0
                
                for persona in personas_file:
                    # Verificar si el registro tiene suficiente información
                    if not self.is_record_complete(persona):
                        registros_incompletos += 1
                        continue
                    
                    # Buscar si ya existe
                    if remove_duplicates:
                        duplicate_idx = self.find_duplicate_index(persona, self.personas)
                        
                        if duplicate_idx >= 0:
                            # Ya existe - comparar cuál tiene más información
                            existing = self.personas[duplicate_idx]
                            new_fields = self.count_filled_fields(persona)
                            existing_fields = self.count_filled_fields(existing)
                            
                            if new_fields > existing_fields:
                                # El nuevo registro tiene más información, reemplazar
                                self.personas[duplicate_idx] = persona
                                duplicados_reemplazados += 1
                            else:
                                # El registro existente es mejor o igual, ignorar el nuevo
                                duplicados_ignorados += 1
                        else:
                            # No existe, agregar
                            self.personas.append(persona)
                            nuevas += 1
                    else:
                        # No verificar duplicados, solo agregar si está completo
                        self.personas.append(persona)
                        nuevas += 1
                
                print(f"  ✓ Encontradas {len(personas_file)} personas")
                if nuevas > 0:
                    print(f"    → {nuevas} nuevas agregadas")
            else:
                print(f"  ⚠ No se encontraron personas en este archivo")
        
        print("\n" + "="*80)
        print(f"✓ Proceso completado")
        print(f"  Total de registros encontrados: {total_personas_encontradas}")
        print(f"  Registros incompletos ignorados: {registros_incompletos}")
        if remove_duplicates:
            print(f"  Duplicados con más info (reemplazados): {duplicados_reemplazados}")
            print(f"  Duplicados con menos info (ignorados): {duplicados_ignorados}")
        print(f"  📊 Personas únicas en la base de datos: {len(self.personas)}")

    
    def save_to_json(self, output_file: str = 'personas.json'):
        """Guarda los datos en formato JSON"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.personas, f, ensure_ascii=False, indent=2)
            print(f"\n✓ Datos guardados en {output_file} ({len(self.personas)} personas)")
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
                'historial_clinico', 'num_visitas', 'archivo_origen'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.personas)
            
            print(f"✓ Datos guardados en {output_file} ({len(self.personas)} personas)")
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
        
        # Contar por archivo origen
        from collections import Counter
        archivos = Counter(p.get('archivo_origen', 'desconocido') for p in self.personas)
        
        print(f"\nPor archivo de origen:")
        for archivo, count in sorted(archivos.items()):
            print(f"  - {archivo:20} : {count:3} personas")
        
        # Contar por tipo
        tipos = Counter(p.get('tipo_persona', 'SIN TIPO') or 'SIN TIPO' for p in self.personas)
        
        print(f"\nPor tipo de persona:")
        for tipo, count in sorted(tipos.items()):
            print(f"  - {tipo:15} : {count:3} personas")
        
        # Contar por status de cita
        status_citas = Counter(p.get('status_cita', 'SIN STATUS') or 'SIN STATUS' for p in self.personas)
        
        print(f"\nPor status de cita:")
        for status, count in sorted(status_citas.items()):
            print(f"  - {status:15} : {count:3} personas")
        
        # Historial clínico
        con_historial = sum(1 for p in self.personas if p.get('historial_clinico') == 'COMPLETO')
        sin_historial = sum(1 for p in self.personas if p.get('historial_clinico') == 'SIN HISTORIAL')
        
        print(f"\nHistorial clínico:")
        print(f"  - Con historial completo: {con_historial}")
        print(f"  - Sin historial: {sin_historial}")
        
        # Total de visitas
        total_visitas = sum(int(p.get('num_visitas', 0)) for p in self.personas)
        print(f"\nTotal de visitas registradas: {total_visitas}")
        
        print("\n" + "="*80)


def main():
    """Función principal"""
    print("="*80)
    print("EXTRACTOR MASIVO DE INFORMACIÓN DE PERSONAS")
    print("Procesa múltiples archivos view.xml desde la carpeta 'views/'")
    print("="*80)
    
    # Crear extractor
    extractor = PersonaExtractor()
    
    # Extraer de todos los archivos (views está en el mismo nivel que scripts)
    extractor.extract_all_from_directory(directory='../views', remove_duplicates=True)
    
    # Si se encontraron personas, guardar y mostrar resumen
    if extractor.personas:
        # Mostrar resumen
        extractor.print_summary()
        
        # Guardar en diferentes formatos
        print("\n" + "="*80)
        print("GUARDANDO DATOS CONSOLIDADOS")
        print("="*80)
        
        extractor.save_to_json('../json/personas.json')
        extractor.save_to_csv('../csv/personas.csv')
        
        print("\n✓ Proceso completado exitosamente")
        print("\nArchivos generados:")
        print("  - json/personas.json (formato JSON)")
        print("  - csv/personas.csv (formato CSV para Excel)")
        print(f"\n💡 Total de personas únicas: {len(extractor.personas)}")
    else:
        print("\n⚠ No se extrajeron datos. Verifica que los archivos XML estén en la carpeta 'views/'")


if __name__ == '__main__':
    main()
