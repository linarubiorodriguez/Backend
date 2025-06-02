from flaskr.modelos import Proveedor

def test_proveedor_creation():
    proveedor = Proveedor(
        nombre="Proveedor Test",
        telefono="1234567890",
        correo="proveedor@test.com",
        estado="Activo"
    )
    assert proveedor.nombre == "Proveedor Test"
    assert proveedor.telefono == "1234567890"
    assert proveedor.correo == "proveedor@test.com"
    assert proveedor.estado == "Activo"