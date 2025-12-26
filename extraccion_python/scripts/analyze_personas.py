#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de utilidades para filtrar y analizar los datos extraídos de personas
"""

import json
import csv
from typing import List, Dict
from collections import Counter


class PersonaAnalyzer:
    """Clase para analizar y filtrar datos de personas"""
    
    def __init__(self, json_file: str = 'personas.json'):
        self.json_file = json_file
        self.personas: List[Dict[str, str]] = []
        self.load_data()
    
    def load_data(self):
        """Carga los datos desde el archivo JSON"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.personas = json.load(f)
            print(f"✓ Cargadas {len(self.personas)} personas desde {self.json_file}")
        except FileNotFoundError:
            print(f"✗ No se encontró el archivo {self.json_file}")
            print("  Ejecuta primero extract_personas.py")
        except Exception as e:
            print(f"✗ Error al cargar datos: {e}")
    
    def filter_by_tipo(self, tipo: str) -> List[Dict[str, str]]:
        """Filtra personas por tipo (PCD, PAM, etc.)"""
        return [p for p in self.personas if p.get('tipo_persona', '').upper() == tipo.upper()]
    
    def filter_by_status_cita(self, status: str) -> List[Dict[str, str]]:
        """Filtra personas por status de cita"""
        return [p for p in self.personas if p.get('status_cita', '').upper() == status.upper()]
    
    def filter_con_historial(self) -> List[Dict[str, str]]:
        """Filtra personas con historial clínico completo"""
        return [p for p in self.personas if p.get('historial_clinico') == 'COMPLETO']
    
    def filter_sin_historial(self) -> List[Dict[str, str]]:
        """Filtra personas sin historial clínico"""
        return [p for p in self.personas if p.get('historial_clinico') == 'SIN HISTORIAL']
    
    def filter_con_visitas(self) -> List[Dict[str, str]]:
        """Filtra personas que tienen al menos una visita"""
        return [p for p in self.personas if int(p.get('num_visitas', 0)) > 0]
    
    def filter_sin_telefono(self) -> List[Dict[str, str]]:
        """Filtra personas sin teléfono registrado"""
        return [p for p in self.personas 
                if not p.get('telefono_1') and not p.get('telefono_2')]
    
    def filter_con_dos_telefonos(self) -> List[Dict[str, str]]:
        """Filtra personas con dos teléfonos registrados"""
        return [p for p in self.personas 
                if p.get('telefono_1') and p.get('telefono_2')]
    
    def search_by_name(self, query: str) -> List[Dict[str, str]]:
        """Busca personas por nombre (búsqueda parcial)"""
        query = query.upper()
        return [p for p in self.personas if query in p.get('nombre', '').upper()]
    
    def get_estadisticas(self) -> Dict:
        """Genera estadísticas detalladas"""
        stats = {
            'total': len(self.personas),
            'por_tipo': Counter(p.get('tipo_persona', 'SIN TIPO') or 'SIN TIPO' 
                               for p in self.personas),
            'por_status_cita': Counter(p.get('status_cita', 'SIN STATUS') or 'SIN STATUS' 
                                      for p in self.personas),
            'por_historial': Counter(p.get('historial_clinico', 'SIN DATOS') or 'SIN DATOS' 
                                    for p in self.personas),
            'con_telefono': sum(1 for p in self.personas if p.get('telefono_1')),
            'sin_telefono': sum(1 for p in self.personas if not p.get('telefono_1')),
            'con_dos_telefonos': sum(1 for p in self.personas 
                                    if p.get('telefono_1') and p.get('telefono_2')),
            'total_visitas': sum(int(p.get('num_visitas', 0)) for p in self.personas),
            'promedio_visitas': 0
        }
        
        if stats['total'] > 0:
            stats['promedio_visitas'] = stats['total_visitas'] / stats['total']
        
        return stats
    
    def print_estadisticas(self):
        """Imprime estadísticas detalladas"""
        stats = self.get_estadisticas()
        
        print("\n" + "="*80)
        print("ESTADÍSTICAS DETALLADAS")
        print("="*80)
        
        print(f"\n📊 Total de personas: {stats['total']}")
        
        print(f"\n👥 Por tipo de persona:")
        for tipo, count in stats['por_tipo'].most_common():
            porcentaje = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"   {tipo:15} : {count:3} ({porcentaje:5.1f}%)")
        
        print(f"\n📅 Por status de cita:")
        for status, count in stats['por_status_cita'].most_common():
            porcentaje = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"   {status:15} : {count:3} ({porcentaje:5.1f}%)")
        
        print(f"\n🏥 Por historial clínico:")
        for historial, count in stats['por_historial'].most_common():
            porcentaje = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"   {historial:15} : {count:3} ({porcentaje:5.1f}%)")
        
        print(f"\n📞 Teléfonos:")
        print(f"   Con al menos 1 teléfono : {stats['con_telefono']}")
        print(f"   Sin teléfono            : {stats['sin_telefono']}")
        print(f"   Con 2 teléfonos         : {stats['con_dos_telefonos']}")
        
        print(f"\n🏠 Visitas:")
        print(f"   Total de visitas        : {stats['total_visitas']}")
        print(f"   Promedio por persona    : {stats['promedio_visitas']:.2f}")
        
        print("\n" + "="*80)
    
    def save_filtered(self, personas: List[Dict[str, str]], filename: str):
        """Guarda un subconjunto filtrado de personas"""
        # Guardar JSON
        json_file = f"{filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(personas, f, ensure_ascii=False, indent=2)
        
        # Guardar CSV
        csv_file = f"{filename}.csv"
        if personas:
            fieldnames = [
                'nombre', 'inicial', 'status_persona', 'tipo_persona',
                'status_cita', 'direccion', 'telefono_1', 'telefono_2',
                'historial_clinico', 'num_visitas'
            ]
            
            with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(personas)
        
        print(f"✓ Guardados {len(personas)} registros en:")
        print(f"  - {json_file}")
        print(f"  - {csv_file}")
    
    def print_personas(self, personas: List[Dict[str, str]], limit: int = 10):
        """Imprime una lista de personas"""
        if not personas:
            print("No se encontraron personas con ese criterio")
            return
        
        print(f"\nMostrando {min(len(personas), limit)} de {len(personas)} personas:")
        print("-" * 80)
        
        for i, p in enumerate(personas[:limit], 1):
            print(f"\n{i}. {p['nombre']}")
            if p.get('tipo_persona'):
                print(f"   Tipo: {p['tipo_persona']}")
            if p.get('status_cita'):
                print(f"   Status Cita: {p['status_cita']}")
            if p.get('telefono_1'):
                telefonos = p['telefono_1']
                if p.get('telefono_2'):
                    telefonos += f" / {p['telefono_2']}"
                print(f"   Tel: {telefonos}")
            if p.get('historial_clinico'):
                print(f"   Historial: {p['historial_clinico']} - {p['num_visitas']} visita(s)")
        
        if len(personas) > limit:
            print(f"\n... y {len(personas) - limit} más")


