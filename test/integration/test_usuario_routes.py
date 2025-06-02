import pytest
from flask import json
import time

def test_get_clientes(client, admin_headers):
    response = client.get('/test/users/clientes', headers=admin_headers)
    assert response.status_code == 200

def test_create_cliente(client, admin_headers):
    unique_email = f"test{int(time.time())}@example.com"
    response = client.post('/test/users/clientes', json={
        'nombres': 'Nuevo',
        'apellidos': 'Cliente',
        'email': unique_email,
        'num_documento': str(int(time.time())),
        'tipo_doc': 1,
        'contrasena': 'password123',
        'direccion': 'Calle 123',
        'telefono': '123456789',
        'id_rol': 2
    }, headers=admin_headers)
    assert response.status_code == 201

def test_get_empleados(client, admin_headers):
    response = client.get('/test/users/empleados', headers=admin_headers)
    assert response.status_code == 200