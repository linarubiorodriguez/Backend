import pytest
from flask import json

def test_login(client):
    response = client.post('/test/auth/login', json={
        'email': 'admin@test.com',
        'contrasena': 'admin123'
    })
    assert response.status_code == 200
    assert 'token_de_acceso' in response.json

def test_signup(client):
    response = client.post('/test/auth/signin', json={
        'nombres': 'New',
        'apellidos': 'User',
        'email': 'newuser@example.com',
        'num_documento': '123123123',
        'tipo_doc': 1,
        'contrasena': 'password123',
        'direccion': 'Calle 123'
    })
    assert response.status_code == 200