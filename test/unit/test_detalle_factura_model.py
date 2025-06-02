from flaskr.modelos import DetalleFactura

def test_detalle_factura_creation():
    detalle = DetalleFactura(
        cantidad=2,
        subtotal=20000.0,
        id_factura=1,
        id_producto=1
    )
    
    assert detalle.cantidad == 2
    assert detalle.subtotal == 20000.0
    assert detalle.id_factura == 1
    assert detalle.id_producto == 1