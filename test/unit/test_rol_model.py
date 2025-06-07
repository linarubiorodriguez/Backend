from flaskr.modelos import Rol

def test_rol_creation():
    rol = Rol(
        nombre="Cajero",
        descripcion="Usuario del sistema"
    )
    assert rol.nombre == "Cajero"
    assert rol.descripcion == "Usuario del sistema"