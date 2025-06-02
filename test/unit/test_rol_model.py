from flaskr.modelos import Rol

def test_rol_creation():
    rol = Rol(
        Nombre="Cajero",
        Descripcion="Usuario del sistema"
    )
    assert rol.Nombre == "Cajero"
    assert rol.Descripcion == "Usuario del sistema"