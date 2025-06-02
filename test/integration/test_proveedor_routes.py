import pytest
from flask import json

def test_get_proveedores(client, admin_headers):
    response = client.get('/test/suppliers/', headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json['proveedores'], list)

def test_create_proveedor(client, admin_headers):
    response = client.post('/test/suppliers/', json={
        'nombre': 'Test Proveedor',
        'telefono': '123456789',
        'correo': 'proveedor@test.com',
        'estado': 'Activo'
    }, headers=admin_headers)
    print(response.json)  # Para ver la estructura real
    assert response.status_code == 201
    assert 'proveedor' in response.json  # Verifica la estructura padre
    assert 'id_proveedor' in response.json['proveedor']  