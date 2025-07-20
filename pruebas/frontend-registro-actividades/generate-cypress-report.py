import os
import json
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import matplotlib.pyplot as plt

def cargar_resultados_json(path_json):
    with open(path_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
    resultados = []
    for test in data["tests"]:
        nombre = test.get("name", "Sin nombre")
        estado = "✅ Éxito" if test.get("status") == "passed" else "❌ Fallo/Error"
        # Si la prueba pasó, el detalle siempre será "Pasó la prueba sin novedad"
        if test.get("status") == "passed":
            detalle = "Pasó la prueba sin novedad"
        else:
            detalle = test.get("details", "")
        resultados.append((nombre, estado, detalle))
    return resultados

def generar_grafico_en_memoria(resultados):
    labels = ['Éxito', 'Fallo/Error']
    success = sum(1 for _, status, _ in resultados if 'Éxito' in status)
    fail = len(resultados) - success
    sizes = [success, fail]
    plt.figure(figsize=(4, 4))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#3CB371', '#FF6347'])
    plt.axis('equal')
    plt.title('Resumen de Resultados')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

def obtener_nombre_pdf_incremental(base_name='reporte_frontend_crear_editar_paciente'):
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
    # Ajusta los márgenes para que el ancho útil sea ~7.5 pulgadas (carta menos 1" total márgenes laterales)
    doc = SimpleDocTemplate(path_pdf, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    logo_path = os.path.join(os.path.dirname(__file__), "logo_unal.png")
    try:
        if os.path.exists(logo_path):
            story.append(Image(logo_path, width=100, height=100))
        else:
            story.append(Paragraph("[ADVERTENCIA] No se encontró el archivo logo_unal.png en la carpeta del script.", styles['Normal']))
    except Exception as e:
        story.append(Paragraph(f"[ADVERTENCIA] No se pudo cargar el logo: {str(e)}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Resultados de prueba del frontend para la funcionalidad de crear y editar actividades",
        styles['Title']
    ))
    story.append(Spacer(1, 12))
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    story.append(Paragraph(f'Fecha de generación: {fecha}', styles['Normal']))
    story.append(Spacer(1, 12))
    tabla_data = [['Nombre del Test', 'Resultado', 'Detalles']]
    for nombre, estado, detalle in resultados:
        tabla_data.append([nombre, estado, detalle[:280]])
    # Anchos de columna (total ~7.5 pulgadas para carta menos márgenes)
    col1 = 2.2*inch  # Nombre del Test
    col2 = 1.2*inch  # Resultado
    col3 = 4.1*inch  # Detalles
    tabla = Table(tabla_data, repeatRows=1, colWidths=[col1, col2, col3])
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
    story.append(Paragraph("Autor del informe: Equipo QA Frontend", styles['Normal']))
    total = len(resultados)
    exitosos = sum(1 for _, estado, _ in resultados if 'Éxito' in estado)
    story.append(Paragraph(f"Resumen: {exitosos} de {total} pruebas fueron exitosas.", styles['Normal']))
    if exitosos == total:
        story.append(Paragraph("Conclusión: Todas las pruebas pasaron correctamente. El módulo es funcional.", styles['Italic']))
    else:
        story.append(Paragraph("Conclusión: Hay fallos en algunas pruebas. Se requiere revisión del módulo.", styles['Italic']))
    doc.build(story)

if __name__ == '__main__':
    ruta_json = os.path.join(os.path.dirname(__file__), "resultados/resultados_frontend.json")
    resultados = cargar_resultados_json(ruta_json)
    nombre_pdf = obtener_nombre_pdf_incremental()
    generar_pdf(resultados, path_pdf=nombre_pdf)
    print(f"[✅] PDF generado: {nombre_pdf}")