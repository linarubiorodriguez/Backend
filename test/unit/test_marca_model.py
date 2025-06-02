from flaskr.modelos import Marca

def test_marca_creation():
    marca = Marca(
        nombre="Marca Test",
        estado="Activo",
        id_proveedor=1,
        imagen="marca.jpg"
    )
    assert marca.nombre == "Marca Test"
    assert marca.estado == "Activo"
    assert marca.id_proveedor == 1
    assert marca.imagen == "marca.jpg"