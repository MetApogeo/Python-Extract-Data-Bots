Fase 1: Configuración de Filtros

Ejecuta estos comandos para llegar a la lista limpia de personas:

    Regresar al Inicio: adb shell input tap 92 1155

    Entrar a Visitar: adb shell input tap 259 208

    Abrir Filtro: adb shell input tap 723 242

    Seleccionar Valor: adb shell input tap 463 516

    Elegir "TODOS": adb shell input tap 412 857

    Aplicar Filtro: adb shell input tap 476 221

Fase 2: El Flujo de Extracción (El "Loop")

Una vez que el filtro esté aplicado y veas la lista, este es el proceso para una sola persona. Recuerda que como vives en Mérida, el clima y la conexión pueden afectar ligeramente la velocidad de carga de la tablet.

    Iniciar Visita: adb shell input tap 648 157

        Espera manual de 3 a 5 segundos aquí para que carguen los datos.( de preferencia 8 para asegurarnos que no haya errores)

    Ir a Siguiente (Pantalla del CURP): adb shell input tap 694 1063

    Capturar XML: * adb shell uiautomator dump /sdcard/prueba_curp.xml

    Descargar a tu PC:

        adb pull /sdcard/prueba_curp.xml .\extraccion_curp\xml\prueba_curp.xml

    Regresar al Inicio: adb shell input tap 92 1155

Fase 3: El Comando de Scroll

Cuando termines de procesar a las personas visibles en pantalla, usa el comando que encontraste para avanzar la lista de forma exacta:

    Scroll Perfecto: adb shell input swipe 290 1055 290 400 1100
