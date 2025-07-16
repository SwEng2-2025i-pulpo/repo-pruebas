import traceback
from datetime import datetime
from test_integracion_patients import (
    test_crear_paciente_exitoso,
    test_get_patient_by_id,
    test_get_patient_by_id_invalido,
    test_add_medication_log,
    test_get_medication_logs,
    test_add_meal,
    test_get_meals,
    test_update_medication_log,
    test_add_hygiene_log,
    test_get_hygiene_logs,
    test_add_vital_signs,
    test_get_vital_signs
)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import matplotlib.pyplot as plt
import os
from io import BytesIO

def run_tests():
    test_functions = {
        "Crear paciente exitoso": test_crear_paciente_exitoso,
        "Obtener paciente por ID": test_get_patient_by_id,
        "Obtener paciente con ID inválido": test_get_patient_by_id_invalido,
        "Añadir registro de medicación": test_add_medication_log,
        "Obtener registros de medicación": test_get_medication_logs,
        "Añadir comida": test_add_meal,
        "Obtener comidas": test_get_meals,
        "Actualizar registro de medicación": test_update_medication_log,
        "Agregar registro de higiene": test_add_hygiene_log,
        "Obtener registros de higiene": test_get_hygiene_logs,
        "Agregar signos vitales": test_add_vital_signs,
        "Obtener signos vitales": test_get_vital_signs
    }

    results = []
    for name, func in test_functions.items():
        try:
            func()
            results.append((name, "✅ Éxito", ""))
        except AssertionError as e:
            results.append((name, "❌ Fallo", str(e)))
        except Exception as e:
            results.append((name, "❌ Error", traceback.format_exc()))

    return results

def generar_grafico_en_memoria(resultados):
    labels = ['Éxito', 'Fallo/Error']
    success = sum(1 for _, status, _ in resultados if 'Éxito' in status)
    fail = len(resultados) - success
    sizes = [success, fail]

    plt.figure(figsize=(4, 4))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Resumen de Resultados')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

def obtener_nombre_pdf_incremental(base_name='reporte_integracion_tests_patients'):
    base_dir = os.path.join(os.path.dirname(__file__), 'resultados')
    os.makedirs(base_dir, exist_ok=True)

    i = 1
    while True:
        filename = f"{base_name}_{i}.pdf"
        path = os.path.join(base_dir, filename)
        if not os.path.exists(path):
            return path
        i += 1

def generar_pdf(resultados, path_pdf):
    doc = SimpleDocTemplate(path_pdf, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    logo_path = "logo_unal.png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=100, height=100))
    else:
        print("[AVISO] El archivo de logo no se encontró. El PDF se generará sin logo.")

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Resultados de prueba del backend-registro-actividades para los endpoints de patients",
        styles['Title']
    ))
    story.append(Spacer(1, 12))

    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    story.append(Paragraph(f'Fecha de generación: {fecha}', styles['Normal']))
    story.append(Spacer(1, 12))

    tabla_data = [['Nombre del Test', 'Resultado', 'Detalles']]
    for nombre, estado, detalle in resultados:
        tabla_data.append([nombre, estado, detalle[:100]])

    tabla = Table(tabla_data, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))
    story.append(tabla)
    story.append(Spacer(1, 20))

    grafico_buffer = generar_grafico_en_memoria(resultados)
    story.append(Image(grafico_buffer, width=300, height=300))

    story.append(Spacer(1, 24))
    story.append(Paragraph("Autor del informe: Anderson", styles['Normal']))
    total = len(resultados)
    exitosos = sum(1 for _, estado, _ in resultados if 'Éxito' in estado)
    story.append(Paragraph(f"Resumen: {exitosos} de {total} pruebas fueron exitosas.", styles['Normal']))
    if exitosos == total:
        story.append(Paragraph("Conclusión: Todas las pruebas pasaron correctamente. El módulo es funcional.", styles['Italic']))
    else:
        story.append(Paragraph("Conclusión: Hay fallos en algunas pruebas. Se requiere revisión del módulo.", styles['Italic']))

    doc.build(story)

if __name__ == '__main__':
    resultados = run_tests()
    nombre_pdf = obtener_nombre_pdf_incremental()
    generar_pdf(resultados, path_pdf=nombre_pdf)
    print(f"[✅] PDF generado: {nombre_pdf}")
