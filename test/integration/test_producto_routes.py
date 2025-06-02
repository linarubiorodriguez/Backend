import pytest
from flask import json

def test_get_productos(client):
    response = client.get('/test/products/')
    assert response.status_code == 200
    assert isinstance(response.json['productos'], list)

def test_create_producto(client, admin_headers, test_categoria, test_marca, test_animal):
    with client:
        response = client.post('/test/products/', 
            data={
                'nombre': 'Test Producto',
                'descripcion': 'Descripción test',
                'precio': '10000',
                'stock': '50',
                'id_categoria': str(test_categoria.id_categoria),
                'id_marca': str(test_marca.id_marca),
                'id_animal': str(test_animal.id_animal),
                'estado': 'Activo',
                'imagen': (open('test/test_image.jpg', 'rb'), 'test_image.jpg')
            },
            headers=admin_headers,
            content_type='multipart/form-data'
        )
    print(response.json)  # Para ver la estructura real
    assert response.status_code == 201
    assert 'producto' in response.json  # Verifica la estructura padre
    assert 'id_producto' in response.json['producto']  