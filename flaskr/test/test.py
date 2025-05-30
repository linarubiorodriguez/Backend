import json
import hashlib
from unittest import TestCase
from datetime import datetime, timedelta
from sqlalchemy import text  # Importación añadida para solucionar el error

from faker import Faker
from faker.generator import random
from ..modelos import db, Usuario, Producto, Categoria, Marca, Animal, Descuento, TipoDoc, Rol, Proveedor, Carrito, DetalleCarrito, Factura, DetalleFactura
from flaskr import create_app
import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

class TestBase(TestCase):
    def setUp(self):
        # Configuración inicial mejorada
        self.data_factory = Faker()
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        # Establecer contexto de aplicación explícitamente
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Reset completo de la base de datos
        db.session.close()
        db.drop_all()
        db.create_all()
        
        # Configurar autoincremento para MySQL (si es necesario)
        if 'mysql' in self.app.config['SQLALCHEMY_DATABASE_URI']:
            db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))  # Modificado para usar text()
            db.session.commit()
        
        # Crear datos iniciales
        self.create_initial_data()
        
        # Crear usuario de prueba
        self.create_test_user_and_login()

    def tearDown(self):
        # Limpieza más exhaustiva
        db.session.remove()
        
        # Resetear autoincrementos en MySQL (con text())
        if 'mysql' in self.app.config['SQLALCHEMY_DATABASE_URI']:
            tables = db.inspect(db.engine).get_table_names()
            for table in tables:
                db.session.execute(text(f'ALTER TABLE {table} AUTO_INCREMENT = 1;'))  # Modificado para usar text()
            db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))  # Modificado para usar text()
        
        db.drop_all()
        db.session.commit()
        self.app_context.pop()

    def create_initial_data(self):
        try:
            # Verificar existencia antes de crear
            if not Rol.query.filter_by(Nombre="Cliente").first():
                db.session.add(Rol(Nombre="Cliente", Descripcion="Usuario cliente"))
            
            if not Rol.query.filter_by(Nombre="Empleado").first():
                db.session.add(Rol(Nombre="Empleado", Descripcion="Usuario empleado"))

            if not TipoDoc.query.filter_by(Nombre="Cédula").first():
                db.session.add(TipoDoc(Nombre="Cédula", Descripcion="Cédula de ciudadanía"))

            if not Categoria.query.filter_by(nombre="Alimentos").first():
                db.session.add(Categoria(nombre="Alimentos", descripcion="Alimentos para mascotas"))

            # Proveedor con nombre único por prueba
            proveedor_nombre = f"Proveedor Test {self.data_factory.unique.word()}"
            if not Proveedor.query.filter_by(nombre=proveedor_nombre).first():
                proveedor = Proveedor(
                    nombre=proveedor_nombre,
                    telefono=self.data_factory.unique.phone_number(),
                    correo=self.data_factory.unique.email(),
                    estado="Activo"
                )
                db.session.add(proveedor)
                db.session.flush()  # Para obtener el ID sin commit

                # Marca con nombre único
                marca_nombre = f"Marca Test {self.data_factory.unique.word()}"
                if not Marca.query.filter_by(nombre=marca_nombre).first():
                    db.session.add(Marca(
                        nombre=marca_nombre,
                        estado="Activo",
                        id_proveedor=proveedor.id_proveedor
                    ))

            # Animal con nombre único
            animal_nombre = f"Animal Test {self.data_factory.unique.word()}"
            if not Animal.query.filter_by(nombre=animal_nombre).first():
                db.session.add(Animal(
                    nombre=animal_nombre,
                    estado="Activo"
                ))

            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            raise e

    def create_test_user_and_login(self):
        try:
            # Datos únicos para cada prueba
            email = self.data_factory.unique.email()
            num_documento = self.data_factory.unique.ssn()
            
            usuario_nuevo = Usuario(
                nombres=f"Test {self.data_factory.unique.first_name()}",
                apellidos=self.data_factory.unique.last_name(),
                telefono=self.data_factory.unique.phone_number(),
                email=email,
                tipo_doc=1,
                num_documento=num_documento,
                direccion=self.data_factory.address(),
                id_rol=2
            )
            contrasena = 'T1$' + self.data_factory.unique.word()
            usuario_nuevo.contrasena = contrasena
            
            db.session.add(usuario_nuevo)
            db.session.commit()

            # Login
            respuesta = self.client.post(
                "/login",
                data=json.dumps({"email": email, "contrasena": contrasena}),
                headers={'Content-Type': 'application/json'}
            )
            datos = json.loads(respuesta.get_data())
            
            self.token = datos["token_de_acceso"]
            self.usuario_id = datos["usuario"]
            
        except Exception as e:
            db.session.rollback()
            raise e

