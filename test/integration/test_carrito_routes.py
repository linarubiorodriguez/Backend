import pytest
from flask import json

def test_add_to_cart(client, user_token, test_product):
    with client:
        headers = {'Authorization': f'Bearer {user_token}'}
        response = client.post('/test/cart/agregar', json={
            'id_producto': test_product.id_producto,
            'cantidad': 2,
            'id_usuario': 2
        }, headers=headers)
        assert response.status_code == 201
        assert 'mensaje' in response.json