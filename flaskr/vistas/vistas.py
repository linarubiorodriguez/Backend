from flask_restx import Resource, Namespace, fields
from flask import jsonify, current_app, request
import uuid
from sqlalchemy import inspect
from datetime import datetime
from datetime import timedelta
from ..modelos import db, Animal, AnimalSchema, Marca, MarcaSchema, Descuento, DescuentoSchema, Usuario, UsuarioSchema, Categoria, FormularioPago, FormularioPagoSchema, CategoriaSchema, TipoDoc, TipoDocSchema, Rol, RolSchema, Proveedor, ProveedorSchema, Producto, ProductoSchema, Factura, FacturaSchema, DetalleFactura, DetalleFacturaSchema, Carrito, DetalleCarrito
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
import time
from .. import admin_required, staff_required
from flask import current_app
from sqlalchemy import func
from urllib.parse import unquote
# Cargar variables de entorno desde el archivo .env
import os
from dotenv import load_dotenv
load_dotenv()


# Importar y configurar Cloudinary para la carga de imágenes
import cloudinary
import cloudinary.uploader

# Configuración de Cloudinary usando las credenciales del archivo .env
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    cloudinary_url=os.getenv('CLOUDINARY_URL')
)

marca_schema = MarcaSchema()
marcas_schema = MarcaSchema(many=True)
animal_schema = AnimalSchema()
animales_schema = AnimalSchema(many=True)
descuento_schema = DescuentoSchema()
descuentos_schema = DescuentoSchema(many=True)

