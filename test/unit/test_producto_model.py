from flaskr.modelos import Producto
from datetime import datetime, timedelta

def test_producto_creation():
    producto = Producto(
        nombre="Producto Test",
        descripcion="Descripción test",
        precio=10000.0,
        stock=50,
        imagen="producto.jpg",
        estado="Disponible",
        id_categoria=1,
        id_marca=1,
        id_animal=1,
        fecha_inicio_descuento=datetime.utcnow(),
        fecha_fin_descuento=datetime.utcnow() + timedelta(days=7)
    )
    
    assert producto.nombre == "Producto Test"
    assert producto.precio == 10000.0
    assert producto.stock == 50
    assert producto.id_categoria == 1
    assert producto.id_marca == 1
    assert producto.id_animal == 1