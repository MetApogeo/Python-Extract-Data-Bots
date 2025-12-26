2. Cómo manejar los 600 archivos (Nombres dinámicos)

Como vas a tener muchísimos registros, no puedes guardarlos todos como prueba_curp.xml porque cada uno sobreescribirá al anterior. En tu script de Python, debes usar una variable para el nombre:
Python

import os

# Supongamos que tienes el nombre de la persona en una variable

nombre_persona = "ABEL_ADAM_MAURICIO_HERNANDEZ"
ruta_pc = f".\\extraccion_curp\\xml\\{nombre_persona}.xml"

# El comando descarga el archivo de la tablet y le pone el nombre de la persona en tu PC

os.system(f"adb pull /sdcard/prueba_curp.xml {ruta_pc}")

Evita caracteres especiales: Al guardar el XML en Windows, asegúrate de limpiar el nombre de la persona (quitar acentos, eñes o caracteres raros) para que el comando adb pull no de error por la ruta de archivos.

Verificación de existencia: Antes de hacer el pull, tu script de Python debería verificar si la carpeta xml existe usando os.makedirs("extraccion_curp/xml", exist_ok=True).

Seguimiento: Como vives en Mérida, aprovecha el tiempo de carga de la tablet para que el script imprima en consola: "Descargado registro 45 de 526..." y así sepas cuánto falta para terminar.

REQUERIMIENTO CRÍTICO (Coordenadas Dinámicas): La pantalla presenta una lista de personas y cada una tiene su propio botón "Visitar" a la derecha. NO uses coordenadas fijas para el botón "Visitar". El script debe:

    Analizar el XML de la pantalla (uiautomator dump).

    Localizar el nodo de texto que contiene el nombre de la persona.

    Identificar el botón "Visitar" que esté en el mismo nivel jerárquico o más cercano al nombre.

    Extraer el atributo bounds (ejemplo: [650,300][800,400]), calcular el punto central (x, y) y ejecutar el adb shell input tap en ese punto exacto.
