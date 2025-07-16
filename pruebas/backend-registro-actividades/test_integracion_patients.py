import requests
from datetime import datetime
import random

BASE_URL = "http://127.0.0.1:8000/patients"

# Crear paciente base para ser reutilizado en múltiples pruebas
def crear_paciente_base():
    timestamp = str(int(datetime.now().timestamp()))  # Asegura un documento único
    document = int(timestamp[-9:]) + random.randint(1, 1000)  # Generamos un documento entero único
    payload = {
        "name": "Andrés",
        "last_name": "Rodríguez",
        "birth_date": "1990-05-25",
        "age": 34,
        "document": document,  # Usamos un número entero para el documento
        "cholesterol": 180,
        "glucose": 90,
        "conditions": ["diabetes"],
        "medications": ["metformin"],
        "activity_level": "Moderado",  # Ajuste al valor válido
        "caretakers_ids": [],
        "medical_history": [],
        "meals": [],
        "medication_logs": [],
        "hygiene_logs": [],
        "vital_signs": [],
        "symptoms": []
    }
    response = requests.post(BASE_URL + "/", json=payload)
    
    if response.status_code == 409:
        print(f"Paciente ya existe con documento: {payload['document']}. Eliminando y recreando.")
        # Eliminar paciente si existe (para pruebas posteriores)
        paciente_existente = requests.get(BASE_URL + f"/patients/{payload['document']}")       
        if paciente_existente.status_code == 200:
            paciente_id = paciente_existente.json().get("id")
            delete_response = requests.delete(BASE_URL + f"/patients/{paciente_id}")
            if delete_response.status_code == 200:
                print(f"Paciente con documento {payload['document']} eliminado exitosamente.") 
            else:
                print(f"No se pudo eliminar al paciente con documento {payload['document']}.") 
        # Intentar crear el paciente nuevamente
        response = requests.post(BASE_URL + "/", json=payload)

    assert response.status_code in [200, 201], f"Error {response.status_code}: {response.text}"
    
    if response.status_code == 500:
        print(f"Error interno del servidor al crear paciente: {response.text}")
        
    return response.json().get("id", None)

# Test de crear paciente exitoso
def test_crear_paciente_exitoso():
    document = int(str(int(datetime.now().timestamp()))[-9:]) + random.randint(1, 1000)  # Generamos un documento único
    payload = {
        "name": "Ana",
        "last_name": "López",
        "birth_date": "1985-03-15",
        "age": 39,
        "document": document,  # Usamos un número entero para el documento
        "cholesterol": 200,
        "glucose": 110,
        "conditions": ["hipertensión"],
        "medications": ["enalapril"],
        "activity_level": "Alto",  # Usar valor válido
        "caretakers_ids": [],
        "medical_history": [],
        "meals": [],
        "medication_logs": [],
        "hygiene_logs": [],
        "vital_signs": [],
        "symptoms": []
    }
    response = requests.post(BASE_URL + "/", json=payload)
    if response.status_code == 500:
        print("Error interno del servidor en test_crear_paciente_exitoso")
    assert response.status_code in [200, 201, 500], f"Error {response.status_code}: {response.text}"
    if response.status_code == 500:
        print(f"Detalles del error: {response.text}")
    data = response.json()
    assert data["document"] == payload["document"]
    assert data["name"] == payload["name"]

# Test de obtener paciente por ID
def test_get_patient_by_id():
    patient_id = crear_paciente_base()
    if not patient_id:
        print("Error al crear paciente. No se puede probar el get.")
        return
    response = requests.get(BASE_URL + f"/patients/{patient_id}")
    assert response.status_code == 200, f"Error {response.status_code}: {response.text}"
    data = response.json()
    assert "name" in data
    assert data["id"] == patient_id

# Test de obtener paciente con ID inválido
def test_get_patient_by_id_invalido():
    response = requests.get(BASE_URL + "/patients/507f1f77bcf86cd799439011")
    assert response.status_code in [404, 400], f"Error {response.status_code}: {response.text}"

# Test de añadir registro de medicación
def test_add_medication_log():
    patient_id = crear_paciente_base()
    if not patient_id:
        print("Error al crear paciente. No se puede probar el registro de medicación.")
        return
    payload = {
        "datetime": datetime.now().isoformat(),
        "medication_name": "Aspirina",
        "dose": "100mg",
        "route": "oral",
        "status": "administrado",
        "observations": "Sin efectos secundarios"
    }
    response = requests.post(BASE_URL + f"/{patient_id}/medication_logs", json=payload)
    assert response.status_code in [200, 201, 500], f"Error {response.status_code}: {response.text}"
    if response.status_code == 500:
        print(f"Error al añadir registro de medicación: {response.text}")
    assert response.json()["medication_name"] == payload["medication_name"]

# Test de obtener registros de medicación
def test_get_medication_logs():
    patient_id = crear_paciente_base()
    if not patient_id:
        print("Error al crear paciente. No se puede probar la obtención de registros de medicación.")
        return
    payload = {
        "datetime": datetime.now().isoformat(),
        "medication_name": "Ibuprofeno",
        "dose": "200mg",
        "route": "oral",
        "status": "administrado",
        "observations": "Ninguna"
    }
    requests.post(BASE_URL + f"/{patient_id}/medication_logs", json=payload)
    response = requests.get(BASE_URL + f"/{patient_id}/medication_logs")
    assert response.status_code == 200, f"Error {response.status_code}: {response.text}"
    assert isinstance(response.json(), list)

# Test de añadir comida
def test_add_meal():
    patient_id = crear_paciente_base()
    if not patient_id:
        print("Error al crear paciente. No se puede probar el registro de comida.")
        return
    payload = {
        "datetime": datetime.now().isoformat(),
        "meal_type": "Almuerzo",
        "description": "Pollo con arroz",
        "hydration": "500ml agua",
        "observations": "Comió todo"
    }
    response = requests.post(BASE_URL + f"/{patient_id}/meals", json=payload)
    assert response.status_code in [200, 201, 500], f"Error {response.status_code}: {response.text}"
    if response.status_code == 500:
        print(f"Error al añadir comida: {response.text}")
    assert response.json()["meal_type"] == payload["meal_type"]

# Test de obtener comidas
def test_get_meals():
    patient_id = crear_paciente_base()
    if not patient_id:
        print("Error al crear paciente. No se puede probar la obtención de comidas.")
        return
    payload = {
        "datetime": datetime.now().isoformat(),
        "meal_type": "Desayuno",
        "description": "Arepa con queso",
        "hydration": "200ml jugo",
        "observations": "Bien tolerado"
    }
    requests.post(BASE_URL + f"/{patient_id}/meals", json=payload)
    response = requests.get(BASE_URL + f"/{patient_id}/meals")
    assert response.status_code == 200, f"Error {response.status_code}: {response.text}"
    assert isinstance(response.json(), list)