def menu_interactivo():
    """Menú interactivo para filtrar y analizar datos"""
    analyzer = PersonaAnalyzer()
    
    if not analyzer.personas:
        return
    
    while True:
        print("\n" + "="*80)
        print("MENÚ DE ANÁLISIS DE PERSONAS")
        print("="*80)
        print("\n1.  Ver estadísticas generales")
        print("2.  Filtrar por tipo de persona (PCD/PAM)")
        print("3.  Filtrar por status de cita")
        print("4.  Ver personas CON historial clínico completo")
        print("5.  Ver personas SIN historial clínico")
        print("6.  Ver personas con visitas registradas")
        print("7.  Ver personas sin teléfono")
        print("8.  Ver personas con 2 teléfonos")
        print("9.  Buscar por nombre")
        print("10. Ver todas las personas")
        print("0.  Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == '0':
            print("\n¡Hasta luego!")
            break
        
        elif opcion == '1':
            analyzer.print_estadisticas()
        
        elif opcion == '2':
            tipo = input("Ingresa el tipo (PCD/PAM): ").strip()
            personas = analyzer.filter_by_tipo(tipo)
            analyzer.print_personas(personas)
            
            if personas and input("\n¿Guardar resultados? (s/n): ").lower() == 's':
                filename = f"personas_tipo_{tipo.lower()}"
                analyzer.save_filtered(personas, filename)
        
        elif opcion == '3':
            status = input("Ingresa el status (ej: PENDIENTE): ").strip()
            personas = analyzer.filter_by_status_cita(status)
            analyzer.print_personas(personas)
            
            if personas and input("\n¿Guardar resultados? (s/n): ").lower() == 's':
                filename = f"personas_status_{status.lower()}"
                analyzer.save_filtered(personas, filename)
        
        elif opcion == '4':
            personas = analyzer.filter_con_historial()
            analyzer.print_personas(personas)
            
            if personas and input("\n¿Guardar resultados? (s/n): ").lower() == 's':
                analyzer.save_filtered(personas, "personas_con_historial")
        
        elif opcion == '5':
            personas = analyzer.filter_sin_historial()
            analyzer.print_personas(personas)
            
            if personas and input("\n¿Guardar resultados? (s/n): ").lower() == 's':
                analyzer.save_filtered(personas, "personas_sin_historial")
        
        elif opcion == '6':
            personas = analyzer.filter_con_visitas()
            analyzer.print_personas(personas)
            
            if personas and input("\n¿Guardar resultados? (s/n): ").lower() == 's':
                analyzer.save_filtered(personas, "personas_con_visitas")
        
        elif opcion == '7':
            personas = analyzer.filter_sin_telefono()
            analyzer.print_personas(personas)
            
            if personas and input("\n¿Guardar resultados? (s/n): ").lower() == 's':
                analyzer.save_filtered(personas, "personas_sin_telefono")
        
        elif opcion == '8':
            personas = analyzer.filter_con_dos_telefonos()
            analyzer.print_personas(personas)
            
            if personas and input("\n¿Guardar resultados? (s/n): ").lower() == 's':
                analyzer.save_filtered(personas, "personas_dos_telefonos")
        
        elif opcion == '9':
            query = input("Ingresa el nombre o parte del nombre: ").strip()
            personas = analyzer.search_by_name(query)
            analyzer.print_personas(personas)
        
        elif opcion == '10':
            analyzer.print_personas(analyzer.personas, limit=20)
        
        else:
            print("❌ Opción no válida")
        
        input("\nPresiona Enter para continuar...")


if __name__ == '__main__':
    print("="*80)
    print("ANALIZADOR DE DATOS DE PERSONAS")
    print("="*80)
    menu_interactivo()
