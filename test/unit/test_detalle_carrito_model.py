from flaskr.modelos import DetalleCarrito

def test_detalle_carrito_creation():
    detalle = DetalleCarrito(
        id_carrito=1,
        id_producto=1,
        cantidad=3
    )
    
    assert detalle.id_carrito == 1
    assert detalle.id_producto == 1
    assert detalle.cantidad == 3