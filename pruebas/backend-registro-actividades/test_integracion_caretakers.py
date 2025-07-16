import requests
from datetime import datetime
import random


BASE_URL = "http://127.0.0.1:8000/caretakers"


def test_crear_caretaker_exitoso():
    # Utiliza un timestamp para garantizar la unicidad del correo y evitar duplicados
    timestamp = str(int(datetime.now().timestamp()))
    payload = {
        "name": "Juan Perez",
        "email": f"juan.perez.{timestamp}@example.com",
        "passwordHash": "hashedpwd123",  # Simula un hash de contraseña en lugar de texto plano
        "role": "user"  # Rol estándar para el usuario
    }
    
    # Realiza la solicitud POST para crear un nuevo caretakera
    response = requests.post(BASE_URL + "/", json=payload)
    
    # Verifica que la respuesta sea exitosa con código 201 (creado)
    assert response.status_code == 201
    
    # Extrae los datos de la respuesta en formato JSON
    data = response.json()
    
    # Validación de los campos retornados por el backend
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]
    assert data["role"] == payload["role"]
    assert "id" in data  # Asegura que el campo "id" esté presente en la respuesta

def test_crear_caretaker_email_duplicado():
    timestamp = str(int(datetime.now().timestamp()))
    email = f"ana.ruiz.{timestamp}@example.com"
    payload = {
        "name": "Ana Ruiz",
        "email": email,
        "passwordHash": "hashedpwd456",  # Simulación de contraseña segura
        "role": "admin"  # Rol de administrador para el usuario
    }
    
    # Primer intento de crear el caretakera: debe ser exitoso
    resp1 = requests.post(BASE_URL + "/", json=payload)
    assert resp1.status_code == 201
    
    # Segundo intento con el mismo correo: debe fallar debido a duplicado
    resp2 = requests.post(BASE_URL + "/", json=payload)
    assert resp2.status_code == 206  # El código 206 indica un conflicto con el correo
    assert "El correo ya existe" in resp2.json()["detail"]  # Verifica que el mensaje de error es adecuado

def test_get_all_caretakers():
    # Realiza la solicitud GET para obtener la lista de todos los caretakers
    response = requests.get(BASE_URL + "/")
    
    # Verifica que la respuesta sea exitosa con código 200 (OK)
    assert response.status_code == 200
    
    # Extrae la lista de caretakers en formato JSON
    caretakers_list = response.json()
    
    # Asegura que la respuesta sea una lista
    assert isinstance(caretakers_list, list)
    
    # Verifica que cada elemento de la lista tenga los campos necesarios
    for caretaker in caretakers_list:
        assert "id" in caretaker
        assert "name" in caretaker
        assert "email" in caretaker
        assert "passwordHash" in caretaker
        assert "role" in caretaker
        # Verifica que los valores de los campos sean válidos
        assert isinstance(caretaker["name"], str)
        assert isinstance(caretaker["email"], str)
        assert caretaker["role"] in ["user", "admin"]  # Verifica que el rol sea válido

def test_get_caretaker_by_id():
    # Genera un email único usando timestamp para evitar duplicados
    timestamp = str(int(datetime.now().timestamp()))
    payload = {
        "name": "Carlos Gómez",
        "email": f"carlos.gomez.{timestamp}@example.com",
        "passwordHash": "hashedpwd789",
        "role": "user"
    }
    
    # Crea un nuevo caretakera
    create_resp = requests.post(BASE_URL + "/", json=payload)
    assert create_resp.status_code == 201
    
    # Obtiene el ID del nuevo caretakera creado
    caretaker_id = create_resp.json()["id"]
    
    # Realiza una solicitud GET para obtener el caretakera por ID
    response = requests.get(BASE_URL + f"/{caretaker_id}")
    
    # Verifica que la respuesta sea exitosa
    assert response.status_code == 200
    
    # Extrae los datos de la respuesta y valida que coincidan con los datos enviados
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]
    assert data["role"] == payload["role"]
    assert data["id"] == caretaker_id  # Verifica que el ID coincida

def test_get_caretaker_by_id_invalido():
    # Utiliza un ObjectId que es válido en formato, pero no existe en la base de datos
    fake_id = "507f1f77bcf86cd799439011"
    
    # Realiza la solicitud GET para obtener el caretakera con un ID inválido
    response = requests.get(BASE_URL + f"/{fake_id}")
    
    # Acepta tanto 404 (No encontrado) como 500 (Error interno del servidor)
    assert response.status_code in (404, 500)
    
    # Verifica que la respuesta tenga contenido y sea un JSON
    try:
        data = response.json()  # Intenta obtener la respuesta como JSON
    except ValueError:
        data = None  # Si no es un JSON, asigna None
    
    # Si la respuesta es 500 (error interno), verifica que no haya datos JSON válidos
    if response.status_code == 500:
        assert data is None  # Si es un error 500, no se espera que haya JSON válido
        assert "Internal Server Error" in response.text  # Verifica que el mensaje de error esté presente
    elif response.status_code == 404:
        assert data is not None  # Si es un 404, debería devolver un JSON
        assert "detail" in data and "not found" in data["detail"].lower()  # Verifica que el 404 tenga un mensaje adecuado