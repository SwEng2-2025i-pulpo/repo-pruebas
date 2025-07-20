import requests
from datetime import datetime
import random

BASE_URL = "http://127.0.0.1:8001/api/pdf/patient"

def test_generar_pdf_exitoso():
    # ID de paciente válido (reemplázalo con un ID válido de tu base de datos)
    valid_patient_id = "6871a921d7e09f4bec1f14bb"  # ID actualizado
    
    # Realiza la solicitud GET para obtener el PDF del paciente
    response = requests.get(f"{BASE_URL}/{valid_patient_id}")
    
    # Verifica que la respuesta sea exitosa con código 200
    assert response.status_code == 200, f"Error: {response.status_code} - {response.text}"
    
    # Verifica que el tipo de contenido sea PDF
    assert response.headers["Content-Type"] == "application/pdf", f"Error: El tipo de contenido no es PDF. {response.headers}"
    
    # Verifica que los encabezados estén configurados correctamente
    assert "Content-Disposition" in response.headers, "Error: No se encontró el encabezado 'Content-Disposition'"
    
    # Verifica que el contenido del archivo no esté vacío
    assert len(response.content) > 0, "Error: El contenido del PDF está vacío."

def test_id_invalido():
    # ID de paciente inválido
    invalid_patient_id = "invalid_id_12345"
    
    # Realiza la solicitud GET con un ID inválido
    response = requests.get(f"{BASE_URL}/{invalid_patient_id}")
    
    # Verifica que la respuesta sea 400 (Bad Request)
    assert response.status_code == 400, f"Error: {response.status_code} - {response.text}"
    
    # Verifica que el mensaje de error esté presente
    assert "detail" in response.json(), "Error: El mensaje de error no está presente."

def test_paciente_no_encontrado():
    # ID de paciente que no existe en la base de datos
    non_existent_patient_id = "507f1f77bcf86cd799439011"
    
    # Realiza la solicitud GET con un ID que no existe
    response = requests.get(f"{BASE_URL}/{non_existent_patient_id}")
    
    # Verifica que la respuesta sea 404 (Not Found)
    assert response.status_code == 404, f"Error: {response.status_code} - {response.text}"
    
    # Verifica que el mensaje de error esté presente
    assert "detail" in response.json(), "Error: El mensaje de error no está presente."

def test_error_interno_servidor():
    # Simula un error interno (por ejemplo, desconectando la base de datos o forzando un error en el servidor)
    # Aquí puedes simular el error modificando la lógica interna del servidor o la base de datos

    # Realiza la solicitud GET con un ID válido
    response = requests.get(f"{BASE_URL}/6871a921d7e09f4bec1f14bb")  # ID de paciente válido actualizado
    
    # Forzar un error en el servidor
    assert response.status_code == 500, f"Error: {response.status_code} - {response.text}"
    
    # Verifica que el mensaje de error esté presente
    assert "detail" in response.json(), "Error: El mensaje de error no está presente."
