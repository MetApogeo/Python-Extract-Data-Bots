# 🤖 PythonBots: Suite de Automatización y Extracción de Datos

Este repositorio alberga un conjunto de herramientas de **RPA (Robotic Process Automation)** y scripts de procesamiento de datos diseñados para la extracción, limpieza y análisis de información desde dispositivos móviles y archivos XML.

El objetivo principal es automatizar tareas repetitivas de recolección de datos (CURP, padrones, visitas) y transformar esa información cruda en formatos estructurados y útiles (Excel, JSON).

## 🔒 Privacidad y Seguridad

Este proyecto está configurado para **proteger estrictamente los datos sensibles**.
El archivo `.gitignore` está configurado para ignorar automáticamente todas las carpetas de datos (`/json`, `/xml`, `/csv`) para evitar que información privada (PII) sea subida al repositorio.

---

## 📂 Módulos del Proyecto

### 1. 🤖 [Bot RPA - Extracción de CURP](./extraccion_curp)

**Ubicación:** `extraccion_curp/`

Un bot avanzado que utiliza **ADB (Android Debug Bridge)** para controlar una tablet y extraer sistemáticamente registros de CURP.

- **Funcionalidad:** Navega automáticamente por una app, visita perfiles, extrae datos y guarda el progreso.
- **Características Clave:**
  - 📍 **Coordenadas Dinámicas:** Se adapta a la interfaz leyendo el XML de la pantalla.
  - 💾 **Persistencia:** Guarda el progreso (`progreso.json`) para reanudar si se interrumpe.
  - 🛡️ **Sanitización:** Limpia nombres y formatos de archivo al vuelo.

### 2. 📊 [Sistema de Procesamiento XML](./extraccion_python)

**Ubicación:** `extraccion_python/`

El motor de procesamiento de datos backend. Toma los datos crudos extraídos y los convierte en inteligencia de negocios.

- **Funcionalidad:** Procesa masivamente archivos XML para generar reportes consolidados.
- **Salidas:**
  - 📋 Reportes Excel (`.csv`) listos para administración.
  - 🗄️ Base de datos JSON completa.
  - 📈 Analíticas de visitas (Visitados vs Rechazados vs No Visitados).

### 3. 📸 [Captura de Citas Hechas](./extraccion_citas_hechas)

**Ubicación:** `extraccion_citas_hechas/`

Una utilidad ligera para la captura rápida de pantallas de listas de visitas.

- **Funcionalidad:** Script "One-shot" para capturar lo que se ve en pantalla en ese momento y extraer nombres/CURPs.
- **Ideal para:** Auditorías rápidas o capturas manuales específicas sin correr el bot completo.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje núcleo.
- **ADB (Android Debug Bridge)**: Comunicación e interacción con dispositivos hardware.
- **XML Parsing (`xml.etree`)**: Análisis de estructuras de interfaz de Android.
- **RPA**: Lógica de automatización de GUI.

## � Herramientas Recomendadas

Este proyecto hace uso intensivo de **ADB**, pero para la visualización, monitoreo y pruebas manuales, recomendamos encarecidamente:

- **[scrcpy](https://github.com/Genymobile/scrcpy)**: Esta herramienta es fundamental para visualizar la pantalla de la tablet en tu ordenador con baja latencia. Aunque nuestros bots no dependen de `scrcpy` para ejecutarse (usan ADB puro), es vital para:
  - Ver lo que el bot está haciendo en tiempo real.
  - Tomar coordenadas manuales si fuera necesario.
  - Debuggear visualmente el flujo de la aplicación.

## �🚀 Cómo Empezar

Cada subproyecto tiene su propio `README.md` con instrucciones detalladas. Se recomienda empezar por:

1.  **Configurar el entorno**: Instalar Python y habilitar ADB.
2.  **Elegir la herramienta**:
    - Si necesitas _extraer_ datos nuevos: Ve a `extraccion_curp`.
    - Si necesitas _procesar_ datos ya extraídos: Ve a `extraccion_python`.

---

_Este proyecto es de uso interno y contiene configuraciones para ignorar datos sensibles por defecto._