usuario_schema = UsuarioSchema()
formupago_schema = FormularioPagoSchema()
rol_schema = RolSchema()
categoria_schema = CategoriaSchema()
tipodoc_schema = TipoDocSchema()
provedoor_schema = ProveedorSchema()
factura_schema = FacturaSchema()
detallefactura_schema = DetalleFacturaSchema()

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class VistaPrivClientes(Resource):
    @jwt_required()  # Requiere un JWT válido para acceder
 # Obtener clientes
    def get(self):
        try:
            clientes = Usuario.query.filter_by(id_rol=2).all()
            clientes_serializados = [
                {
                    "id_usuario": cliente.id_usuario,
                    "nombres": cliente.nombres,
                    "apellidos": cliente.apellidos,
                    "telefono": cliente.telefono,
                    "email": cliente.email,
                    "tipo_doc": cliente.tipo_doc,
                    "num_documento": cliente.num_documento,
                    "direccion": cliente.direccion,
                    "estado": cliente.estado  
                }
                for cliente in clientes
            ]
            return jsonify({"clientes": clientes_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los clientes: {str(e)}"}, 500

    
    @jwt_required()  # Requiere un JWT válido para acceder
    # Agregar cliente
    def post(self):
        try:
            # Validar que los campos necesarios estén presentes
            if not request.json.get("nombres") or not request.json.get("apellidos") or not request.json.get("email"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            # Crear un nuevo cliente
            nuevo_cliente = Usuario(
                nombres=request.json["nombres"],
                apellidos=request.json["apellidos"],
                telefono=request.json.get("telefono"),
                email=request.json["email"],
                tipo_doc=request.json.get("tipo_doc"),
                num_documento=request.json.get("num_documento"),
                direccion=request.json.get("direccion"),
                id_rol=2,
            )

            # Asignar y encriptar la contraseña si está presente
            if request.json.get("contrasena"):
                nuevo_cliente.contrasena = request.json["contrasena"]

            db.session.add(nuevo_cliente)
            db.session.commit()

            return {
                "mensaje": "Cliente agregado exitosamente.",
                "cliente": {
                    "id_usuario": nuevo_cliente.id_usuario,
                    "nombres": nuevo_cliente.nombres,
                    "apellidos": nuevo_cliente.apellidos,
                    "email": nuevo_cliente.email
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar el cliente: {str(e)}"}, 500

   
class VistaPrivCliente(Resource):
    @jwt_required()  # Requiere un JWT válido para acceder
    def get(self, id_usuario):
        try:
            # Buscar al usuario con id_usuario y con rol 2 (cliente)
            cliente = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=2).first()

            if not cliente:
                return {"mensaje": "Cliente no encontrado o no válido."}, 404

            # Serializar los datos del cliente
            cliente_serializado = {
                "id_usuario": cliente.id_usuario,
                "nombres": cliente.nombres,
                "apellidos": cliente.apellidos,
                "telefono": cliente.telefono,
                "email": cliente.email,
                "tipo_doc": cliente.tipo_doc,
                "num_documento": cliente.num_documento,
                "direccion": cliente.direccion
            }

            return jsonify({"cliente": cliente_serializado})

        except Exception as e:
            return {"mensaje": f"Error al obtener el cliente: {str(e)}"}, 500
    

    @jwt_required()  # Requiere un JWT válido para acceder
     # Modificar cliente
    def put(self, id_usuario):
        try:
            # Buscar el cliente por ID
            cliente = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=2).first()
            if not cliente:
                return {"mensaje": "Cliente no encontrado o no válido."}, 404

            # Actualizar los campos del cliente si están presentes en la solicitud
            cliente.nombres = request.json.get("nombres", cliente.nombres)
            cliente.apellidos = request.json.get("apellidos", cliente.apellidos)
            cliente.telefono = request.json.get("telefono", cliente.telefono)
            cliente.email = request.json.get("email", cliente.email)
            cliente.tipo_doc = request.json.get("tipo_doc", cliente.tipo_doc)
            cliente.num_documento = request.json.get("num_documento", cliente.num_documento)
            cliente.direccion = request.json.get("direccion", cliente.direccion)

            # Actualizar la contraseña si está presente
            if request.json.get("contrasena"):
                cliente.contrasena = request.json["contrasena"]

            db.session.commit()

            return {
                "mensaje": "Cliente actualizado exitosamente.",
                "cliente": {
                    "id_usuario": cliente.id_usuario,
                    "nombres": cliente.nombres,
                    "apellidos": cliente.apellidos,
                    "telefono": cliente.telefono,
                    "email": cliente.email,
                    "direccion": cliente.direccion
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el cliente: {str(e)}"}, 500
        
    @admin_required    
    @jwt_required()
    def patch(self, id_usuario):
        try:
                # Buscar el usuario en la base de datos
            cliente = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=2).first()
            if not cliente:
                return {"mensaje": "Cliente no encontrado o no válido."}, 404

            # Obtener el estado enviado en la solicitud
            nuevo_estado = request.json.get("estado")

            if nuevo_estado not in ["Activo", "Inactivo"]:
                return {"mensaje": "Estado inválido, debe ser 'Activo' o 'Inactivo'."}, 400

            # Actualizar el estado en la base de datos
            cliente.estado = nuevo_estado
            db.session.commit()

            return {"mensaje": f"Cliente {nuevo_estado.lower()} correctamente.", "estado": cliente.estado}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al actualizar el estado del cliente: {str(e)}"}, 500
# ----------------------- Gestion de admin para empleados

class VistaAdminEmpleados(Resource): 
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Obtener empleados
    def get(self):
        try:
            # Filtrar los usuarios con id_rol = 3 (empleados)
            empleados = Usuario.query.filter_by(id_rol=3).all()

            # Serializar los datos para retornarlos en formato JSON
            empleados_serializados = [
                {
                    "id_usuario": empleado.id_usuario,
                    "nombres": empleado.nombres,
                    "apellidos": empleado.apellidos,
                    "telefono": empleado.telefono,
                    "email": empleado.email,
                    "tipo_doc": empleado.tipo_doc,
                    "num_documento": empleado.num_documento,
                    "direccion": empleado.direccion
                }
                for empleado in empleados
            ]

            return jsonify({"empleados": empleados_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los empleados: {str(e)}"}, 500
    
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Agregar empleado
    def post(self):
        try:
            # Validar que los campos necesarios estén presentes
            if not request.json.get("nombres") or not request.json.get("apellidos") or not request.json.get("email"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            # Crear un nuevo empleado
            nuevo_empleado = Usuario(
                nombres=request.json["nombres"],
                apellidos=request.json["apellidos"],
                telefono=request.json.get("telefono"),
                email=request.json["email"],
                tipo_doc=request.json.get("tipo_doc"),
                num_documento=request.json.get("num_documento"),
                direccion=request.json.get("direccion"),
                id_rol=3,  # El rol 3 representa a los empleados
            )

            # Asignar y encriptar la contraseña si está presente
            if request.json.get("contrasena"):
                nuevo_empleado.contrasena = request.json["contrasena"]

            db.session.add(nuevo_empleado)
            db.session.commit()

            return {
                "mensaje": "Empleado agregado exitosamente.",
                "empleado": {
                    "id_usuario": nuevo_empleado.id_usuario,
                    "nombres": nuevo_empleado.nombres,
                    "apellidos": nuevo_empleado.apellidos,
                    "email": nuevo_empleado.email
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar el empleado: {str(e)}"}, 500


class VistaAdminEmpleado(Resource): 
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    def get(self, id_usuario):
        try:
            # Buscar al usuario con id_usuario y con rol 3 (empleado)
            empleado = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=3).first()

            if not empleado:
                return {"mensaje": "Empleado no encontrado o no válido."}, 404

            # Serializar los datos del empleado
            empleado_serializado = {
                "id_usuario": empleado.id_usuario,
                "nombres": empleado.nombres,
                "apellidos": empleado.apellidos,
                "telefono": empleado.telefono,
                "email": empleado.email,
                "tipo_doc": empleado.tipo_doc,
                "num_documento": empleado.num_documento,
                "direccion": empleado.direccion
            }

            return jsonify({"empleado": empleado_serializado})

        except Exception as e:
            return {"mensaje": f"Error al obtener el empleado: {str(e)}"}, 500

    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Modificar empleado
    def put(self, id_usuario):
        try:
            # Buscar el empleado por ID
            empleado = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=3).first()
            if not empleado:
                return {"mensaje": "Empleado no encontrado o no válido."}, 404

            # Actualizar los campos del empleado si están presentes en la solicitud
            empleado.nombres = request.json.get("nombres", empleado.nombres)
            empleado.apellidos = request.json.get("apellidos", empleado.apellidos)
            empleado.telefono = request.json.get("telefono", empleado.telefono)
            empleado.email = request.json.get("email", empleado.email)
            empleado.tipo_doc = request.json.get("tipo_doc", empleado.tipo_doc)
            empleado.num_documento = request.json.get("num_documento", empleado.num_documento)
            empleado.direccion = request.json.get("direccion", empleado.direccion)

            # Actualizar la contraseña si está presente
            if request.json.get("contrasena"):
                empleado.contrasena = request.json["contrasena"]

            db.session.commit()

            return {
                "mensaje": "Empleado actualizado exitosamente.",
                "empleado": {
                    "id_usuario": empleado.id_usuario,
                    "nombres": empleado.nombres,
                    "apellidos": empleado.apellidos,
                    "telefono": empleado.telefono,
                    "email": empleado.email,
                    "direccion": empleado.direccion
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el empleado: {str(e)}"}, 500
        
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder

    # Desactivar empleado
    def patch(self, id_usuario):
        try:
        # Buscar el empleado por ID
            empleado = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=3).first()
            if not empleado:
                return {"mensaje": "Empleado no encontrado o no válido."}, 404

        # Cambiar estado a inactivo
            nuevo_estado = request.json.get("estado")

            if nuevo_estado not in ["Activo", "Inactivo"]:
                return {"mensaje": "Estado inválido, debe ser 'Activo' o 'Inactivo'."}, 400

            # Actualizar el estado en la base de datos
            empleado.estado = nuevo_estado
            db.session.commit()

            return {"mensaje": f"empleado {nuevo_estado.lower()} correctamente.", "estado": empleado.estado}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al actualizar el estado del empleado: {str(e)}"}, 500


# ----------------------- Gestion de admin para productos

class VistaPrivProductos(Resource):
    def get(self):
        try:
            productos = Producto.query.all()
            productos_serializados = [
                {
                    "id_producto": producto.id_producto,
                    "nombre": producto.nombre,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "precio_descuento": producto.precio_descuento,  # Campo calculado
                    "tiene_descuento": producto.descuento_activo is not None,  # Nuevo campo
                    "stock": producto.stock,
                    "estado": producto.estado,
                    "id_categoria": producto.id_categoria,
                    "id_marca": producto.id_marca,
                    "id_animal": producto.id_animal,
                    "categoria": producto.categoria.nombre if producto.categoria else None,
                    "marca": producto.marca.nombre if producto.marca else None,
                    "animal": producto.animal.nombre if producto.animal else None,
                    "imagen": producto.imagen
                }
                for producto in productos
            ]
            return jsonify({"productos": productos_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los productos: {str(e)}"}, 500
        
    @admin_required
    @jwt_required()
    def post(self):
        try:
            # Usar request.form para datos y request.files para la imagen
            datos = request.form
            
            nuevo_producto = Producto(
                nombre=datos.get("nombre"),
                descripcion=datos.get("descripcion"),
                precio=float(datos.get("precio")),
                stock=int(datos.get("stock")),
                estado=datos.get("estado", "Disponible"),
                id_categoria=int(datos.get("id_categoria")),
                id_marca=int(datos.get("id_marca")),
                id_animal=int(datos.get("id_animal"))
            )

            # Manejo de imagen
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                if imagen.filename != '':
                    upload_result = cloudinary.uploader.upload(imagen)
                    nuevo_producto.imagen = upload_result.get('secure_url')

            db.session.add(nuevo_producto)
            db.session.commit()

            return {
                "mensaje": "Producto creado exitosamente",
                "producto": producto_schema.dump(nuevo_producto)
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error de integridad en la base de datos."}, 400
        except Exception as e:
            return {"mensaje": f"Error al agregar el producto: {str(e)}"}, 500
        
class VistaPrivProducto(Resource):
    def get(self, id_producto):
        try:
            producto = Producto.query.filter_by(id_producto=id_producto).first()
            if not producto:
                return {"mensaje": "Producto no encontrado o no válido."}, 404

            producto_serializado = {
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "stock": producto.stock,
                "estado": producto.estado,
                "id_categoria": producto.id_categoria,
                "categoria": producto.categoria.nombre if producto.categoria else None,
                "imagen": producto.imagen
            }

            return jsonify({"producto": producto_serializado})
        except Exception as e:
            return {"mensaje": f"Error al obtener el producto: {str(e)}"}, 500

    @jwt_required()
    def put(self, id_producto):
        try:
            producto = Producto.query.filter_by(id_producto=id_producto).first()
            if not producto:
                return {"mensaje": "Producto no encontrado o no válido."}, 404

            datos = request.form
            producto.nombre = datos.get("nombre", producto.nombre)
            producto.descripcion = datos.get("descripcion", producto.descripcion)
            producto.precio = datos.get("precio", producto.precio)
            producto.stock = datos.get("stock", producto.stock)
            producto.estado = datos.get("estado", producto.estado)
            producto.id_categoria = datos.get("id_categoria", producto.id_categoria)

            # Gestionar nueva imagen si se envía
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                producto.imagen = upload_result.get('secure_url')

            db.session.commit()

            return {
                "mensaje": "Producto actualizado exitosamente.",
                "producto": producto_schema.dump(producto)
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el producto: {str(e)}"}, 500
        
    @admin_required
    @jwt_required()
    def patch(self, id_producto):
        try:
            producto = Producto.query.filter_by(id_producto=id_producto).first()
            if not producto:
                return {"mensaje": "Producto no encontrado o no válido."}, 404

            producto.estado = "inactivo"
            db.session.commit()

            return {"mensaje": "Producto desactivado exitosamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al desactivar el producto: {str(e)}"}, 500

# ---------------------------- Vista para facturas
class VistaPrivFacturas(Resource):
    @jwt_required()
    def get(self):
        try:
            # Verificar si la tabla existe (forma compatible con SQLAlchemy moderno)
            inspector = inspect(db.engine)
            if 'factura' not in inspector.get_table_names():
                return {"mensaje": "Tabla de facturas no existe"}, 500

            facturas = Factura.query.all()
            
            if not facturas:
                return {"facturas": []}, 200
            
            facturas_serializadas = []
            for factura in facturas:
                try:
                    factura_data = {
                        "id_factura": factura.id_factura,
                        "fecha_factura": factura.fecha_factura.isoformat() if factura.fecha_factura else None,
                        "total": float(factura.total) if factura.total is not None else 0.0,
                        "iva_total": float(factura.iva_total) if factura.iva_total is not None else 0.0,
                        "estado": factura.estado,
                        "fecha_vencimiento": factura.fecha_vencimiento.isoformat() if factura.fecha_vencimiento else None,
                        "id_cliente": factura.id_cliente
                    }
                    
                    # Agregar datos del cliente si existe la relación
                    if hasattr(factura, 'cliente') and factura.cliente:
                        factura_data["cliente"] = {
                            "id_usuario": factura.cliente.id_usuario,
                            "nombres": factura.cliente.nombres,
                            "apellidos": factura.cliente.apellidos
                        }
                    
                    facturas_serializadas.append(factura_data)
                except Exception as e:
                    current_app.logger.error(f"Error serializando factura {factura.id_factura}: {str(e)}")
                    continue

            return {"facturas": facturas_serializadas}, 200

        except Exception as e:
            current_app.logger.error(f"Error en VistaPrivFacturas: {str(e)}", exc_info=True)
            return {
                "mensaje": "Error interno al obtener las facturas",
                "error": str(e)
            }, 500
        
    # Agregar una nueva factura
    @jwt_required()
    def post(self):
        try:
            data = request.json

            # Validar que los datos requeridos estén presentes
            if not data.get("total") or not data.get("id_cliente"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            # Crear una nueva factura en estado "Pendiente"
            nueva_factura = Factura(
                fecha_factura=datetime.utcnow(),
                total=data["total"],
                iva_total=data.get("iva_total", 0),
                estado="Pendiente",
                fecha_vencimiento=data.get("fecha_vencimiento"),
                id_cliente=data["id_cliente"]
            )

            db.session.add(nueva_factura)
            db.session.commit()

            return {
                "mensaje": "Factura creada exitosamente.",
                "id_factura": nueva_factura.id_factura
            }, 201

        except Exception as e:
            return {"mensaje": f"Error al crear la factura: {str(e)}"}, 500

class VistaPrivFactura(Resource):
    @jwt_required()
    def get(self, id_factura):
        try:
            factura = Factura.query.filter_by(id_factura=id_factura).first()

            if not factura:
                return {"mensaje": "Factura no encontrada o no válida."}, 404

            # Construir respuesta de manera segura
            factura_serializada = {
                "id_factura": factura.id_factura,
                "fecha_factura": factura.fecha_factura.strftime('%Y-%m-%d %H:%M:%S') if factura.fecha_factura else None,
                "total": factura.total,
                "iva_total": factura.iva_total,
                "estado": factura.estado,
                "fecha_vencimiento": factura.fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S') if factura.fecha_vencimiento else None,
                "id_cliente": factura.id_cliente
            }

            # Agregar datos del cliente solo si existe la relación
            if factura.cliente:
                factura_serializada["cliente"] = {
                    "id_usuario": factura.cliente.id_usuario,
                    "nombres": factura.cliente.nombres,
                    "apellidos": factura.cliente.apellidos,
                    "email": factura.cliente.email
                }

            return {"factura": factura_serializada}, 200

        except Exception as e:
            # Registrar el error real en los logs del servidor
            current_app.logger.error(f"Error al obtener factura {id_factura}: {str(e)}")
            return {
                "mensaje": "Error al obtener la factura",
                "error": str(e)  # Solo para desarrollo, quitar en producción
            }, 500
        
    @admin_required       
    @jwt_required()  # Requiere un JWT válido para acceder
    # Modificar factura
    def put(self, id_factura):
        try:
            # Buscar la factura por ID
            factura = Factura.query.filter_by(id_factura=id_factura).first()

            if not factura:
                return {"mensaje": "Factura no encontrada o no válida."}, 404

            # Actualizar los campos de la factura si están presentes en la solicitud
            factura.fecha_factura = request.json.get("fecha_factura", factura.fecha_factura)
            factura.total = request.json.get("total", factura.total)
            factura.iva_total = request.json.get("iva_total", factura.iva_total)
            factura.estado = request.json.get("estado", factura.estado)
            factura.fecha_vencimiento = request.json.get("fecha_vencimiento", factura.fecha_vencimiento)
            factura.id_cliente = request.json.get("id_cliente", factura.id_cliente)

            db.session.commit()

            return {
                "mensaje": "Factura actualizada exitosamente.",
                "factura": {
                    "id_factura": factura.id_factura,
                    "fecha_factura": factura.fecha_factura.strftime('%Y-%m-%d %H:%M:%S'),
                    "total": factura.total,
                    "iva_total": factura.iva_total,
                    "estado": factura.estado,
                    "fecha_vencimiento": factura.fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S'),
                    "id_cliente": factura.id_cliente
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar la factura: {str(e)}"}, 500
    
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Actualizar estado de factura
    def patch(self, id_factura):
        try:
        # Buscar la factura por ID
            factura = Factura.query.filter_by(id_factura=id_factura).first()

            if not factura:
                return {"mensaje": "Factura no encontrada o no válida."}, 404

        # Cambiar estado a "cancelada" o "pagada" según corresponda
            factura.estado = "cancelada"  
            db.session.commit()

            return {"mensaje": "Estado de la factura actualizado exitosamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el estado de la factura: {str(e)}"}, 500

# ----------------------- Gestión formulario de pago

class VistaFormularioPagos(Resource):
    # Detalle del pago
    @jwt_required()
    def get(self, id_factura):
        try:
            pago = FormularioPago.query.filter_by(id_factura=id_factura).first()

            if not pago:
                return {"mensaje": "No hay pagos registrados para esta factura."}, 404

            return {
                "pago": {
                    "id_formulario": pago.id_formulario,
                    "id_factura": pago.id_factura,
                    "titular": pago.titular,
                    "estado_pago": pago.estado_pago,
                    "referencia_pago": pago.referencia_pago,
                    "fecha_pago": pago.fecha_pago.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, 200

        except Exception as e:
            return {"mensaje": f"Error al obtener la información del pago: {str(e)}"}, 500

# Ncesario para el formulario de pago
class VistaProcesarPago(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            
            # Validación exhaustiva
            required_fields = ["id_factura", "tipo_pago"]
            if not all(field in data for field in required_fields):
                return {"mensaje": "Faltan campos obligatorios"}, 400
                
            if data["tipo_pago"] not in ['tarjeta', 'efectivo', 'transferencia']:
                return {"mensaje": "Tipo de pago no válido"}, 400

            factura = Factura.query.get(data["id_factura"])
            if not factura:
                return {"mensaje": "Factura no encontrada"}, 404
                
            if factura.estado != "Pendiente":
                return {"mensaje": "La factura ya fue procesada"}, 400

            # Validaciones específicas para tarjeta
            if data["tipo_pago"] == "tarjeta":
                card_fields = ["titular", "numero_tarjeta", "fecha_expiracion", "codigo_seguridad"]
                if not all(field in data for field in card_fields):
                    return {"mensaje": "Faltan datos de la tarjeta"}, 400
                
                if not data["numero_tarjeta"].isdigit() or len(data["numero_tarjeta"]) != 16:
                    return {"mensaje": "Número de tarjeta no válido"}, 400
                
                try:
                    month, year = map(int, data["fecha_expiracion"].split('/'))
                    current_year = datetime.now().year % 100
                    current_month = datetime.now().month
                    
                    if (year < current_year) or (year == current_year and month < current_month):
                        return {"mensaje": "Tarjeta expirada"}, 400
                except:
                    return {"mensaje": "Fecha de expiración no válida (use formato MM/YY)"}, 400
                
                if not data["codigo_seguridad"].isdigit() or len(data["codigo_seguridad"]) not in [3, 4]:
                    return {"mensaje": "Código de seguridad no válido"}, 400
            
            # Crear registro de pago
            nuevo_pago = FormularioPago(
                id_factura=data["id_factura"],
                tipo_pago=data["tipo_pago"],
                titular=data.get("titular", ""),
                numero_tarjeta=data.get("numero_tarjeta", ""),
                fecha_expiracion=data.get("fecha_expiracion", ""),
                codigo_seguridad=data.get("codigo_seguridad", ""),
                estado_pago="Procesando",
                referencia_pago=f"PAY-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            )
            
            db.session.add(nuevo_pago)
            
            # Simular procesamiento
            if data["tipo_pago"] == "tarjeta":
                time.sleep(2)
                nuevo_pago.estado_pago = "Aprobado"
                nuevo_pago.fecha_pago = datetime.utcnow()
                factura.estado = "Pagada"
                
                # Vaciar carrito y actualizar stock
                carrito = Carrito.query.filter_by(id_usuario=factura.id_cliente).first()
                if carrito:
                    DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito).delete()
                
                for detalle in factura.detalles:
                    producto = Producto.query.get(detalle.id_producto)
                    if producto:
                        producto.stock -= detalle.cantidad
                
                factura.metodo_pago = data["tipo_pago"]
                factura.referencia_pago = nuevo_pago.referencia_pago
        
                if data["tipo_pago"] == "tarjeta":
                    factura.estado = "Pagada"

            else:
                nuevo_pago.estado_pago = "Pendiente"
                factura.estado = "Pendiente"
            
            db.session.commit()
            
            return {
                "mensaje": "Pago procesado exitosamente",
                "pago": {
                    "referencia_pago": nuevo_pago.referencia_pago,
                    "estado_pago": nuevo_pago.estado_pago,
                    "fecha_pago": nuevo_pago.fecha_pago.strftime('%Y-%m-%d %H:%M:%S') if nuevo_pago.fecha_pago else None
                },
                "carrito_vaciado": data["tipo_pago"] == "tarjeta",
                "stock_actualizado": data["tipo_pago"] == "tarjeta"
            }, 201
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error en VistaProcesarPago: {str(e)}", exc_info=True)
            return {
                "mensaje": "Error interno al procesar el pago",
                "error": "Error en el servidor"
            }, 500

class VistaHistorialCompras(Resource):
    @jwt_required()
    def get(self):
        try:
            usuario_id = get_jwt_identity()
            
            # Incluir facturas Pendientes, Pagadas y Completadas
            facturas = Factura.query.filter(
                Factura.id_cliente == usuario_id,
                Factura.estado.in_(["Pendiente", "Pagada", "Completada"])
            ).order_by(Factura.fecha_factura.desc()).all()
            
            if not facturas:
                return {"mensaje": "No hay historial de compras", "compras": []}, 200
            
            historial = []
            for factura in facturas:
                detalles = []
                for detalle in factura.detalles:
                    detalles.append({
                        "producto": detalle.producto.nombre,
                        "cantidad": detalle.cantidad,
                        "precio_unitario": detalle.subtotal / detalle.cantidad,
                        "subtotal": detalle.subtotal
                    })
                
                # Agregar información específica según el estado
                item_historial = {
                    "id_factura": factura.id_factura,
                    "fecha": factura.fecha_factura.isoformat(),
                    "total": factura.total,
                    "metodo_pago": factura.metodo_pago,
                    "estado": factura.estado,
                    "productos": detalles,
                    "acciones_disponibles": self._obtener_acciones(factura)  # Nuevo método
                }
                
                historial.append(item_historial)
            
            return {"compras": historial}, 200
            
        except Exception as e:
            return {"mensaje": f"Error al obtener historial: {str(e)}"}, 500
    
    def _obtener_acciones(self, factura):
        """Determina qué acciones puede realizar el usuario según el estado"""
        if factura.estado == "Pendiente":
            return ["cancelar", "reintentar_pago"]
        elif factura.estado == "Pagada":
            return ["ver_detalle", "descargar_factura"]
        return ["ver_detalle"]

class VistaCancelarPago(Resource):
    @jwt_required()
    def post(self, id_factura):
        try:
            usuario_id = get_jwt_identity()
            factura = Factura.query.filter_by(
                id_factura=id_factura,
                id_cliente=usuario_id,
                estado="Pendiente"
            ).first()
            
            if not factura:
                return {"mensaje": "Factura no encontrada o no cancelable"}, 404
            
            # Eliminar detalles primero
            DetalleFactura.query.filter_by(id_factura=id_factura).delete()
            
            # Eliminar formulario de pago si existe
            FormularioPago.query.filter_by(id_factura=id_factura).delete()
            
            # Finalmente eliminar la factura
            db.session.delete(factura)
            db.session.commit()
            
            return {"mensaje": "Compra cancelada exitosamente"}, 200
            
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al cancelar compra: {str(e)}"}, 500

# ----------------------- Gestión de Proveedores

class VistaAdminProveedores(Resource):
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Obtener proveedores
    def get(self):
        try:
            # Obtener todos los proveedores
            proveedores = Proveedor.query.all()

            # Serializar los datos para retornarlos en formato JSON
            proveedores_serializados = [
                {
                    "id_proveedor": proveedor.id_proveedor,
                    "nombre": proveedor.nombre,
                    "telefono": proveedor.telefono,
                    "correo": proveedor.correo,
                    "estado": proveedor.estado
                }
                for proveedor in proveedores
            ]

            return jsonify({"proveedores": proveedores_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los proveedores: {str(e)}"}, 500

    # Agregar proveedor
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    def post(self):
        try:
            # Validar que los campos necesarios estén presentes
            if not request.json.get("nombre") or not request.json.get("telefono") or not request.json.get("correo"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            # Crear un nuevo proveedor
            nuevo_proveedor = Proveedor(
                nombre=request.json["nombre"],
                telefono=request.json["telefono"],
                correo=request.json["correo"],
                estado=request.json.get("estado", "activo")  # Estado predeterminado "activo"
            )

            db.session.add(nuevo_proveedor)
            db.session.commit()

            return {
                "mensaje": "Proveedor agregado exitosamente.",
                "proveedor": {
                    "id_proveedor": nuevo_proveedor.id_proveedor,
                    "nombre": nuevo_proveedor.nombre,
                    "telefono": nuevo_proveedor.telefono,
                    "correo": nuevo_proveedor.correo,
                    "estado": nuevo_proveedor.estado
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar el proveedor: {str(e)}"}, 500


class VistaAdminProveedor(Resource):
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Obtener proveedor por ID
    def get(self, id_proveedor):
        try:
            # Buscar el proveedor por ID
            proveedor = Proveedor.query.filter_by(id_proveedor=id_proveedor).first()

            if not proveedor:
                return {"mensaje": "Proveedor no encontrado o no válido."}, 404

            proveedor_serializado = {
                "id_proveedor": proveedor.id_proveedor,
                "nombre": proveedor.nombre,
                "telefono": proveedor.telefono,
                "correo": proveedor.correo,
                "estado": proveedor.estado
            }

            return jsonify({"proveedor": proveedor_serializado})
        except Exception as e:
            return {"mensaje": f"Error al obtener el proveedor: {str(e)}"}, 500

    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Modificar proveedor
    def put(self, id_proveedor):
        try:
            # Buscar el proveedor por ID
            proveedor = Proveedor.query.filter_by(id_proveedor=id_proveedor).first()
            if not proveedor:
                return {"mensaje": "Proveedor no encontrado o no válido."}, 404

            # Actualizar los campos del proveedor si están presentes en la solicitud
            proveedor.nombre = request.json.get("nombre", proveedor.nombre)
            proveedor.telefono = request.json.get("telefono", proveedor.telefono)
            proveedor.correo = request.json.get("correo", proveedor.correo)
            proveedor.estado = request.json.get("estado", proveedor.estado)

            db.session.commit()

            return {
                "mensaje": "Proveedor actualizado exitosamente.",
                "proveedor": {
                    "id_proveedor": proveedor.id_proveedor,
                    "nombre": proveedor.nombre,
                    "telefono": proveedor.telefono,
                    "correo": proveedor.correo,
                    "estado": proveedor.estado
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el proveedor: {str(e)}"}, 500
   
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Desactivar proveedor
    def patch(self, id_proveedor):
        try:
            # Buscar el proveedor por ID
            proveedor = Proveedor.query.filter_by(id_proveedor=id_proveedor).first()
            if not proveedor:
                return {"mensaje": "Proveedor no encontrado o no válido."}, 404

            # Cambiar estado a "inactivo"
            proveedor.estado = "inactivo"
            db.session.commit()

            return {"mensaje": "Proveedor desactivado exitosamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al desactivar el proveedor: {str(e)}"}, 500


# -------------------------- Carrito y proceso
class VistaAgregarAlCarrito(Resource):
    @jwt_required()  # Requiere un JWT válido para acceder
    def post(self):
        try:
            id_usuario = request.json.get("id_usuario")
            id_producto = request.json.get("id_producto")
            cantidad = request.json.get("cantidad", 1)

            # Validar que el producto existe y tiene precio
            producto = Producto.query.get(id_producto)
            if not producto or producto.precio is None:
                return {"mensaje": "Producto no disponible"}, 400
            
            # Buscar carrito del usuario, o crearlo si no existe
            carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
            if not carrito:
                carrito = Carrito(id_usuario=id_usuario)
                db.session.add(carrito)
                db.session.commit()

            # Agregar el producto al carrito
            detalle = DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito, id_producto=id_producto).first()
            if detalle:
                detalle.cantidad += cantidad
            else:
                nuevo_detalle = DetalleCarrito(id_carrito=carrito.id_carrito, id_producto=id_producto, cantidad=cantidad)
                db.session.add(nuevo_detalle)

            db.session.commit()
            return {"mensaje": "Producto agregado al carrito exitosamente."}, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar producto al carrito: {str(e)}"}, 500

class VistaCarrito(Resource):
    @jwt_required()  # Requiere un JWT válido para acceder
    def get(self, id_usuario):
        try:
            # Buscar carrito del usuario
            carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
            if not carrito:
                return {"mensaje": "Carrito no encontrado."}, 404

            # Serializar productos en el carrito con validación de precios
            productos_serializados = []
            for detalle in carrito.detalles:
                producto = detalle.producto
                
                # Validar que el producto existe
                if not producto:
                    continue
                    
                # Determinar el precio a usar (precio_descuento si existe, sino precio normal)
                precio = producto.precio_descuento if producto.precio_descuento is not None else producto.precio
                
                # Validar que el precio es válido
                if precio is None:
                    current_app.logger.error(f"Producto {producto.id_producto} no tiene precio")
                    continue
                
                # Calcular subtotal solo si tenemos cantidad y precio válidos
                subtotal = detalle.cantidad * precio if detalle.cantidad and precio else 0
                
                productos_serializados.append({
                    "id_producto": producto.id_producto,
                    "nombre": producto.nombre,
                    "cantidad": detalle.cantidad,
                    "precio": precio,
                    "precio_original": producto.precio,
                    "precio_descuento": producto.precio_descuento,
                    "subtotal": subtotal,
                    "imagen": producto.imagen
                })

            return {
                "id_carrito": carrito.id_carrito,
                "productos": productos_serializados
            }, 200
        except Exception as e:
            current_app.logger.error(f"Error al obtener el carrito: {str(e)}")
            return {"mensaje": f"Error al obtener el carrito: {str(e)}"}, 500
        
class VistaProductoCarrito(Resource):
    @jwt_required()  # Requiere un JWT válido para acceder
    def put(self, id_carrito, id_producto):
        try:
            nueva_cantidad = request.json.get("cantidad")

            if nueva_cantidad is None or nueva_cantidad < 1:
                return {"mensaje": "La cantidad debe ser mayor a 0."}, 400

            detalle = DetalleCarrito.query.filter_by(id_carrito=id_carrito, id_producto=id_producto).first()
            if not detalle:
                return {"mensaje": "Producto no encontrado en el carrito."}, 404

            detalle.cantidad = nueva_cantidad
            db.session.commit()

            return {"mensaje": "Producto modificado exitosamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al modificar producto: {str(e)}"}, 500
        
    @jwt_required()  # Requiere un JWT válido para acceder
    def delete(self, id_carrito, id_producto):
        try:
            detalle = DetalleCarrito.query.filter_by(id_carrito=id_carrito, id_producto=id_producto).first()
            if not detalle:
                return {"mensaje": "Producto no encontrado en el carrito."}, 404

            db.session.delete(detalle)
            db.session.commit()

            return {"mensaje": "Producto eliminado del carrito exitosamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al eliminar producto: {str(e)}"}, 500
        
class VistaProcesarCompra(Resource):
    @jwt_required()
    def post(self, id_usuario):
        try:
            # Buscar carrito del usuario
            carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
            if not carrito or not carrito.detalles:
                return {"mensaje": "El carrito está vacío o no existe."}, 400

            # Verificar stock antes de crear la factura
            for detalle in carrito.detalles:
                producto = detalle.producto
                if not producto or producto.stock < detalle.cantidad:
                    return {
                        "mensaje": f"No hay suficiente stock para {producto.nombre if producto else 'producto desconocido'}",
                        "producto": producto.nombre if producto else None,
                        "stock_disponible": producto.stock if producto else 0,
                        "solicitado": detalle.cantidad
                    }, 400

            # Calcular totales
            subtotal = sum(
                detalle.cantidad * (detalle.producto.precio_descuento if detalle.producto.precio_descuento is not None else detalle.producto.precio)
                for detalle in carrito.detalles
            )
            iva = subtotal * 0.16
            total = subtotal + iva

            # Crear factura con fecha de vencimiento (7 días después)
            fecha_actual = datetime.utcnow()
            fecha_vencimiento = fecha_actual + timedelta(days=7)
            
            nueva_factura = Factura(
                fecha_factura=fecha_actual,
                total=total,
                iva_total=iva,
                estado="Pendiente",
                fecha_vencimiento=fecha_vencimiento,
                id_cliente=id_usuario
            )
            
            db.session.add(nueva_factura)
            db.session.flush()

            # Crear detalles de factura
            for detalle in carrito.detalles:
                precio = detalle.producto.precio_descuento if detalle.producto.precio_descuento is not None else detalle.producto.precio
                nuevo_detalle = DetalleFactura(
                    id_factura=nueva_factura.id_factura,
                    id_producto=detalle.producto.id_producto,
                    cantidad=detalle.cantidad,
                    subtotal=detalle.cantidad * precio
                )
                db.session.add(nuevo_detalle)

            db.session.commit()

            return {
                "mensaje": "Factura creada exitosamente. Proceda al pago.",
                "id_factura": nueva_factura.id_factura,
                "total": total,
                "fecha_vencimiento": fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S'),
                "productos": [
                    {
                        "id_producto": detalle.producto.id_producto,
                        "nombre": detalle.producto.nombre,
                        "cantidad": detalle.cantidad,
                        "precio": detalle.producto.precio,
                        "precio_descuento": detalle.producto.precio_descuento
                    }
                    for detalle in carrito.detalles
                ]
            }, 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al procesar compra: {str(e)}")
            return {"mensaje": f"Error al procesar la compra: {str(e)}"}, 500
        
class VistaConfirmarPago(Resource):
    @jwt_required()
    def post(self, id_factura):
        try:
            # 1. Verificar y obtener la factura
            factura = Factura.query.get(id_factura)
            if not factura:
                return {"mensaje": "Factura no encontrada"}, 404
                
            if factura.estado == "Pagada":
                return {"mensaje": "La factura ya fue pagada anteriormente"}, 400

            # 2. Obtener el carrito del usuario
            carrito = Carrito.query.filter_by(id_usuario=factura.id_cliente).first()

            # 3. Procesar cada producto (reducir stock)
            productos_actualizados = []
            for detalle_factura in factura.detalles:
                producto = Producto.query.get(detalle_factura.id_producto)
                if producto:
                    # Verificar stock nuevamente
                    if producto.stock < detalle_factura.cantidad:
                        return {
                            "mensaje": f"Stock insuficiente para {producto.nombre}",
                            "producto": producto.nombre,
                            "stock_actual": producto.stock,
                            "solicitado": detalle_factura.cantidad
                        }, 400
                    
                    # Reducir stock
                    producto.stock -= detalle_factura.cantidad
                    productos_actualizados.append({
                        "id_producto": producto.id_producto,
                        "nombre": producto.nombre,
                        "nuevo_stock": producto.stock
                    })

            # 4. Vaciar el carrito si existe
            if carrito:
                # Eliminar todos los detalles del carrito
                DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito).delete()
                db.session.commit()

            # 5. Actualizar estado de la factura
            factura.estado = "Pagada"
            factura.fecha_pago = datetime.utcnow()

            # 6. Crear registro de pago
            nuevo_pago = FormularioPago(
                id_factura=factura.id_factura,
                estado_pago="Aprobado",
                referencia_pago=f"PAY-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                fecha_pago=datetime.utcnow()
            )
            db.session.add(nuevo_pago)

            db.session.commit()

            return {
                "mensaje": "Pago confirmado exitosamente. Carrito vaciado y stock actualizado.",
                "factura": {
                    "id_factura": factura.id_factura,
                    "referencia_pago": nuevo_pago.referencia_pago,
                    "estado": factura.estado,
                    "fecha_pago": factura.fecha_pago.strftime('%Y-%m-%d %H:%M:%S'),
                    "total": factura.total
                },
                "productos_actualizados": productos_actualizados,
                "carrito_vaciado": True if carrito else False
            }, 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al confirmar pago: {str(e)}")
            return {"mensaje": f"Error al confirmar el pago: {str(e)}"}, 500
# ---------------- Parte de LOGIN
class VistaLogIn(Resource):
    def post(self):
        u_email = request.json["email"]
        u_contrasena = request.json["contrasena"]
        
        usuario = Usuario.query.filter_by(email=u_email).first()  
        print(usuario)
        if usuario and usuario.verificar_contrasena(u_contrasena):
            usuario.ultimo_login = datetime.utcnow()  # Actualizar último login
            db.session.commit()
            user_id = str(usuario.id_usuario) 
            
            token_de_acceso = create_access_token(
                identity=user_id, 
                additional_claims={
                    'rol': usuario.id_rol,
                    'email': usuario.email
                }
            )
            return {
                'usuario': user_id,  
                'mensaje': 'Inicio de sesión exitoso',
                'token_de_acceso': token_de_acceso,
            }, 200
        else:
            return {'mensaje': 'Email o contraseña incorrectos'}, 401
        
class VistaSignIn(Resource):
    def post(self):
        try:

            if Usuario.query.filter_by(email=request.json.get("email")).first():
                return {'mensaje': 'El email ya está registrado'}, 400

            if Usuario.query.filter_by(num_documento=request.json.get("num_documento")).first():
                return {'mensaje': 'El número de documento ya está registrado'}, 400

            nuevo_usuario = Usuario(
                nombres=request.json["nombres"],
                apellidos=request.json.get("apellidos"),
                telefono=request.json.get("telefono"),
                email=request.json.get("email"),
                tipo_doc=request.json.get("tipo_doc"),
                num_documento=request.json.get("num_documento"),
                direccion=request.json.get("direccion"),
                contrasena=request.json.get("contrasena")
            )
            nuevo_usuario.id_rol = 2
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            return {'mensaje': 'Usuario creado exitosamente'}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'mensaje': f'Error al crear usuario: {str(e)}'}, 500



class VistaPrivTipoDoc(Resource):
    # Obtener todos los tipos de documento
    def get(self):
        try:
            tipo_docs = TipoDoc.query.all()
            tipo_docs_serializados = [
                {
                    "id_TipoDocumento": tipo_doc.id_TipoDocumento,
                    "Nombre": tipo_doc.Nombre,
                    "Descripcion": tipo_doc.Descripcion
                }
                for tipo_doc in tipo_docs
            ]
            return jsonify({"tipo_docs": tipo_docs_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los tipos de documento: {str(e)}"}, 500

    @jwt_required()  # Requiere un JWT válido para acceder
    # Agregar un nuevo tipo de documento
    def post(self):
        try:
            if not request.json.get("Nombre"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            nuevo_tipo_doc = TipoDoc(
                Nombre=request.json["Nombre"],
                Descripcion=request.json.get("Descripcion")
            )

            db.session.add(nuevo_tipo_doc)
            db.session.commit()

            return {
                "mensaje": "Tipo de documento agregado exitosamente.",
                "tipo_doc": {
                    "id_TipoDocumento": nuevo_tipo_doc.id_TipoDocumento,
                    "Nombre": nuevo_tipo_doc.Nombre
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar el tipo de documento: {str(e)}"}, 500


class VistaPrivTipoDocs(Resource):
    @jwt_required()  # Requiere un JWT válido para acceder
    # Modificar tipo de documento
    def put(self, id_TipoDocumento):
        try:
            tipo_doc = TipoDoc.query.filter_by(id_TipoDocumento=id_TipoDocumento).first()
            if not tipo_doc:
                return {"mensaje": "Tipo de documento no encontrado."}, 404

            tipo_doc.Nombre = request.json.get("Nombre", tipo_doc.Nombre)
            tipo_doc.Descripcion = request.json.get("Descripcion", tipo_doc.Descripcion)

            db.session.commit()

            return {
                "mensaje": "Tipo de documento actualizado exitosamente.",
                "tipo_doc": {
                    "id_TipoDocumento": tipo_doc.id_TipoDocumento,
                    "Nombre": tipo_doc.Nombre,
                    "Descripcion": tipo_doc.Descripcion
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el tipo de documento: {str(e)}"}, 500


class VistaPrivRol(Resource):

    @jwt_required()  # Requiere un JWT válido para acceder
    # Obtener todos los roles
    def get(self):
        try:
            roles = Rol.query.all()
            roles_serializados = [
                {
                    "id_Rol": rol.id_Rol,
                    "Nombre": rol.Nombre,
                    "Descripcion": rol.Descripcion
                }
                for rol in roles
            ]
            return jsonify({"roles": roles_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los roles: {str(e)}"}, 500
    
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Agregar un nuevo rol
    def post(self):
        try:
            if not request.json.get("Nombre"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            nuevo_rol = Rol(
                Nombre=request.json["Nombre"],
                Descripcion=request.json.get("Descripcion")
            )

            db.session.add(nuevo_rol)
            db.session.commit()

            return {
                "mensaje": "Rol agregado exitosamente.",
                "rol": {
                    "id_Rol": nuevo_rol.id_Rol,
                    "Nombre": nuevo_rol.Nombre
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar el rol: {str(e)}"}, 500

class VistaPrivRoles(Resource):
    @admin_required
    @jwt_required()  # Requiere un JWT válido para acceder
    # Modificar rol
    def put(self, id_Rol):
        try:
            rol = Rol.query.filter_by(id_Rol=id_Rol).first()
            if not rol:
                return {"mensaje": "Rol no encontrado."}, 404

            rol.Nombre = request.json.get("Nombre", rol.Nombre)
            rol.Descripcion = request.json.get("Descripcion", rol.Descripcion)

            db.session.commit()

            return {
                "mensaje": "Rol actualizado exitosamente.",
                "rol": {
                    "id_Rol": rol.id_Rol,
                    "Nombre": rol.Nombre,
                    "Descripcion": rol.Descripcion
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el rol: {str(e)}"}, 500




class VistaPrivCategoria(Resource):
    def get(self):
        try:
            categorias = Categoria.query.all()
            categorias_serializadas = [
                {
                    "id_categoria": categoria.id_categoria,
                    "nombre": categoria.nombre,
                    "descripcion": categoria.descripcion,
                    "imagen": categoria.imagen
                }
                for categoria in categorias
            ]
            return jsonify({"categorias": categorias_serializadas})
        except Exception as e:
            return {"mensaje": f"Error al obtener las categorías: {str(e)}"}, 500
        
    @admin_required
    @jwt_required()
    def post(self):
        """Crea una nueva categoría con o sin imagen."""
        try:
            datos = request.form
            if not datos.get("nombre"):
                return {"mensaje": "El nombre es obligatorio."}, 400

            imagen_url = None  # Inicializar la variable de imagen

            # Si se proporciona una imagen, subirla a Cloudinary
            if "imagen" in request.files and request.files["imagen"].filename:
                imagen = request.files["imagen"]
                upload_result = cloudinary.uploader.upload(imagen)
                imagen_url = upload_result.get("secure_url")

            nueva_categoria = Categoria(
                nombre=datos["nombre"],
                descripcion=datos.get("descripcion"),
                imagen=imagen_url
            )

            db.session.add(nueva_categoria)
            db.session.commit()

            return {
                "mensaje": "Categoría agregada exitosamente.",
                "categoria": {
                    "id_categoria": nueva_categoria.id_categoria,
                    "nombre": nueva_categoria.nombre,
                    "descripcion": nueva_categoria.descripcion,
                    "imagen": nueva_categoria.imagen
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar la categoría: {str(e)}"}, 500


class VistaPrivCategorias(Resource):
    def get(self, id_categoria):
        try:
            categoria = Categoria.query.get(id_categoria)
            if not categoria:
                return {"mensaje": "Categoría no encontrada"}, 404
            return jsonify({
                "categoria": {
                    "id_categoria": categoria.id_categoria,
                    "nombre": categoria.nombre,
                    "descripcion": categoria.descripcion,
                    "imagen": categoria.imagen
                }
            })
        except Exception as e:
            return {"mensaje": f"Error al obtener categoría: {str(e)}"}, 500
        
    @admin_required
    @jwt_required()
    def put(self, id_categoria):
        """Actualiza una categoría existente, incluyendo la imagen si se proporciona."""
        try:
            categoria = Categoria.query.filter_by(id_categoria=id_categoria).first()
            if not categoria:
                return {"mensaje": "Categoría no encontrada."}, 404

            datos = request.form
            categoria.nombre = datos.get("nombre", categoria.nombre)
            categoria.descripcion = datos.get("descripcion", categoria.descripcion)

            # Manejo de imágenes: Si hay una nueva, la subimos a Cloudinary
            if "imagen" in request.files and request.files["imagen"].filename:
                imagen = request.files["imagen"]
                upload_result = cloudinary.uploader.upload(imagen)
                categoria.imagen = upload_result.get("secure_url")

            # Si se proporciona una URL de imagen en el formulario, usarla
            elif "imagen_url" in datos and datos["imagen_url"].strip():
                categoria.imagen = datos["imagen_url"]

            db.session.commit()

            return {
                "mensaje": "Categoría actualizada exitosamente.",
                "categoria": {
                    "id_categoria": categoria.id_categoria,
                    "nombre": categoria.nombre,
                    "descripcion": categoria.descripcion,
                    "imagen": categoria.imagen
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar la categoría: {str(e)}"}, 500
        # ----------------------- Gestion de admin para marcas
class VistaMarcas(Resource):
    # Obtener todas las marcas
    def get(self):
        try:
            marcas = Marca.query.all()
            marcas_serializadas = [
                {
                    "id_marca": marca.id_marca,
                    "nombre": marca.nombre,
                    "estado": marca.estado,
                    "id_proveedor": marca.id_proveedor,
                    "imagen": marca.imagen  # Nuevo campo
                }
                for marca in marcas
            ]
            return jsonify({"marcas": marcas_serializadas})
        except Exception as e:
            return {"mensaje": f"Error al obtener las marcas: {str(e)}"}, 500

    # Agregar una nueva marca
    @admin_required
    @jwt_required()
    def post(self):
        try:
            datos = request.form
            if not datos.get("nombre") or not datos.get("id_proveedor"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            imagen_url = None  # Inicializar la variable de imagen

            # Si se proporciona una imagen, subirla a Cloudinary
            if "imagen" in request.files and request.files["imagen"].filename:
                imagen = request.files["imagen"]
                upload_result = cloudinary.uploader.upload(imagen)
                imagen_url = upload_result.get("secure_url")

            nueva_marca = Marca(
                nombre=datos["nombre"],
                estado=datos.get("estado", "Activo"),
                id_proveedor=datos["id_proveedor"],
                imagen=imagen_url  # Nuevo campo
            )

            db.session.add(nueva_marca)
            db.session.commit()

            return {
                "mensaje": "Marca agregada exitosamente.",
                "marca": {
                    "id_marca": nueva_marca.id_marca,
                    "nombre": nueva_marca.nombre,
                    "estado": nueva_marca.estado,
                    "id_proveedor": nueva_marca.id_proveedor,
                    "imagen": nueva_marca.imagen  # Nuevo campo
                }
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error: La marca ya existe o el proveedor no es válido."}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al agregar la marca: {str(e)}"}, 500


class VistaMarca(Resource):
    # Obtener marca por ID
    def get(self, id_marca):
        try:
            marca = Marca.query.get(id_marca)
            if not marca:
                return {"mensaje": "Marca no encontrada."}, 404

            marca_serializada = {
                "id_marca": marca.id_marca,
                "nombre": marca.nombre,
                "estado": marca.estado,
                "id_proveedor": marca.id_proveedor,
                "imagen": marca.imagen  # Nuevo campo
            }

            return jsonify({"marca": marca_serializada})
        except Exception as e:
            return {"mensaje": f"Error al obtener la marca: {str(e)}"}, 500

    # Actualizar marca
    @admin_required
    @jwt_required()
    def put(self, id_marca):
        try:
            marca = Marca.query.get(id_marca)
            if not marca:
                return {"mensaje": "Marca no encontrada."}, 404

            datos = request.form
            marca.nombre = datos.get("nombre", marca.nombre)
            marca.id_proveedor = datos.get("id_proveedor", marca.id_proveedor)
            marca.estado = datos.get("estado", marca.estado)

            # Manejo de imágenes: Si hay una nueva, la subimos a Cloudinary
            if "imagen" in request.files and request.files["imagen"].filename:
                imagen = request.files["imagen"]
                upload_result = cloudinary.uploader.upload(imagen)
                marca.imagen = upload_result.get("secure_url")
            # Si se proporciona una URL de imagen en el formulario, usarla
            elif "imagen_url" in datos and datos["imagen_url"].strip():
                marca.imagen = datos["imagen_url"]

            db.session.commit()

            return {
                "mensaje": "Marca actualizada exitosamente.",
                "marca": {
                    "id_marca": marca.id_marca,
                    "nombre": marca.nombre,
                    "estado": marca.estado,
                    "id_proveedor": marca.id_proveedor,
                    "imagen": marca.imagen  
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar la marca: {str(e)}"}, 500
    
    @admin_required
    @jwt_required()
    def patch(self, id_marca):
        try:
            marca = Marca.query.get(id_marca)
            if not marca:
                return {"mensaje": "Marca no encontrada."}, 404

            nuevo_estado = request.json.get("estado")
            if nuevo_estado not in ["Activo", "Inactivo"]:
                return {"mensaje": "Estado inválido, debe ser 'Activo' o 'Inactivo'."}, 400

            marca.estado = nuevo_estado
            db.session.commit()

            return {"mensaje": f"Marca {nuevo_estado.lower()} correctamente.", "estado": marca.estado}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al actualizar el estado de la marca: {str(e)}"}, 500

# ----------------------- Gestion de admin para descuentos
class VistaDescuentos(Resource):
    def get(self):
        try:
            descuentos = Descuento.query.options(db.joinedload(Descuento.producto)).all()
            return jsonify({
                "descuentos": [{
                    "id_descuento": d.id_descuento,
                    "porcentaje_descuento": d.porcentaje_descuento,
                    "fecha_inicio": d.fecha_inicio.isoformat() if d.fecha_inicio else None,
                    "fecha_fin": d.fecha_fin.isoformat() if d.fecha_fin else None,
                    "id_producto": d.id_producto,
                    "producto": {
                        "id_producto": d.producto.id_producto,
                        "nombre": d.producto.nombre,
                        "imagen": d.producto.imagen,
                        "precio": d.producto.precio,
                        "id_categoria": d.producto.id_categoria,
                        "id_marca": d.producto.id_marca
                    } if d.producto else None  # Manejar caso cuando producto es None
                } for d in descuentos]
            })
        except Exception as e:
            return {"mensaje": f"Error al obtener los descuentos: {str(e)}"}, 500    
    
    @admin_required        
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"mensaje": "No se proporcionaron datos"}, 400
                
            # Validaciones obligatorias
            if not data.get("id_producto"):
                return {"mensaje": "El id_producto es obligatorio"}, 400
            if not data.get("porcentaje_descuento"):  # Cambiado de 'porcentaje' a 'porcentaje_descuento'
                return {"mensaje": "El porcentaje es obligatorio"}, 400

            # Validar que el producto existe
            producto = Producto.query.get(data["id_producto"])
            if not producto:
                return {"mensaje": "El producto especificado no existe"}, 400

            nuevo_descuento = Descuento(
                id_producto=data["id_producto"],
                porcentaje_descuento=data["porcentaje_descuento"],  # Cambiado para coincidir con el modelo
                fecha_inicio=data.get("fecha_inicio"),
                fecha_fin=data.get("fecha_fin")
            )

            db.session.add(nuevo_descuento)
            db.session.commit()

            return {
                "mensaje": "Descuento agregado exitosamente",
                "descuento": descuento_schema.dump(nuevo_descuento)
            }, 201
            
        except IntegrityError as e:
            db.session.rollback()
            return {"mensaje": f"Error de integridad: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error inesperado al agregar descuento: {str(e)}"}, 500
        
class VistaDescuento(Resource):
    def get(self, id_descuento):
        try:
            descuento = Descuento.query.get(id_descuento)
            if not descuento:
                return {"mensaje": "Descuento no encontrado."}, 404
            return jsonify({"descuento": descuento_schema.dump(descuento)})
        except Exception as e:
            return {"mensaje": f"Error al obtener el descuento: {str(e)}"}, 500
    
    @admin_required
    @jwt_required()
    def put(self, id_descuento):
        try:
            descuento = Descuento.query.get(id_descuento)
            if not descuento:
                return {"mensaje": "Descuento no encontrado."}, 404

            data = request.json
            
            # Validar que el producto existe si se está cambiando
            if 'id_producto' in data:
                producto = Producto.query.get(data['id_producto'])
                if not producto:
                    return {"mensaje": "El producto especificado no existe"}, 400
            
            # Actualizar todos los campos incluyendo id_producto
            descuento.id_producto = data.get("id_producto", descuento.id_producto)
            descuento.porcentaje_descuento = data.get("porcentaje_descuento", descuento.porcentaje_descuento)
            descuento.fecha_inicio = data.get("fecha_inicio", descuento.fecha_inicio)
            descuento.fecha_fin = data.get("fecha_fin", descuento.fecha_fin)

            db.session.commit()

            return {
                "mensaje": "Descuento actualizado exitosamente.",
                "descuento": descuento_schema.dump(descuento)
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al actualizar el descuento: {str(e)}"}, 500  
         
    @admin_required        
    @jwt_required()
    def delete(self, id_descuento):
        try:
            descuento = Descuento.query.get(id_descuento)
            if not descuento:
                return {"mensaje": "Descuento no encontrado."}, 404

            db.session.delete(descuento)
            db.session.commit()

            return {"mensaje": "Descuento eliminado exitosamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al eliminar el descuento: {str(e)}"}, 500
        
class VistaAnimales(Resource):
    def get(self):
        try:
            animales = Animal.query.all()
            animales_serializados = [
                {
                    "id_animal": animal.id_animal,
                    "nombre": animal.nombre,
                    "imagen": animal.imagen,
                    "estado": animal.estado  # Agregamos el estado a la respuesta
                }
                for animal in animales
            ]
            return jsonify({"animales": animales_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los animales: {str(e)}"}, 500
    
    @admin_required
    @jwt_required()
    def post(self):
        try:
            datos = request.form
            if not datos.get("nombre"):
                return {"mensaje": "El nombre es obligatorio."}, 400

            imagen_url = None
            if 'imagen' in request.files and request.files['imagen'].filename:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                imagen_url = upload_result.get('secure_url')

            nuevo_animal = Animal(
                nombre=datos["nombre"],
                imagen=imagen_url,
                estado=datos.get("estado", "Activo")  # Estado por defecto "Activo"
            )

            db.session.add(nuevo_animal)
            db.session.commit()

            return {
                "mensaje": "Animal agregado exitosamente.",
                "animal": {
                    "id_animal": nuevo_animal.id_animal,
                    "nombre": nuevo_animal.nombre,
                    "imagen": nuevo_animal.imagen,
                    "estado": nuevo_animal.estado
                }
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error: El nombre del animal ya existe."}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al agregar el animal: {str(e)}"}, 500


class VistaAnimal(Resource):
    def get(self, id_animal):
        try:
            animal = Animal.query.get(id_animal)
            if not animal:
                return {"mensaje": "Animal no encontrado."}, 404

            return jsonify({
                "animal": {
                    "id_animal": animal.id_animal,
                    "nombre": animal.nombre,
                    "imagen": animal.imagen,
                    "estado": animal.estado
                }
            })
        except Exception as e:
            return {"mensaje": f"Error al obtener el animal: {str(e)}"}, 500

    @admin_required
    @jwt_required()
    def put(self, id_animal):
        try:
            animal = Animal.query.get(id_animal)
            if not animal:
                return {"mensaje": "Animal no encontrado."}, 404

            datos = request.form
            if 'nombre' in datos:
                animal.nombre = datos['nombre']

            # Gestionar nueva imagen si se envía
            if 'imagen' in request.files and request.files['imagen'].filename:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                animal.imagen = upload_result.get('secure_url')
            # Si se proporciona una URL de imagen en el formulario, usarla
            elif 'imagen_url' in datos and datos['imagen_url'].strip():
                animal.imagen = datos['imagen_url']

            db.session.commit()

            return {
                "mensaje": "Animal actualizado exitosamente.",
                "animal": {
                    "id_animal": animal.id_animal,
                    "nombre": animal.nombre,
                    "imagen": animal.imagen,
                    "estado": animal.estado
                }
            }, 200
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error: El nombre del animal ya existe."}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al actualizar el animal: {str(e)}"}, 500
        
    @admin_required
    @jwt_required()
    def patch(self, id_animal):
        try:
            animal = Animal.query.get(id_animal)
            if not animal:
                return {"mensaje": "Animal no encontrado."}, 404

            nuevo_estado = request.json.get("estado")
            if nuevo_estado not in ["Activo", "Inactivo"]:
                return {"mensaje": "Estado inválido, debe ser 'Activo' o 'Inactivo'."}, 400

            animal.estado = nuevo_estado
            db.session.commit()

            return {
                "mensaje": f"Estado del animal actualizado a '{nuevo_estado}' correctamente.",
                "animal": {
                    "id_animal": animal.id_animal,
                    "nombre": animal.nombre,
                    "estado": animal.estado
                }
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al actualizar el estado del animal: {str(e)}"}, 500


# ----------------------------- Sistema de reportes

class VistaReporteVentas(Resource):
    @admin_required
    def get(self):
        try:
            # Parámetros de fecha (opcionales)
            start_date = request.args.get('start', default=(datetime.now() - timedelta(days=30)).isoformat())
            end_date = request.args.get('end', default=datetime.now().isoformat())
            
            ventas = db.session.query(
                func.date(Factura.fecha_factura).label('fecha'),
                func.sum(Factura.total).label('total')
            ).filter(
                Factura.fecha_factura.between(start_date, end_date),
                Factura.estado == 'Pagada'
            ).group_by(func.date(Factura.fecha_factura)).all()

            return jsonify([{
                'fecha': v.fecha.isoformat() if v.fecha else None,
                'total': float(v.total) if v.total else 0
            } for v in ventas])
            
        except Exception as e:
            return {'mensaje': f'Error generando reporte: {str(e)}'}, 500

class VistaReporteProductos(Resource):
    @admin_required
    def get(self):
        try:
            # Top 10 productos más vendidos
            productos_top = db.session.query(
                Producto.nombre,
                func.sum(DetalleFactura.cantidad).label('vendidos'),
                func.sum(DetalleFactura.subtotal).label('ingresos')
            ).join(DetalleFactura).group_by(Producto.id_producto
            ).order_by(func.sum(DetalleFactura.subtotal).desc()).limit(10).all()

            # Productos con stock bajo
            stock_bajo = Producto.query.filter(Producto.stock < 10).all()

            return jsonify({
                'top_productos': [{
                    'nombre': p.nombre,
                    'vendidos': p.vendidos,
                    'ingresos': float(p.ingresos)
                } for p in productos_top],
                'stock_bajo': [{
                    'id_producto': p.id_producto,
                    'nombre': p.nombre,
                    'stock': p.stock,
                    'precio': float(p.precio)
                } for p in stock_bajo]
            })
        except Exception as e:
            return {'mensaje': f'Error generando reporte: {str(e)}'}, 500

class VistaReporteUsuarios(Resource):
    @admin_required
    def get(self):
        try:
            usuarios_activos = Usuario.query.filter_by(estado='Activo').count()
            nuevos_clientes = Usuario.query.filter(
                Usuario.id_rol == 2,  # Clientes
                Usuario.ultimo_login >= (datetime.now() - timedelta(days=30))
            ).count()

            return jsonify({
                'usuarios_activos': usuarios_activos,
                'nuevos_clientes': nuevos_clientes
            })
        except Exception as e:
            return {'mensaje': f'Error generando reporte: {str(e)}'}, 500

class VistaOtrosAnimales(Resource):
    def get(self):
        try:
            # Obtener IDs de perros y gatos
            perro = Animal.query.filter(
                func.lower(Animal.nombre) == func.lower('perro')
            ).first()
            gato = Animal.query.filter(
                func.lower(Animal.nombre) == func.lower('gato')
            ).first()
            
            if not perro or not gato:
                return {"mensaje": "No se encontraron los animales base para filtrar"}, 404
            
            # Filtrar productos excluyendo perros y gatos
            productos = Producto.query.filter(
                Producto.id_animal.notin_([perro.id_animal, gato.id_animal])
            ).all()
            
            return [p.to_dict() for p in productos], 200
            
        except Exception as e:
            current_app.logger.error(f"Error en VistaOtrosAnimales: {str(e)}")
            return {"mensaje": "Error interno del servidor"}, 500


class VistaProductosPorCategoria(Resource):
    def get(self, nombre_categoria):
        try:
            from urllib.parse import unquote
            from sqlalchemy import func, or_
            
            # Decodificar y limpiar el nombre
            nombre = unquote(nombre_categoria).strip().lower()
            
            # Mapeo flexible de nombres
            mapeo_animales = {
                'gatos': 'gato',
                'perros': 'perro'
            }
            
            # Dividir y validar formato
            if ' para ' not in nombre:
                return {"mensaje": "Formato debe ser 'Tipo para Animal'"}, 400
                
            tipo_producto, animal_nombre = nombre.split(' para ', 1)
            tipo_producto = tipo_producto.strip()
            animal_nombre = animal_nombre.strip()
            
            # Normalizar nombre de animal
            animal_nombre = mapeo_animales.get(animal_nombre, animal_nombre)
            
            # Buscar animal (insensible a mayúsculas y singular/plural)
            animal = Animal.query.filter(
                or_(
                    func.lower(Animal.nombre) == animal_nombre,
                    func.lower(Animal.nombre) == animal_nombre + 's',
                    func.lower(Animal.nombre) == animal_nombre[:-1]  # Quita 's' final
                )
            ).first()
            
            if not animal:
                return {"mensaje": f"Animal '{animal_nombre}' no encontrado"}, 404
            
            # Buscar categoría (insensible a mayúsculas)
            categoria = Categoria.query.filter(
                func.lower(Categoria.nombre) == tipo_producto
            ).first()
            
            if not categoria:
                return {"mensaje": f"Categoría '{tipo_producto}' no encontrada"}, 404
            
            # Buscar productos
            productos = Producto.query.filter(
                Producto.id_categoria == categoria.id_categoria,
                Producto.id_animal == animal.id_animal
            ).all()
            
            return [{
                "id_producto": p.id_producto,
                "nombre": p.nombre,
                "precio": float(p.precio),
                "imagen": p.imagen,
                "categoria": categoria.nombre,
                "animal": animal.nombre,
                "marca": p.marca.nombre if p.marca else None
            } for p in productos], 200
            
        except Exception as e:
            return {"mensaje": "Error interno", "error": str(e)}, 500
        
class VistaDebug(Resource):
    def get(self):
        try:
            # Verificar animales con diferentes variaciones
            animales_variaciones = ['gato', 'gatos', 'perro', 'perros']
            animales_db = Animal.query.filter(
                func.lower(Animal.nombre).in_([v.lower() for v in animales_variaciones])
            ).all()
            
            # Verificar categorías
            categorias_db = Categoria.query.filter(
                func.lower(Categoria.nombre) == 'camas'
            ).all()
            
            return {
                "animales_encontrados": [a.nombre for a in animales_db],
                "categoria_camas_encontrada": len(categorias_db) > 0,
                "total_productos": Producto.query.count()
            }, 200
            
        except Exception as e:
            return {"error": str(e)}, 500