class TestProducto(TestBase):
    def test_crear_producto(self):
        try:
            # Datos del producto con valores únicos
            nombre_nuevo_producto = f"Producto {self.data_factory.unique.word()}"
            descripcion_nuevo_producto = self.data_factory.text()
            precio_nuevo_producto = round(random.uniform(1, 100), 2)
            stock_nuevo_producto = random.randint(1, 100)

            nuevo_producto = {
                "nombre": nombre_nuevo_producto,
                "descripcion": descripcion_nuevo_producto,
                "precio": precio_nuevo_producto,
                "stock": stock_nuevo_producto,
                "id_categoria": 1,
                "id_marca": 1,
                "id_animal": 1
            }

            endpoint_productos = "/PrivProd"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }

            resultado_nuevo_producto = self.client.post(
                endpoint_productos,
                data=json.dumps(nuevo_producto),
                headers=headers
            )

            datos_respuesta = json.loads(resultado_nuevo_producto.get_data())

            self.assertEqual(resultado_nuevo_producto.status_code, 201)
            self.assertEqual(datos_respuesta['nombre'], nombre_nuevo_producto)
            self.assertEqual(datos_respuesta['descripcion'], descripcion_nuevo_producto)
            self.assertEqual(float(datos_respuesta['precio']), float(precio_nuevo_producto))
            self.assertEqual(datos_respuesta['stock'], stock_nuevo_producto)
            self.assertIsNotNone(datos_respuesta['id_producto'])
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_obtener_productos(self):
        try:
            # Crear productos de prueba con nombres únicos
            for i in range(5):
                producto = Producto(
                    nombre=f"Producto Test {i} {self.data_factory.unique.word()}",
                    descripcion=f"Descripción test {i}",
                    precio=round(random.uniform(1, 100), 2),
                    stock=random.randint(1, 100),
                    id_categoria=1,
                    id_marca=1,
                    id_animal=1
                )
                db.session.add(producto)
            db.session.commit()

            # Obtener productos
            endpoint_productos = "/PrivProd"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.get(
                endpoint_productos,
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 200)
            self.assertGreaterEqual(len(datos_respuesta['productos']), 5)
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_actualizar_producto(self):
        try:
            # Crear producto de prueba con nombre único
            producto = Producto(
                nombre=f"Producto Original {self.data_factory.unique.word()}",
                descripcion="Descripción original",
                precio=10.99,
                stock=50,
                id_categoria=1,
                id_marca=1,
                id_animal=1
            )
            db.session.add(producto)
            db.session.commit()

            # Actualizar producto
            producto_actualizado = {
                "nombre": f"Producto Actualizado {self.data_factory.unique.word()}",
                "descripcion": "Descripción actualizada",
                "precio": 15.99,
                "stock": 30
            }

            endpoint_producto = f"/PrivProd/{producto.id_producto}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.put(
                endpoint_producto,
                data=json.dumps(producto_actualizado),
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 200)
            self.assertEqual(datos_respuesta['nombre'], producto_actualizado['nombre'])
            self.assertEqual(datos_respuesta['descripcion'], producto_actualizado['descripcion'])
            self.assertEqual(float(datos_respuesta['precio']), producto_actualizado['precio'])
            self.assertEqual(datos_respuesta['stock'], producto_actualizado['stock'])
            
        except Exception as e:
            db.session.rollback()
            raise e

