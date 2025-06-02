import pytest
from flask import json

def test_get_descuentos(client, admin_headers):
    response = client.get('/test/products/descuentos', headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json['descuentos'], list)

def test_create_descuento(client, admin_headers, test_product):
    response = client.post('/test/products/descuentos', json={
        'id_producto': test_product.id_producto,
        'porcentaje_descuento': 10,
        'fecha_inicio': '2023-01-01',
        'fecha_fin': '2023-12-31'
    }, headers=admin_headers)
    print(response.json)  # Para ver la estructura real
    assert response.status_code == 201
    assert 'descuento' in response.json  # Verifica la estructura padre
    assert 'id_descuento' in response.json['descuento']  # Accede al ID dentro de 'descuento'