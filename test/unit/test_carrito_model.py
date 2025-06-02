from flaskr.modelos import Carrito

def test_carrito_creation():
    carrito = Carrito(
        id_usuario=1
    )
    assert carrito.id_usuario == 1