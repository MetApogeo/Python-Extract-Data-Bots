#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot RPA para extracción automática de 526 registros CURP desde tablet Android
Versión modular con manejo robusto de errores y sistema de checkpoint
"""

import os
import time
import json
import logging
import xml.etree.ElementTree as ET
from typing import Set
from pathlib import Path

# Importar módulos locales
from config import *
from utils import (
    sanitize_name,
    adb_tap,
    safe_adb_command,
    dump_screen_xml,
    get_people_with_buttons,
    extraer_curp_de_xml
)


# === CONFIGURACIÓN DE LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# === FUNCIONES DE CHECKPOINT ===

def load_checkpoint() -> dict:
    """
    Carga el progreso guardado desde progreso.json
    
    Returns:
        Dict con 'procesados' (set de nombres)
    """
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Checkpoint cargado: {len(data.get('procesados', []))} personas ya procesadas")
                return {
                    'procesados': set(data.get('procesados', []))
                }
        except Exception as e:
            logger.error(f"Error al cargar checkpoint: {e}")
    
    return {'procesados': set()}


def save_checkpoint(procesados: Set[str], scroll_count: int = 0, ultimo_scroll: int = 0):
    """
    Guarda el progreso actual en progreso.json
    
    Args:
        procesados: Set de nombres ya procesados
        scroll_count: (Obsoleto, mantenido por compatibilidad)
        ultimo_scroll: (Obsoleto, mantenido por compatibilidad)
    """
    try:
        data = {
            'procesados': list(procesados),
            'timestamp': time.time(),
            'total_procesados': len(procesados)
        }
        
        with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.debug(f"Checkpoint guardado: {len(procesados)} personas")
    except Exception as e:
        logger.error(f"Error al guardar checkpoint: {e}")


# === FUNCIONES DE FLUJO ===

def apply_filters():
    """
    Aplica los filtros para mostrar todas las personas
    Solo se ejecuta UNA VEZ al inicio
    """
    logger.info("Aplicando filtros para mostrar lista completa...")
    
    # Ir al inicio
    adb_tap(BTN_INICIO, DELAY_TAP_DEFAULT)
    
    # Entrar al padrón
    adb_tap(BTN_VISITAR_MENU, DELAY_TAP_DEFAULT)
    
    # Abrir filtro
    adb_tap(BTN_FILTRO, DELAY_TAP_DEFAULT)
    
    # Seleccionar "Todos"
    adb_tap(BTN_VALOR_TODOS, DELAY_TAP_DEFAULT)
    adb_tap(BTN_TODOS_OPCION, DELAY_TAP_DEFAULT)
    
    # Aplicar filtro
    adb_tap(BTN_APLICAR_FILTRO, DELAY_FILTRO_CARGA)
    
    logger.info("Filtros aplicados. Lista cargada.")


def regresar_a_lista():
    """
    Regresa a la lista de personas usando el botón ATRÁS de Android (2 veces)
    
    OPTIMIZACIÓN CLAVE: Esto mantiene la posición del scroll, a diferencia de
    reaplicar filtros que resetea todo. Es MUCHO más rápido.
    
    Secuencia:
    1. Primer ATRÁS: Sale de la pantalla de CURP
    2. Segundo ATRÁS: Sale de la ficha de la persona
    3. Resultado: Vuelve a la lista en la MISMA posición
    """
    logger.debug("   Regresando a lista (2x ATRÁS)...")
    
    # Primer ATRÁS (salir de pantalla CURP)
    if not safe_adb_command("shell input keyevent 4"):
        logger.error("   ❌ Falló primer ATRÁS")
        return False
    
    time.sleep(1.5)  # Esperar a que procese
    
    # Segundo ATRÁS (salir de ficha de persona)
    if not safe_adb_command("shell input keyevent 4"):
        logger.error("   ❌ Falló segundo ATRÁS")
        return False
    
    time.sleep(1.5)  # Esperar a que procese
    
    logger.debug("   ✅ De vuelta en la lista")
    return True


def verificar_pantalla_correcta() -> bool:
    """
    Verifica que estamos en la pantalla correcta (filtro "Sin visita realizada")
    
    VALIDACIÓN CRÍTICA: Antes de procesar personas, verificamos que no nos hayamos
    salido accidentalmente de la pantalla correcta.
    
    Returns:
        True si estamos en la pantalla correcta, False si no
    """
    try:
        # Capturar XML de la pantalla actual
        if not dump_screen_xml(SCREEN_XML_TEMP):
            logger.warning("⚠️  No se pudo capturar XML para verificación")
            return False
        
        # Buscar el texto indicador "Personas sin visita realizada" o "sin visita"
        tree = ET.parse(SCREEN_XML_TEMP)
        root = tree.getroot()
        
        for node in root.findall(".//node[@class='android.widget.TextView']"):
            text = node.get("text", "").strip()
            if "sin visita" in text.lower() or "sin visita realizada" in text.lower():
                logger.debug("✓ Verificación: Estamos en la pantalla correcta")
                return True
        
        # Si no encontramos el texto, estamos en la pantalla incorrecta
        logger.warning("⚠️  ALERTA: No estamos en la pantalla 'Sin visita realizada'")
        return False
        
    except Exception as e:
        logger.error(f"Error al verificar pantalla: {e}")
        return False


def recuperar_pantalla_correcta():
    """
    Intenta recuperar la pantalla correcta si nos salimos accidentalmente
    
    Estrategia SIMPLE:
    1. Presionar botón INICIO para resetear
    2. Reaplicar filtros (como al inicio del bot)
    """
    logger.warning("🔄 Intentando recuperar pantalla correcta...")
    
    # Presionar botón INICIO para resetear
    logger.debug("   Presionando botón INICIO...")
    adb_tap(BTN_INICIO, DELAY_TAP_DEFAULT)
    
    # Reaplicar filtros (igual que al inicio)
    apply_filters()
    
    # Verificar si funcionó
    if verificar_pantalla_correcta():
        logger.info("✅ Pantalla correcta recuperada")
        return True
    else:
        logger.error("❌ No se pudo recuperar la pantalla correcta")
        return False


def process_person(nombre: str, coordenadas_boton: str, procesados: Set[str]) -> bool:
    """
    Procesa una persona: entra a su ficha, captura CURP, guarda JSON
    
    Args:
        nombre: Nombre completo de la persona
        coordenadas_boton: Coordenadas del botón "Visitar" de esta persona
        procesados: Set de personas ya procesadas
    
    Returns:
        True si se procesó exitosamente
    """
    nombre_limpio = sanitize_name(nombre)
    ruta_json = os.path.join(FOLDER_JSON, f"{nombre_limpio}.json")
    
    # Verificar si ya existe el archivo
    if os.path.exists(ruta_json):
        logger.info(f"⏭️  Ya existe: {nombre_limpio}.json - Saltando")
        procesados.add(nombre)
        return True
    
    logger.info(f"📝 Procesando ({len(procesados)+1}/{TOTAL_OBJETIVO}): {nombre}")
    
    try:
        # 1. Hacer clic en el botón "Visitar" de ESTA persona (coordenadas dinámicas)
        logger.debug(f"   Clic en botón Visitar: {coordenadas_boton}")
        if not adb_tap(coordenadas_boton, DELAY_TAP_DEFAULT):
            logger.error(f"   ❌ Falló tap en botón Visitar")
            return False
        
        # 2. Iniciar visita (esperar a ver si la pantalla cambia)
        logger.debug(f"   Iniciando visita...")
        if not adb_tap(BTN_INICIAR_VISITA, DELAY_TAP_DEFAULT):
            logger.error(f"   ❌ Falló tap en Iniciar Visita")
            return False
        
        # 2.5. Verificar si la visita ya fue realizada
        # Si la pantalla no cambia en 5 segundos, significa que ya se visitó
        logger.debug(f"   Verificando si la visita ya fue realizada (esperando 5s)...")
        time.sleep(5)
        
        # Capturar XML para verificar si estamos en la misma pantalla
        if not dump_screen_xml("temp_check.xml"):
            logger.warning(f"   ⚠️  No se pudo verificar estado de visita")
        else:
            # Buscar si sigue apareciendo "Iniciar visita" (señal de que ya fue visitada)
            try:
                tree = ET.parse("temp_check.xml")
                root = tree.getroot()
                
                # Buscar texto "Iniciar visita" o "Ya visitada" o similar
                for node in root.findall(".//node[@class='android.widget.TextView']"):
                    text = node.get("text", "").strip()
                    if "Iniciar visita" in text or "visitada" in text.lower():
                        logger.warning(f"   ⚠️  Esta persona ya fue visitada. Omitiendo...")
                        # Regresar al inicio
                        adb_tap(BTN_INICIO, DELAY_TAP_DEFAULT)
                        apply_filters()
                        # Marcar como procesada para no intentar de nuevo
                        procesados.add(nombre)
                        return True  # Retornar True porque técnicamente se "procesó"
                
                # Limpiar archivo temporal
                if os.path.exists("temp_check.xml"):
                    os.remove("temp_check.xml")
                    
            except Exception as e:
                logger.warning(f"   ⚠️  Error al verificar estado: {e}")
        
        # Si llegamos aquí, la pantalla cambió (visita no realizada previamente)
        # Esperar el tiempo restante para que carguen los datos
        logger.debug(f"   Visita no realizada previamente. Esperando {DELAY_CARGA_DATOS - 5}s más...")
        time.sleep(DELAY_CARGA_DATOS - 5)  # Ya esperamos 5s, esperamos el resto
        
        # 3. Ir a la pantalla del CURP
        logger.debug(f"   Presionando 'Siguiente' para ir a pantalla CURP...")
        if not adb_tap(BTN_SIGUIENTE, DELAY_TAP_DEFAULT):
            logger.error(f"   ❌ Falló tap en Siguiente")
            return False
        
        # 3.5. Esperar a que cargue la pantalla del CURP (CRÍTICO)
        logger.debug(f"   Esperando {DELAY_SIGUIENTE}s a que cargue pantalla CURP...")
        time.sleep(DELAY_SIGUIENTE)
        
        # 4. Capturar XML de la pantalla del CURP
        logger.debug(f"   Capturando XML del CURP...")
        ruta_xml_temp = os.path.join(FOLDER_XML, f"{nombre_limpio}_temp.xml")
        if not safe_adb_command(f"shell uiautomator dump {CURP_XML_TEMP}"):
            logger.error(f"   ❌ Falló dump del XML")
            return False
        
        # 5. Descargar XML temporal
        logger.debug(f"   Descargando XML temporal...")
        if not safe_adb_command(f"pull {CURP_XML_TEMP} {ruta_xml_temp}"):
            logger.error(f"   ❌ Falló pull del XML")
            return False
        
        # 6. Extraer CURP del XML
        logger.debug(f"   Extrayendo CURP del XML...")
        curp = extraer_curp_de_xml(ruta_xml_temp)
        
        if not curp:
            logger.warning(f"   ⚠️  No se pudo extraer CURP del XML")
            # Guardar JSON sin CURP
            data = {
                "nombre": nombre,
                "curp": None,
                "error": "No se encontró CURP en el XML"
            }
        else:
            # Guardar JSON con CURP
            data = {
                "nombre": nombre,
                "curp": curp
            }
        
        # 7. Guardar JSON
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"   ✅ Guardado: {nombre_limpio}.json" + (f" (CURP: {curp})" if curp else " (sin CURP)"))
        
        # 8. Borrar XML temporal
        if os.path.exists(ruta_xml_temp):
            os.remove(ruta_xml_temp)
        
        # 9. OPTIMIZACIÓN: Regresar a lista con botón ATRÁS (mantiene scroll)
        logger.debug(f"   Regresando a lista...")
        if not regresar_a_lista():
            logger.warning(f"   ⚠️  Falló regreso a lista, intentando recuperar...")
            # Fallback: ir al inicio y reaplicar filtros
            adb_tap(BTN_INICIO, DELAY_TAP_DEFAULT)
            apply_filters()
        
        logger.info(f"   ✅ Completado: {nombre_limpio}.json")
        procesados.add(nombre)
        return True
        
    except Exception as e:
        logger.error(f"   ❌ Error al procesar {nombre}: {e}")
        # Intentar regresar a lista en caso de error
        logger.debug("   Intentando regresar a lista después de error...")
        if not regresar_a_lista():
            # Fallback: ir al inicio y reaplicar filtros
            adb_tap(BTN_INICIO, DELAY_TAP_DEFAULT)
            apply_filters()
        return False


def do_scroll():
    """
    Ejecuta el scroll perfecto para avanzar en la lista
    """
    logger.info("📜 Haciendo scroll para ver más personas...")
    # Extraer solo la parte del comando después de 'adb '
    scroll_cmd = SCROLL_COMMAND.replace("adb ", "")
    safe_adb_command(scroll_cmd)
    time.sleep(DELAY_SCROLL)


# === FUNCIÓN PRINCIPAL ===

def main():
    """
    Función principal del bot
    """
    logger.info("="*80)
    logger.info("🤖 BOT RPA - EXTRACCIÓN DE CURP")
    logger.info(f"   Objetivo: {TOTAL_OBJETIVO} registros")
    logger.info("="*80)
    
    # Crear carpetas si no existen
    os.makedirs(FOLDER_XML, exist_ok=True)
    os.makedirs(FOLDER_JSON, exist_ok=True)
    
    # Cargar checkpoint
    checkpoint = load_checkpoint()
    procesados = checkpoint['procesados']
    
    if procesados:
        logger.info(f"🔄 Reanudando desde checkpoint: {len(procesados)} ya procesados")
    
    # Aplicar filtros iniciales (SOLO UNA VEZ)
    # OPTIMIZACIÓN: No volvemos a aplicar filtros después de cada persona
    # En su lugar, usamos el botón ATRÁS que mantiene la posición del scroll
    apply_filters()
    
    # Variables de control
    intentos_sin_nuevos = 0
    max_intentos_sin_nuevos = 100  # Permitir más scrolls antes de terminar
    
    # Loop principal SIMPLIFICADO
    while len(procesados) < TOTAL_OBJETIVO:
        # VALIDACIÓN CRÍTICA: Verificar que estamos en la pantalla correcta
        logger.debug("🔍 Verificando que estamos en la pantalla correcta...")
        if not verificar_pantalla_correcta():
            logger.error("❌ ERROR: Nos salimos de la pantalla 'Sin visita realizada'")
            
            # Intentar recuperar
            if recuperar_pantalla_correcta():
                logger.info("✅ Pantalla recuperada, continuando...")
                continue
            else:
                logger.error("❌ CRÍTICO: No se pudo recuperar la pantalla. Deteniendo bot.")
                break
        
        # Capturar XML de la pantalla actual
        logger.info(f"\n📸 Capturando pantalla actual...")
        if not dump_screen_xml(SCREEN_XML_TEMP):
            logger.error("❌ No se pudo capturar XML de pantalla. Reintentando...")
            time.sleep(3)
            continue
        
        # Extraer personas y sus botones
        personas_en_pantalla = get_people_with_buttons(SCREEN_XML_TEMP)
        
        if not personas_en_pantalla:
            logger.warning("⚠️  No se detectaron personas en la pantalla")
            do_scroll()
            intentos_sin_nuevos += 1
            
            if intentos_sin_nuevos >= max_intentos_sin_nuevos:
                logger.warning(f"⚠️  {max_intentos_sin_nuevos} scrolls sin personas nuevas. Finalizando.")
                break
            continue
        
        logger.info(f"👥 Detectadas {len(personas_en_pantalla)} personas en pantalla")
        
        # Procesar cada persona visible que NO esté en procesados
        encontrado_nuevo = False
        for nombre, coordenadas in personas_en_pantalla:
            if nombre not in procesados:
                # Procesar esta persona
                if process_person(nombre, coordenadas, procesados):
                    encontrado_nuevo = True
                    intentos_sin_nuevos = 0  # Resetear contador
                    
                    # Guardar checkpoint cada 10 registros
                    if len(procesados) % 10 == 0:
                        save_checkpoint(procesados, 0, 0)  # scroll_count y scroll_actual ya no son necesarios
                        logger.info(f"💾 Checkpoint guardado: {len(procesados)}/{TOTAL_OBJETIVO}")
                    
                    # IMPORTANTE: Después de procesar, la persona desaparece de la lista
                    # Salir del for para refrescar la pantalla SIN hacer scroll
                    logger.debug("   Refrescando pantalla (persona desapareció de lista)...")
                    break
                else:
                    logger.warning(f"⚠️  Falló procesamiento de {nombre}. Continuando...")
        
        # Si encontramos y procesamos alguien, NO hacer scroll
        # La lista se actualiza automáticamente y las personas suben de posición
        if encontrado_nuevo:
            logger.debug("   ✅ Persona procesada. Continuando sin scroll...")
            continue  # Volver al inicio del while para capturar pantalla de nuevo
        
        # Si TODAS las personas visibles ya fueron procesadas, hacer 1 scroll
        logger.info("🔍 Todas las personas visibles ya fueron procesadas")
        logger.info("📜 Haciendo 1 scroll para ver más personas...")
        do_scroll()
        intentos_sin_nuevos += 1
        
        if intentos_sin_nuevos >= max_intentos_sin_nuevos:
            logger.warning(f"⚠️  {max_intentos_sin_nuevos} scrolls sin personas nuevas. Finalizando.")
            break
    
    # Guardar checkpoint final
    save_checkpoint(procesados, 0, 0)
    
    # Resumen final
    logger.info("\n" + "="*80)
    logger.info("✅ PROCESO COMPLETADO")
    logger.info(f"   Total procesados: {len(procesados)}/{TOTAL_OBJETIVO}")
    logger.info(f"   XMLs guardados en: {FOLDER_XML}")
    logger.info(f"   Scrolls realizados: {scroll_count}")
    logger.info("="*80)
    
    # Verificar si se completó el objetivo
    if len(procesados) >= TOTAL_OBJETIVO:
        logger.info("🎉 ¡Objetivo alcanzado!")
    else:
        logger.warning(f"⚠️  Faltan {TOTAL_OBJETIVO - len(procesados)} registros")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️  Bot detenido manualmente por el usuario")
    except Exception as e:
        logger.error(f"\n❌ Error fatal: {e}", exc_info=True)