class TestUsuario(TestBase):
    def test_registro_usuario(self):
        try:
            # Datos de usuario con valores únicos
            nuevo_usuario = {
                "nombres": f"Test {self.data_factory.unique.first_name()}",
                "apellidos": self.data_factory.unique.last_name(),
                "telefono": self.data_factory.unique.phone_number(),
                "email": self.data_factory.unique.email(),
                "tipo_doc": 1,
                "num_documento": self.data_factory.unique.ssn(),
                "direccion": self.data_factory.address(),
                "contrasena": "Test123$"
            }

            endpoint = "/signin"
            headers = {'Content-Type': 'application/json'}
            resultado = self.client.post(
                endpoint,
                data=json.dumps(nuevo_usuario),
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 201)
            self.assertEqual(datos_respuesta['mensaje'], 'Usuario creado exitosamente')
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_login_usuario(self):
        try:
            # Crear usuario de prueba con datos únicos
            email = self.data_factory.unique.email()
            contrasena = "Test123$"
            
            usuario = Usuario(
                nombres=f"Test {self.data_factory.unique.first_name()}",
                apellidos=self.data_factory.unique.last_name(),
                telefono=self.data_factory.unique.phone_number(),
                email=email,
                tipo_doc=1,
                num_documento=self.data_factory.unique.ssn(),
                direccion=self.data_factory.address(),
                id_rol=2
            )
            usuario.contrasena = contrasena
            db.session.add(usuario)
            db.session.commit()

            # Login
            login_data = {
                "email": email,
                "contrasena": contrasena
            }

            endpoint = "/login"
            headers = {'Content-Type': 'application/json'}
            resultado = self.client.post(
                endpoint,
                data=json.dumps(login_data),
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 200)
            self.assertEqual(datos_respuesta['mensaje'], 'Inicio de sesión exitoso')
            self.assertIsNotNone(datos_respuesta['token_de_acceso'])
            self.assertIsNotNone(datos_respuesta['usuario'])
            
        except Exception as e:
            db.session.rollback()
            raise e

class TestCarrito(TestBase):
    def setUp(self):
        super().setUp()
        try:
            # Crear producto de prueba con nombre único
            self.producto = Producto(
                nombre=f"Producto Test {self.data_factory.unique.word()}",
                descripcion="Descripción test",
                precio=10.99,
                stock=50,
                id_categoria=1,
                id_marca=1,
                id_animal=1
            )
            db.session.add(self.producto)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_agregar_producto_carrito(self):
        try:
            # Agregar producto al carrito
            carrito_data = {
                "id_usuario": self.usuario_id,
                "id_producto": self.producto.id_producto,
                "cantidad": 2
            }

            endpoint = "/Carrito/agregar"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.post(
                endpoint,
                data=json.dumps(carrito_data),
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 201)
            self.assertEqual(datos_respuesta['mensaje'], 'Producto agregado al carrito exitosamente.')
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_obtener_carrito(self):
        try:
            # Primero agregar un producto al carrito
            carrito = Carrito(id_usuario=self.usuario_id)
            db.session.add(carrito)
            db.session.commit()

            detalle = DetalleCarrito(
                id_carrito=carrito.id_carrito,
                id_producto=self.producto.id_producto,
                cantidad=2
            )
            db.session.add(detalle)
            db.session.commit()

            # Obtener el carrito
            endpoint = f"/Carrito/{self.usuario_id}"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.get(
                endpoint,
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 200)
            self.assertEqual(len(datos_respuesta['productos']), 1)
            self.assertEqual(datos_respuesta['productos'][0]['id_producto'], self.producto.id_producto)
            self.assertEqual(datos_respuesta['productos'][0]['cantidad'], 2)
            
        except Exception as e:
            db.session.rollback()
            raise e

class TestOrden(TestBase):
    def setUp(self):
        super().setUp()
        try:
            # Crear producto de prueba con stock
            self.producto = Producto(
                nombre=f"Producto Test {self.data_factory.unique.word()}",
                descripcion="Descripción test",
                precio=10.99,
                stock=50,
                id_categoria=1,
                id_marca=1,
                id_animal=1
            )
            db.session.add(self.producto)
            db.session.commit()

            # Agregar producto al carrito
            self.carrito = Carrito(id_usuario=self.usuario_id)
            db.session.add(self.carrito)
            db.session.commit()

            self.detalle = DetalleCarrito(
                id_carrito=self.carrito.id_carrito,
                id_producto=self.producto.id_producto,
                cantidad=2
            )
            db.session.add(self.detalle)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_procesar_compra(self):
        try:
            # Procesar la orden
            endpoint = f"/Carrito/procesar/{self.usuario_id}"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.post(
                endpoint,
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 200)
            self.assertEqual(datos_respuesta['mensaje'], 'Factura creada exitosamente. Proceda al pago.')
            self.assertIsNotNone(datos_respuesta['id_factura'])
            self.assertEqual(len(datos_respuesta['productos']), 1)
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_confirmar_pago(self):
        try:
            # Crear factura de prueba
            factura = Factura(
                fecha_factura=datetime.utcnow(),
                total=21.98,  # 2 * 10.99
                iva_total=3.52,  # 16% of 21.98
                estado="Pendiente",
                fecha_vencimiento=datetime.utcnow() + timedelta(days=7),
                id_cliente=self.usuario_id
            )
            db.session.add(factura)
            db.session.flush()

            # Agregar detalle de factura
            detalle = DetalleFactura(
                id_factura=factura.id_factura,
                id_producto=self.producto.id_producto,
                cantidad=2,
                subtotal=21.98
            )
            db.session.add(detalle)
            db.session.commit()

            # Confirmar pago
            endpoint = f"/confirmar-pago/{factura.id_factura}"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.post(
                endpoint,
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 200)
            self.assertEqual(datos_respuesta['mensaje'], 'Pago confirmado exitosamente. Carrito vaciado y stock actualizado.')
            
            # Verificar que el stock se actualizó
            producto_actualizado = Producto.query.get(self.producto.id_producto)
            self.assertEqual(producto_actualizado.stock, 48)  # Original 50 - 2
            
        except Exception as e:
            db.session.rollback()
            raise e

