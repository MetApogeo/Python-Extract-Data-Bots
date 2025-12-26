#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para validar get_people_with_buttons() con el XML real
"""

import sys
sys.path.append('.')

from utils import get_people_with_buttons

# Probar con el XML real descargado
xml_path = "../../screen.xml"

print("="*60)
print("TEST: get_people_with_buttons() con XML real")
print("="*60)

personas = get_people_with_buttons(xml_path)

print(f"\n✅ Detectadas {len(personas)} personas:\n")

for i, (nombre, coords) in enumerate(personas, 1):
    print(f"{i}. {nombre}")
    print(f"   Botón: {coords}\n")

print("="*60)
