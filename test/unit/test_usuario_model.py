from flaskr.modelos import Usuario

def test_usuario_creation():
    usuario = Usuario(
        nombres="Juan",
        apellidos="Perez",
        email="juan@example.com",
        num_documento="123456789",
        tipo_doc=1,
        id_rol=2
    )
    usuario.contrasena = "password123"
    
    assert usuario.nombres == "Juan"
    assert usuario.apellidos == "Perez"
    assert usuario.email == "juan@example.com"
    assert usuario.check_password("password123") is True
    assert usuario.check_password("wrongpass") is False
    assert usuario.id_rol == 2