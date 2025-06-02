def test_get_animales(client):
    response = client.get('/test/products/animales')  
    print(response.data)  
    assert response.status_code == 200
    assert isinstance(response.json['animales'], list)

def test_create_animal(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}

    with open('test/test_image.jpg', 'rb') as img:
        response = client.post(
            '/test/products/animales',
            data={
                'nombre': 'Nuevo Animal',
                'estado': 'Activo',
                'imagen': (img, 'test_image.jpg')
            },
            headers=headers,
            content_type='multipart/form-data'
        )

    print(response.json) 
    assert response.status_code == 201
    assert 'animal' in response.json  
    assert 'id_animal' in response.json['animal']  