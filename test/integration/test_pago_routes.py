import uuid
from flaskr.modelos import db, FormularioPago, Factura, DetalleFactura
from datetime import datetime, timedelta
from flaskr.modelos.modelos import Producto

def test_procesar_pago_tarjeta(client, user_token, app):
    with app.app_context():
        # 1. Crear producto FRESCO para evitar conflictos de sesión
        producto = Producto(
            nombre="Producto Test Pago",
            descripcion="Descripción test",
            precio=50000,
            stock=10,
            id_categoria=1,
            id_marca=1,
            id_animal=1,
            estado="Activo",
            imagen="producto.jpg"
        )
        
        db.session.add(producto)
        db.session.commit()
        db.session.refresh(producto)
        # 2. Crear factura
        factura = Factura(
            total=150000,
            iva_total=24000,
            estado="Pendiente",
            id_cliente=2,
            metodo_pago=None,
            referencia_pago=None
        )
        
        # 3. Crear detalle usando ID del producto en lugar del objeto
        detalle = DetalleFactura(
            cantidad=3,
            subtotal=150000,
            id_producto=producto.id_producto  # Usar ID en lugar de relación
        )
        factura.detalles.append(detalle)
        
        db.session.add(factura)
        db.session.commit()

        # 4. Procesar pago
        headers = {'Authorization': f'Bearer {user_token}'}
        response = client.post('/test/sales/pagos/procesar', 
            json={
                'id_factura': factura.id_factura,
                'tipo_pago': 'tarjeta',
                'numero_tarjeta': '4111111111111111',
                'titular': 'Test User',
                'fecha_expiracion': '12/25',
                'codigo_seguridad': '123'
            },
            headers=headers
        )

        # 5. Verificaciones
        assert response.status_code == 201
        assert response.json['mensaje'] == "Pago procesado exitosamente"
        
        # Verificar cambios en BD
        factura_actualizada = Factura.query.get(factura.id_factura)
        assert factura_actualizada.estado == "Pagada"
        
        producto_actualizado = Producto.query.get(producto.id_producto)
        assert producto_actualizado.stock == 7  # 10 inicial - 3 comprados

        # Limpieza
        FormularioPago.query.filter_by(id_factura=factura.id_factura).delete()
        db.session.delete(detalle)
        db.session.delete(factura)
        db.session.delete(producto)
        db.session.commit()

def test_procesar_pago_efectivo(client, user_token, app):
    with app.app_context():
        # Similar al test anterior pero con tipo 'efectivo'
        producto = Producto(
            nombre="Producto Test Efectivo",
            descripcion="Descripción test",
            precio=40000,
            stock=5,
            id_categoria=1,
            id_marca=1,
            id_animal=1,
            estado="Activo"
        )
        db.session.add(producto)
        db.session.commit()

        factura = Factura(
            total=80000,
            iva_total=12800,
            estado="Pendiente",
            id_cliente=2
        )
        
        detalle = DetalleFactura(
            cantidad=2,
            subtotal=80000,
            id_producto=producto.id_producto
        )
        factura.detalles.append(detalle)
        
        db.session.add(factura)
        db.session.commit()

        response = client.post('/test/sales/pagos/procesar', 
            json={
                'id_factura': factura.id_factura,
                'tipo_pago': 'efectivo'
            },
            headers={'Authorization': f'Bearer {user_token}'}
        )

        assert response.status_code == 201
        assert response.json['mensaje'] == "Pago procesado exitosamente"
        
        factura_actualizada = Factura.query.get(factura.id_factura)
        assert factura_actualizada.estado == "Pendiente"  # Efectivo queda pendiente
        
        # Stock no debe cambiar hasta confirmación
        producto_actualizado = Producto.query.get(producto.id_producto)
        assert producto_actualizado.stock == 5

        # Limpieza
        FormularioPago.query.filter_by(id_factura=factura.id_factura).delete()
        db.session.delete(detalle)
        db.session.delete(factura)
        db.session.delete(producto)
        db.session.commit()