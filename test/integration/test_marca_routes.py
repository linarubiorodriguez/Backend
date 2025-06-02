import pytest
from flask import json

def test_get_marcas(client):
    response = client.get('/test/products/marcas')
    assert response.status_code == 200
    assert isinstance(response.json['marcas'], list)

def test_create_marca(client, admin_headers, test_proveedor):
    response = client.post('/test/products/marcas', 
        data={
            'nombre': 'Test Marca',
            'id_proveedor': test_proveedor.id_proveedor,
            'estado': 'Activo',
            'imagen': (open('test/test_image.jpg', 'rb'), 'test_image.jpg')
        },
        headers=admin_headers,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201
    assert 'marca' in response.json
    assert 'id_marca' in response.json['marca']