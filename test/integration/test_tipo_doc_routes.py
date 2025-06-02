import pytest
from flask import json

def test_create_tipo_doc(client, admin_headers):
    response = client.post('/test/users/tipo_doc', json={
        'Nombre': 'TI',
        'Descripcion': 'Tarjeta de Identidad'
    }, headers=admin_headers)
    print(response.json)  # Para ver la estructura real
    assert response.status_code == 201
    assert 'tipo_doc' in response.json  # Verifica la estructura padre
    assert 'id_TipoDocumento' in response.json['tipo_doc'] 
