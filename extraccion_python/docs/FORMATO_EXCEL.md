# 📊 Formato Excel - Documentación

## Descripción

El script `generar_excel.py` transforma los datos de `personas.json` al formato de tabla Excel con las siguientes columnas:

| Columna       | Descripción             | Ejemplo                        |
| ------------- | ----------------------- | ------------------------------ |
| **Nombre(s)** | Nombre(s) de la persona | MARIA GUADALUPE                |
| **Paterno**   | Apellido paterno        | LOPEZ                          |
| **Materno**   | Apellido materno        | PEREZ                          |
| **Domicilio** | Dirección completa      | C. 81 X 26 Y 28 #408, Col. ... |
| **Teléfono**  | Teléfono principal      | 9991234567                     |
| **No**        | Estado de visita        | VISITADO / RECHAZO / NO        |

## Estado de Visita

El campo **"No"** se calcula automáticamente según estas reglas:

### 🔴 RECHAZO

- Cuando el historial clínico contiene "RECHAZADA(S)"
- Ejemplo: "SIN HISTORIAL - 1 VISITA(S) RECHAZADA(S)"

### ✅ VISITADO

- Cuando `num_visitas >= 1` Y NO está rechazado
- La persona fue visitada exitosamente

### ⚪ NO

- Cuando `num_visitas == 0` Y NO está rechazado
- La persona aún no ha sido visitada

## Separación de Nombres

El script separa automáticamente el nombre completo en tres partes:

### Ejemplos:

| Nombre Completo               | Nombre(s)       | Paterno | Materno   |
| ----------------------------- | --------------- | ------- | --------- |
| MARIA LOPEZ PEREZ             | MARIA           | LOPEZ   | PEREZ     |
| MARIA GUADALUPE LOPEZ PEREZ   | MARIA GUADALUPE | LOPEZ   | PEREZ     |
| JOSE ANTONIO GARCIA RODRIGUEZ | JOSE ANTONIO    | GARCIA  | RODRIGUEZ |
| MARIA                         | MARIA           |         |           |
| MARIA LOPEZ                   | MARIA           | LOPEZ   |           |

**Regla:** Los últimos 2 elementos son apellidos, todo lo demás es nombre.

## Uso

### Generar archivos Excel

```bash
python generar_excel.py
```

### Archivos generados

- **`personas_excel.json`** - Datos en formato JSON
- **`personas_excel.csv`** - Listo para abrir en Excel (UTF-8 con BOM)

### Requisitos

- Debe existir `personas.json` (generado por `extract_all_views.py`)
- Python 3.6+

## Estadísticas

El script muestra automáticamente:

```
Total de personas: 281
  - VISITADO: 144 (51.2%)
  - RECHAZO: 15 (5.3%)
  - NO: 122 (43.4%)
```

### Desglose por Estado

- **VISITADO (144 personas)**: Tienen 1 o más visitas exitosas
- **RECHAZO (15 personas)**: Tienen visitas pero fueron rechazadas
- **NO (122 personas)**: Aún no han sido visitadas

## Ejemplo de Salida JSON

```json
{
  "Nombre(s)": "MARIA GUADALUPE",
  "Paterno": "LOPEZ",
  "Materno": "PEREZ",
  "Domicilio": "C. 81 X 26 Y 28 #408, Col. COLONIA VICENTE SOLIS...",
  "Teléfono": "9991234567",
  "No": "VISITADO"
}
```

## Ejemplo de Salida CSV

```csv
Nombre(s),Paterno,Materno,Domicilio,Teléfono,No
MARIA GUADALUPE,LOPEZ,PEREZ,"C. 81 X 26 Y 28 #408, Col. ...",9991234567,VISITADO
JOSE ANTONIO,GARCIA,RODRIGUEZ,"79 X 26 Y 28 #413, Col. ...",9992345678,NO
```

## Notas Importantes

1. **Codificación UTF-8 con BOM**: El CSV usa `utf-8-sig` para compatibilidad con Excel
2. **Preserva datos originales**: Los archivos `personas.json` y `personas.csv` no se modifican
3. **Actualización**: Ejecuta el script cada vez que actualices `personas.json`

## Flujo de Trabajo Completo

```
1. extract_all_views.py  →  personas.json + personas.csv
                             (formato completo con todos los campos)

2. generar_excel.py      →  personas_excel.json + personas_excel.csv
                             (formato tabla Excel simplificado)
```

## Casos Especiales

### Nombres con "Y"

Algunos nombres contienen "Y" como parte del nombre:

```
"GABINA DEL SOCORRO CORAL Y PARRA"
→ Nombre(s): "GABINA DEL SOCORRO CORAL"
→ Paterno: "Y"
→ Materno: "PARRA"
```

### Nombres sin apellidos completos

```
"MARIA"
→ Nombre(s): "MARIA"
→ Paterno: ""
→ Materno: ""
```

## Verificación de Datos

Para verificar que los datos se generaron correctamente:

1. Abre `personas_excel.csv` en Excel
2. Verifica que las columnas estén correctamente separadas
3. Revisa que los acentos y caracteres especiales se vean bien
4. Confirma que el estado de visita sea correcto

---

**Última actualización:** Diciembre 2025
