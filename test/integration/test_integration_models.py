import pytest
from faker import Faker
from flaskr.modelos import db, Usuario, Producto, Factura, DetalleFactura, Carrito, DetalleCarrito

faker = Faker()

def test_create_user_product_factura_cart(app):
    with app.app_context():
        from flaskr.modelos import Usuario, Producto, Factura, DetalleFactura, Carrito, DetalleCarrito
        
        # Crear usuario
        user = Usuario(
            nombres="Int",
            apellidos="Test",
            email="inttest@example.com",
            num_documento="111222333",
            tipo_doc=1,
            id_rol=2
        )
        user.contrasena = "password123"
        db.session.add(user)
        db.session.commit()
        
        # Crear producto
        product = Producto(
            nombre="Producto Int",
            descripcion="Desc",
            precio=10000,
            stock=10,
            id_categoria=1,
            id_marca=1,
            id_animal=1
        )
        db.session.add(product)
        db.session.commit()
        
        # Crear carrito
        cart = Carrito(id_usuario=user.id_usuario)
        db.session.add(cart)
        db.session.commit()
        
        # Añadir producto al carrito
        cart_item = DetalleCarrito(
            id_carrito=cart.id_carrito,
            id_producto=product.id_producto,
            cantidad=2
        )
        db.session.add(cart_item)
        
        # Crear factura
        factura = Factura(
            total=20000,
            iva_total=3200,
            id_cliente=user.id_usuario
        )
        db.session.add(factura)
        db.session.commit()
        
        # Crear detalle factura
        detalle = DetalleFactura(
            id_factura=factura.id_factura,
            id_producto=product.id_producto,
            cantidad=2,
            subtotal=20000
        )
        db.session.add(detalle)
        db.session.commit()
        
        assert user.id_usuario is not None
        assert product.id_producto is not None
        assert cart.id_carrito is not None
        assert factura.id_factura is not None