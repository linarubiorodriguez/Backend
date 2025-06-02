import pytest
from flask import json

def test_get_facturas(client, admin_headers):
    response = client.get('/test/sales/facturas', headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json['facturas'], list)

def test_create_factura(client, user_token):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.post('/test/sales/facturas', json={
        'total': 100000,
        'iva_total': 16000,
        'id_cliente': 2,
        'metodo_pago': 'tarjeta',
        'referencia_pago': 'TEST123'
    }, headers=headers)
    assert response.status_code == 201
    assert 'id_factura' in response.json