
# Pruebas Backend Registro Actividades

Este repositorio contiene pruebas de integración para los endpoints de diferentes módulos de backend de registro de actividades. Actualmente, solo se han implementado pruebas para los endpoints de **caretakers** y **patients**, pero todos los reportes generados tendrán la misma estructura en formato PDF.

## Estructura de Directorios

El directorio del proyecto tiene la siguiente estructura:

```
repo-pruebas/
├── pruebas/
│   ├── backend-registro-actividades/
│   │   ├── run_and_generate_report_caretakers.py
│   │   ├── run_and_generate_report_patients.py
│   │   ├── test_integracion_caretakers.py
│   │   ├── test_integracion_patients.py
│   │   └── resultados/
│   │       ├── reporte_integracion_tests_caretakers_1.pdf
│   │       ├── reporte_integracion_tests_caretakers_2.pdf
│   │       ├── reporte_integracion_tests_patients_1.pdf
│   │       ├── reporte_integracion_tests_patients_2.pdf
├── logo_unal.png
├── requirements.txt
├── README.md
```

## 1. **Instalación de dependencias**

Antes de correr las pruebas, asegúrate de tener todas las librerías necesarias. Puedes instalar las dependencias mediante `pip`:

```bash
pip install -r requirements.txt
```

## 2. **Ejecución de las pruebas**

Para ejecutar las pruebas y generar un reporte en formato PDF, usa los siguientes comandos según el tipo de prueba que deseas ejecutar:

#### **Para los tests de `caretakers`**:
```bash
python .\pruebasbackend-registro-actividades
un_and_generate_report_caretakers.py
```

#### **Para los tests de `patients`**:
```bash
python .\pruebasbackend-registro-actividades
un_and_generate_report_patients.py
```

Cada uno de estos comandos ejecutará los tests correspondientes para los endpoints de **caretakers** o **patients** y generará un archivo PDF en la carpeta `resultados/` dentro del directorio actual. El nombre del archivo PDF será incrementado automáticamente para evitar sobrescrituras.

## 3. **Estructura de los archivos de resultados**

Los archivos PDF generados con los resultados de las pruebas se almacenan en la carpeta `resultados/`. Cada archivo está versionado con un número, lo que garantiza que se mantengan diferentes versiones de los reportes.

Por ejemplo:

- **`reporte_integracion_tests_caretakers_1.pdf`**
- **`reporte_integracion_tests_caretakers_2.pdf`**
- **`reporte_integracion_tests_patients_1.pdf`**

Cada vez que se ejecute el script, el archivo PDF se generará con un número incremental, garantizando que no se sobrescriba ningún reporte anterior.

## 4. **Estructura de los PDFs**

Los reportes generados en formato PDF contienen los siguientes elementos:

- **Logo de la Universidad** (si se encuentra en el directorio): Se incluye al inicio del reporte.
- **Título**: El título del reporte indica el tipo de pruebas realizadas, como "Resultados de prueba del backend-registro-actividades para los endpoints de caretakers".
- **Fecha de generación**: Se muestra la fecha y hora en que el reporte fue generado.
- **Tabla de resultados**: Una tabla que lista cada prueba con los siguientes campos:
  - **Nombre del Test**: El nombre del test realizado.
  - **Resultado**: El estado de la prueba (Éxito, Fallo o Error).
  - **Detalles**: Detalles sobre el resultado. Si la prueba pasó, el detalle dirá "Pasó la prueba sin novedad", y si falló, se incluirán los detalles del error.
- **Gráfico de resultados**: Un gráfico de pastel que muestra el porcentaje de pruebas exitosas versus las que fallaron.
- **Conclusión**: Un resumen sobre el número de pruebas exitosas y el estado general del módulo probado.