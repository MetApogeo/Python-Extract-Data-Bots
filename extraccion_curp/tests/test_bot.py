#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para validar las funciones del bot antes de ejecutarlo
Prueba: sanitize_name, calculate_center, y otras utilidades
"""

import sys
sys.path.append('.')

from utils import sanitize_name, calculate_center


def test_sanitize_name():
    """Prueba la función de sanitización de nombres"""
    print("="*60)
    print("TEST: sanitize_name()")
    print("="*60)
    
    tests = [
        ("JOSÉ MARÍA LÓPEZ", "JOSE_MARIA_LOPEZ"),
        ("ANA  SOFÍA  PÉREZ", "ANA_SOFIA_PEREZ"),
        ("JUAN-CARLOS GARCÍA", "JUAN_CARLOS_GARCIA"),
        ("MARÍA DE LOS ÁNGELES", "MARIA_DE_LOS_ANGELES"),
        ("PEÑA NIETO", "PENA_NIETO"),
        ("O'BRIEN", "OBRIEN"),
    ]
    
    passed = 0
    failed = 0
    
    for input_name, expected in tests:
        result = sanitize_name(input_name)
        status = "✅" if result == expected else "❌"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} '{input_name}' -> '{result}'")
        if result != expected:
            print(f"   Esperado: '{expected}'")
    
    print(f"\nResultado: {passed} passed, {failed} failed\n")
    return failed == 0


def test_calculate_center():
    """Prueba la función de cálculo de centro de bounds"""
    print("="*60)
    print("TEST: calculate_center()")
    print("="*60)
    
    tests = [
        ("[100,200][300,400]", "200 300"),
        ("[0,0][100,100]", "50 50"),
        ("[650,300][800,400]", "725 350"),
        ("[259,208][400,250]", "329 229"),
    ]
    
    passed = 0
    failed = 0
    
    for bounds, expected in tests:
        result = calculate_center(bounds)
        status = "✅" if result == expected else "❌"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} '{bounds}' -> '{result}'")
        if result != expected:
            print(f"   Esperado: '{expected}'")
    
    # Prueba con formato inválido
    invalid_result = calculate_center("[invalid]")
    if invalid_result is None:
        print(f"✅ '[invalid]' -> None (correcto)")
        passed += 1
    else:
        print(f"❌ '[invalid]' -> '{invalid_result}' (esperado: None)")
        failed += 1
    
    print(f"\nResultado: {passed} passed, {failed} failed\n")
    return failed == 0


def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*60)
    print("PRUEBAS UNITARIAS DEL BOT RPA")
    print("="*60 + "\n")
    
    all_passed = True
    
    # Ejecutar pruebas
    if not test_sanitize_name():
        all_passed = False
    
    if not test_calculate_center():
        all_passed = False
    
    # Resumen final
    print("="*60)
    if all_passed:
        print("✅ TODAS LAS PRUEBAS PASARON")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
