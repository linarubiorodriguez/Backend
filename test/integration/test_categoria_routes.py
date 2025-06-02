import pytest
from flask import json

def test_get_categorias(client):
    response = client.get('/test/products/categorias')
    assert response.status_code == 200
    assert isinstance(response.json['categorias'], list)

def test_create_categoria(client, admin_headers):
    response = client.post('/test/products/categorias',
        data={
            'nombre': 'Test Categoria',
            'descripcion': 'Descripción test',
            'imagen': (open('test/test_image.jpg', 'rb'), 'test_image.jpg')
        },
        headers=admin_headers,
        content_type='multipart/form-data'
    )
    print(response.json)  # Para ver la estructura real
    assert response.status_code == 201
    assert 'categoria' in response.json  # Verifica la estructura padre
    assert 'id_categoria' in response.json['categoria']  # Accede al ID dentro de 'categoria'