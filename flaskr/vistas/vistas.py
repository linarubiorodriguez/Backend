from flask_restful import Resource
from flask import jsonify, current_app, request
import uuid
from datetime import datetime
from ..modelos import db, Animal, AnimalSchema, Marca, MarcaSchema, Descuento, DescuentoSchema, Usuario, UsuarioSchema, Categoria, FormularioPago, FormularioPagoSchema, CategoriaSchema, TipoDoc, TipoDocSchema, Rol, RolSchema, Proveedor, ProveedorSchema, Producto, ProductoSchema, Factura, FacturaSchema, DetalleFactura, DetalleFacturaSchema, Carrito, DetalleCarrito
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

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
                    "estado": cliente.estado  # <--- Asegurar que el estado se retorne
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
# ----------------------- Gestion de admin para empleados


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
                    "stock": producto.stock,
                    "estado": producto.estado,
                    "id_categoria": producto.id_categoria,
                    "categoria": producto.categoria.nombre if producto.categoria else None,
                    "imagen": producto.imagen
                }
                for producto in productos
            ]
            return jsonify({"productos": productos_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los productos: {str(e)}"}, 500

    @jwt_required()
    def post(self):
        try:
            datos = request.form
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                imagen_url = upload_result.get('secure_url')
            else:
                imagen_url = None

            nuevo_producto = Producto(
                nombre=datos["nombre"],
                descripcion=datos.get("descripcion"),
                precio=datos["precio"],
                stock=datos["stock"],
                estado=datos.get("estado", "Disponible"),
                id_categoria=datos["id_categoria"],
                imagen=imagen_url
            )

            db.session.add(nuevo_producto)
            db.session.commit()

            return producto_schema.dump(nuevo_producto), 201
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
class VistaPrivFacturas(Resource):    # Obtener todas las facturas
    def get(self):
        try:
            # Obtener todas las facturas
            facturas = Factura.query.all()

            # Serializar los datos para retornarlos en formato JSON
            facturas_serializadas = [
                {
                    "id_factura": factura.id_factura,
                    "fecha_factura": factura.fecha_factura.strftime('%Y-%m-%d %H:%M:%S'),  # Formatear la fecha
                    "total": factura.total,
                    "iva_total": factura.iva_total,
                    "estado": factura.estado,
                    "fecha_vencimiento": factura.fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S'),  # Formatear la fecha
                    "id_cliente": factura.id_cliente,
                    "cliente": {
                        "id_usuario": factura.cliente.id_usuario,
                        "nombres": factura.cliente.nombres,
                        "apellidos": factura.cliente.apellidos,
                        "email": factura.cliente.email
                    }
                }
                for factura in facturas
            ]

            return jsonify({"facturas": facturas_serializadas})

        except Exception as e:
            return {"mensaje": f"Error al obtener las facturas: {str(e)}"}, 500

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
    # Obtener factura por ID
    @jwt_required()  # Requiere un JWT válido para acceder
    def get(self, id_factura):
        try:
            # Buscar la factura por id_factura
            factura = Factura.query.filter_by(id_factura=id_factura).first()

            if not factura:
                return {"mensaje": "Factura no encontrada o no válida."}, 404

            # Serializar los datos de la factura
            factura_serializada = {
                "id_factura": factura.id_factura,
                "fecha_factura": factura.fecha_factura.strftime('%Y-%m-%d %H:%M:%S'),
                "total": factura.total,
                "iva_total": factura.iva_total,
                "estado": factura.estado,
                "fecha_vencimiento": factura.fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S'),
                "id_cliente": factura.id_cliente,
                "cliente": {
                    "id_usuario": factura.cliente.id_usuario,
                    "nombres": factura.cliente.nombres,
                    "apellidos": factura.cliente.apellidos,
                    "email": factura.cliente.email
                }
            }

            return jsonify({"factura": factura_serializada})

        except Exception as e:
            return {"mensaje": f"Error al obtener la factura: {str(e)}"}, 500
    
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
class VistaFormularioPago(Resource):
    @jwt_required()  # Requiere autenticación
    def post(self):
        try:
            data = request.json

            factura = Factura.query.filter_by(id_factura=data.get("id_factura")).first()
            if not factura:
                return {"mensaje": "Factura no encontrada."}, 404

            if not data.get("tipo_pago"):
                return {"mensaje": "El tipo de pago es obligatorio."}, 400

            referencia_pago = str(uuid.uuid4())[:10] 

            nuevo_pago = FormularioPago(
                id_factura=factura.id_factura,
                titular=data.get("titular"),
                numero_tarjeta=data.get("numero_tarjeta"),
                fecha_expiracion=data.get("fecha_expiracion"),
                codigo_seguridad=data.get("codigo_seguridad"),
                estado_pago="Pagado",  
                referencia_pago=referencia_pago,
                fecha_pago=datetime.utcnow()
            )

            db.session.add(nuevo_pago)

            factura.estado = "Pagada"

            db.session.commit()

            return {
                "mensaje": "Pago registrado exitosamente.",
                "pago": {
                    "id_formulario": nuevo_pago.id_formulario,
                    "id_factura": nuevo_pago.id_factura,
                    "titular": nuevo_pago.titular,
                    "estado_pago": nuevo_pago.estado_pago,
                    "referencia_pago": nuevo_pago.referencia_pago,
                    "fecha_pago": nuevo_pago.fecha_pago.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, 201

        except Exception as e:
            return {"mensaje": f"Error al procesar el pago: {str(e)}"}, 500
        
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

# ----------------------- Gestión de Proveedores

class VistaAdminProveedores(Resource):
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
    def post(self):
        try:
            id_usuario = request.json.get("id_usuario")
            id_producto = request.json.get("id_producto")
            cantidad = request.json.get("cantidad", 1)

            if not id_usuario or not id_producto:
                return {"mensaje": "Datos incompletos: se requiere id_usuario y id_producto."}, 400

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
    def get(self, id_usuario):
        try:
            # Buscar carrito del usuario
            carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
            if not carrito:
                return {"mensaje": "Carrito no encontrado."}, 404

            # Serializar productos en el carrito
            productos_serializados = [
                {
                    "id_producto": detalle.id_producto,
                    "nombre": detalle.producto.nombre,
                    "cantidad": detalle.cantidad,
                    "precio_unitario": detalle.producto.precio,
                    "subtotal": detalle.cantidad * detalle.producto.precio
                }
                for detalle in carrito.productos
            ]

            return jsonify({"productos": productos_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener el carrito: {str(e)}"}, 500

class VistaProductoCarrito(Resource):

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
    @jwt_required()  # Requiere un JWT válido para acceder
    def post(self, id_usuario):
        try:
            # Buscar carrito del usuario
            carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
            if not carrito or not carrito.productos:
                return {"mensaje": "El carrito está vacío o no existe."}, 400

            # Procesar compra
            total = sum(
                detalle.cantidad * detalle.producto.precio
                for detalle in carrito.productos
            )

            # Vaciar carrito
            for detalle in carrito.productos:
                db.session.delete(detalle)

            db.session.commit()
            return {"mensaje": "Compra procesada exitosamente.", "total": total}, 200
        except Exception as e:
            return {"mensaje": f"Error al procesar la compra: {str(e)}"}, 500



# ---------------- Parte de LOGIN
class VistaLogIn(Resource):
    def post(self):
        u_email = request.json["email"]
        u_contrasena = request.json["contrasena"]
        
        usuario = Usuario.query.filter_by(email=u_email).first()  
        print(usuario)
        if usuario and usuario.verificar_contrasena(u_contrasena):
            token_de_acceso = create_access_token(identity=request.json['email'])
            return {
                'usuario': usuario.id_usuario,
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
                    "id_proveedor": marca.id_proveedor
                }
                for marca in marcas
            ]
            return jsonify({"marcas": marcas_serializadas})
        except Exception as e:
            return {"mensaje": f"Error al obtener las marcas: {str(e)}"}, 500

    # Agregar una nueva marca
    @jwt_required()
    def post(self):
        try:
            if not request.json.get("nombre") or not request.json.get("id_proveedor"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            nueva_marca = Marca(
                nombre=request.json["nombre"],
                estado=request.json.get("estado", "Activo"),
                id_proveedor=request.json["id_proveedor"]
            )

            db.session.add(nueva_marca)
            db.session.commit()

            return {
                "mensaje": "Marca agregada exitosamente.",
                "marca": {
                    "id_marca": nueva_marca.id_marca,
                    "nombre": nueva_marca.nombre,
                    "estado": nueva_marca.estado
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
                "id_proveedor": marca.id_proveedor
            }

            return jsonify({"marca": marca_serializada})
        except Exception as e:
            return {"mensaje": f"Error al obtener la marca: {str(e)}"}, 500

    # Actualizar marca
    @jwt_required()
    def put(self, id_marca):
        try:
            marca = Marca.query.get(id_marca)
            if not marca:
                return {"mensaje": "Marca no encontrada."}, 404

            marca.nombre = request.json.get("nombre", marca.nombre)
            marca.id_proveedor = request.json.get("id_proveedor", marca.id_proveedor)

            db.session.commit()

            return {"mensaje": "Marca actualizada exitosamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar la marca: {str(e)}"}, 500

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
            descuentos = Descuento.query.all()
            return jsonify({"descuentos": descuentos_schema.dump(descuentos)})
        except Exception as e:
            return {"mensaje": f"Error al obtener los descuentos: {str(e)}"}, 500

    @jwt_required()
    def post(self):
        try:
            data = request.json
            if not data.get("id_producto") or not data.get("porcentaje"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            nuevo_descuento = Descuento(
                id_producto=data["id_producto"],
                porcentaje=data["porcentaje"],
                fecha_inicio=data.get("fecha_inicio"),
                fecha_fin=data.get("fecha_fin"),
            )

            db.session.add(nuevo_descuento)
            db.session.commit()

            return {
                "mensaje": "Descuento agregado exitosamente.",
                "descuento": descuento_schema.dump(nuevo_descuento)
            }, 201

        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error de integridad: El producto no existe."}, 400
        except Exception as e:
            return {"mensaje": f"Error al agregar el descuento: {str(e)}"}, 500

class VistaDescuento(Resource):
    def get(self, id_descuento):
        try:
            descuento = Descuento.query.get(id_descuento)
            if not descuento:
                return {"mensaje": "Descuento no encontrado."}, 404
            return jsonify({"descuento": descuento_schema.dump(descuento)})
        except Exception as e:
            return {"mensaje": f"Error al obtener el descuento: {str(e)}"}, 500

    @jwt_required()
    def put(self, id_descuento):
        try:
            descuento = Descuento.query.get(id_descuento)
            if not descuento:
                return {"mensaje": "Descuento no encontrado."}, 404

            data = request.json
            descuento.porcentaje = data.get("porcentaje", descuento.porcentaje)
            descuento.fecha_inicio = data.get("fecha_inicio", descuento.fecha_inicio)
            descuento.fecha_fin = data.get("fecha_fin", descuento.fecha_fin)

            db.session.commit()

            return {
                "mensaje": "Descuento actualizado exitosamente.",
                "descuento": descuento_schema.dump(descuento)
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el descuento: {str(e)}"}, 500

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
                    "imagen": animal.imagen
                }
                for animal in animales
            ]
            return jsonify({"animales": animales_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los animales: {str(e)}"}, 500

    @jwt_required()
    def post(self):
        try:
            datos = request.form  # Cambiado de request.json a request.form
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                imagen_url = upload_result.get('secure_url')
            else:
                imagen_url = None

            nuevo_animal = Animal(
                nombre=datos["nombre"],
                imagen=imagen_url
            )

            db.session.add(nuevo_animal)
            db.session.commit()

            return {"mensaje": "Animal agregado exitosamente.", "animal": animal_schema.dump(nuevo_animal)}, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar el animal: {str(e)}"}, 500


class VistaAnimal(Resource):
    def get(self, id_animal):
        try:
            animal = Animal.query.get(id_animal)
            if not animal:
                return {"mensaje": "Animal no encontrado."}, 404

            return jsonify({"animal": animal_schema.dump(animal)})
        except Exception as e:
            return {"mensaje": f"Error al obtener el animal: {str(e)}"}, 500

    @jwt_required()
    def put(self, id_animal):
        try:
            animal = Animal.query.get(id_animal)
            if not animal:
                return {"mensaje": "Animal no encontrado."}, 404

            datos = request.form
            animal.nombre = datos.get("nombre", animal.nombre)

            # Gestionar nueva imagen si se envía
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                animal.imagen = upload_result.get('secure_url')

            db.session.commit()

            return {"mensaje": "Animal actualizado exitosamente.", "animal": animal_schema.dump(animal)}, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el animal: {str(e)}"}, 500

    @jwt_required()
    def delete(self, id_animal):
        try:
            animal = Animal.query.get(id_animal)
            if not animal:
                return {"mensaje": "Animal no encontrado."}, 404

            db.session.delete(animal)
            db.session.commit()

            return {"mensaje": "Animal eliminado correctamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al eliminar el animal: {str(e)}"}, 500