class TestMarca(TestBase):
    def test_crear_marca(self):
        try:
            # Datos de marca con nombre único
            nueva_marca = {
                "nombre": f"Nueva Marca {self.data_factory.unique.word()}",
                "id_proveedor": 1
            }

            endpoint = "/PrivMarcas"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.post(
                endpoint,
                data=json.dumps(nueva_marca),
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 201)
            self.assertEqual(datos_respuesta['mensaje'], 'Marca agregada exitosamente.')
            self.assertEqual(datos_respuesta['marca']['nombre'], nueva_marca['nombre'])
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_actualizar_marca(self):
        try:
            # Crear marca de prueba con nombre único
            marca = Marca(
                nombre=f"Marca Original {self.data_factory.unique.word()}",
                estado="Activo",
                id_proveedor=1
            )
            db.session.add(marca)
            db.session.commit()

            # Actualizar marca
            marca_actualizada = {
                "nombre": f"Marca Actualizada {self.data_factory.unique.word()}",
                "estado": "Inactivo"
            }

            endpoint = f"/PrivMarca/{marca.id_marca}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.put(
                endpoint,
                data=json.dumps(marca_actualizada),
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 200)
            self.assertEqual(datos_respuesta['mensaje'], 'Marca actualizada exitosamente.')
            self.assertEqual(datos_respuesta['marca']['nombre'], marca_actualizada['nombre'])
            self.assertEqual(datos_respuesta['marca']['estado'], marca_actualizada['estado'])
            
        except Exception as e:
            db.session.rollback()
            raise e

class TestDescuento(TestBase):
    def setUp(self):
        super().setUp()
        try:
            # Crear producto de prueba con nombre único
            self.producto = Producto(
                nombre=f"Producto con Descuento {self.data_factory.unique.word()}",
                descripcion="Descripción test",
                precio=100.00,
                stock=50,
                id_categoria=1,
                id_marca=1,
                id_animal=1
            )
            db.session.add(self.producto)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_crear_descuento(self):
        try:
            # Datos de descuento
            fecha_inicio = datetime.utcnow()
            fecha_fin = fecha_inicio + timedelta(days=7)
            
            nuevo_descuento = {
                "id_producto": self.producto.id_producto,
                "porcentaje_descuento": 20.0,
                "fecha_inicio": fecha_inicio.isoformat(),
                "fecha_fin": fecha_fin.isoformat()
            }

            endpoint = "/descuentosProd"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.post(
                endpoint,
                data=json.dumps(nuevo_descuento),
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 201)
            self.assertEqual(datos_respuesta['mensaje'], 'Descuento agregado exitosamente')
            self.assertEqual(float(datos_respuesta['descuento']['porcentaje_descuento']), 20.0)
            
        except Exception as e:
            db.session.rollback()
            raise e

    def test_obtener_descuentos(self):
        try:
            # Crear descuento de prueba
            descuento = Descuento(
                id_producto=self.producto.id_producto,
                porcentaje_descuento=15.0,
                fecha_inicio=datetime.utcnow(),
                fecha_fin=datetime.utcnow() + timedelta(days=7)
            )
            db.session.add(descuento)
            db.session.commit()

            # Obtener descuentos
            endpoint = "/descuentosProd"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            resultado = self.client.get(
                endpoint,
                headers=headers
            )

            datos_respuesta = json.loads(resultado.get_data())
            self.assertEqual(resultado.status_code, 200)
            self.assertGreaterEqual(len(datos_respuesta['descuentos']), 1)
            self.assertEqual(float(datos_respuesta['descuentos'][0]['porcentaje_descuento']), 15.0)
            
        except Exception as e:
            db.session.rollback()
            raise e