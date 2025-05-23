from flask_restful import Resource
from flask import jsonify, current_app, request
import uuid
from ..modelos import db, Usuario, UsuarioSchema, MetodoPago, MetodoPagoSchema, Categoria, CategoriaSchema, TipoDoc, TipoDocSchema, Rol, RolSchema, Proveedor, ProveedorSchema, Producto, ProductoSchema, Factura, FacturaSchema, DetalleFactura, DetalleFacturaSchema, Carrito, DetalleCarrito
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
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)


usuario_schema = UsuarioSchema()
rol_schema = RolSchema()
metodo_pago = MetodoPagoSchema()
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
            # Filtrar los usuarios con id_rol = 2 (clientes)
            clientes = Usuario.query.filter_by(id_rol=2).all()

            # Serializar los datos para retornarlos en formato JSON
            clientes_serializados = [
                {
                    "id_usuario": cliente.id_usuario,
                    "nombres": cliente.nombres,
                    "apellidos": cliente.apellidos,
                    "telefono": cliente.telefono,
                    "email": cliente.email,
                    "tipo_doc": cliente.tipo_doc,
                    "num_documento": cliente.num_documento,
                    "direccion": cliente.direccion
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
@jwt_required()  # Requiere un JWT válido para acceder
    # Desactivar cliente
def patch(self, id_usuario):
    try:
        # Buscar el cliente por ID
        cliente = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=2).first()
        if not cliente:
            return {"mensaje": "Cliente no encontrado o no válido."}, 404

        # Cambiar estado a inactivo
        cliente.estado = "inactivo"
        db.session.commit()

        return {"mensaje": "Cliente desactivado exitosamente."}, 200
    except Exception as e:
        return {"mensaje": f"Error al desactivar el cliente: {str(e)}"}, 500

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
        empleado.estado = "inactivo"
        db.session.commit()

        return {"mensaje": "Empleado desactivado exitosamente."}, 200
    except Exception as e:
        return {"mensaje": f"Error al desactivar el empleado: {str(e)}"}, 500

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
                    "metodo_pago": factura.metodo_pago,
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

    @jwt_required()  # Requiere un JWT válido para acceder
    # Agregar una nueva factura
    def post(self):
        try:
            # Validar que los campos necesarios estén presentes
            if not request.json.get("total") or not request.json.get("estado") or not request.json.get("metodo_pago"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            # Crear una nueva factura
            nueva_factura = Factura(
                fecha_factura=request.json.get("fecha_factura"),
                total=request.json["total"],
                iva_total=request.json["iva_total"],
                estado=request.json["estado"],
                metodo_pago=request.json["metodo_pago"],
                fecha_vencimiento=request.json.get("fecha_vencimiento"),
                id_cliente=request.json["id_cliente"]
            )

            db.session.add(nueva_factura)
            db.session.commit()

            return {
                "mensaje": "Factura agregada exitosamente.",
                "factura": {
                    "id_factura": nueva_factura.id_factura,
                    "fecha_factura": nueva_factura.fecha_factura.strftime('%Y-%m-%d %H:%M:%S'),
                    "total": nueva_factura.total,
                    "iva_total": nueva_factura.iva_total,
                    "estado": nueva_factura.estado,
                    "metodo_pago": nueva_factura.metodo_pago,
                    "fecha_vencimiento": nueva_factura.fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S'),
                    "id_cliente": nueva_factura.id_cliente
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar la factura: {str(e)}"}, 500

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
                "metodo_pago": factura.metodo_pago,
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
            factura.metodo_pago = request.json.get("metodo_pago", factura.metodo_pago)
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
                    "metodo_pago": factura.metodo_pago,
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
        if usuario and usuario.verificar_contrasena(u_contrasena):
            token_de_acceso = create_access_token(identity=request.json['email'])
            return {
                'mensaje': 'Inicio de sesión exitoso',
                'token_de_acceso': token_de_acceso,
            }, 200
        else:
            return {'mensaje': 'Email o contraseña incorrectos'}, 401


class VistaSignIn(Resource):
    def post(self):
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


class VistaPrivMetodoPago(Resource):
    @jwt_required()  # Requiere un JWT válido para acceder
    # Obtener todos los métodos de pago
    def get(self):
        try:
            metodos_pago = MetodoPago.query.all()
            metodos_pago_serializados = [
                {
                    "id_pago": metodo.id_pago,
                    "nombre": metodo.nombre
                }
                for metodo in metodos_pago
            ]
            return jsonify({"metodos_pago": metodos_pago_serializados})
        except Exception as e:
            return {"mensaje": f"Error al obtener los métodos de pago: {str(e)}"}, 500

    @jwt_required()  # Requiere un JWT válido para acceder
    # Agregar un nuevo método de pago
    def post(self):
        try:
            if not request.json.get("nombre"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            nuevo_metodo_pago = MetodoPago(
                nombre=request.json["nombre"]
            )

            db.session.add(nuevo_metodo_pago)
            db.session.commit()

            return {
                "mensaje": "Método de pago agregado exitosamente.",
                "metodo_pago": {
                    "id_pago": nuevo_metodo_pago.id_pago,
                    "nombre": nuevo_metodo_pago.nombre
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar el método de pago: {str(e)}"}, 500

class VistaPrivMetodoPagos(Resource):
    @jwt_required()  # Requiere un JWT válido para acceder
    # Modificar método de pago
    def put(self, id_pago):
        try:
            metodo_pago = MetodoPago.query.filter_by(id_pago=id_pago).first()
            if not metodo_pago:
                return {"mensaje": "Método de pago no encontrado."}, 404

            metodo_pago.nombre = request.json.get("nombre", metodo_pago.nombre)

            db.session.commit()

            return {
                "mensaje": "Método de pago actualizado exitosamente.",
                "metodo_pago": {
                    "id_pago": metodo_pago.id_pago,
                    "nombre": metodo_pago.nombre
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el método de pago: {str(e)}"}, 500


class VistaPrivCategoria(Resource):
    # Obtener todas las categorías
    def get(self):
        try:
            categorias = Categoria.query.all()
            categorias_serializadas = [
                {
                    "id_categoria": categoria.id_categoria,
                    "nombre": categoria.nombre,
                    "descripcion": categoria.descripcion
                }
                for categoria in categorias
            ]
            return jsonify({"categorias": categorias_serializadas})
        except Exception as e:
            return {"mensaje": f"Error al obtener las categorías: {str(e)}"}, 500

    @jwt_required()  # Requiere un JWT válido para acceder
    # Agregar una nueva categoría
    def post(self):
        try:
            if not request.json.get("nombre"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            nueva_categoria = Categoria(
                nombre=request.json["nombre"],
                descripcion=request.json.get("descripcion")
            )

            db.session.add(nueva_categoria)
            db.session.commit()

            return {
                "mensaje": "Categoría agregada exitosamente.",
                "categoria": {
                    "id_categoria": nueva_categoria.id_categoria,
                    "nombre": nueva_categoria.nombre
                }
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar la categoría: {str(e)}"}, 500

class VistaPrivCategorias(Resource):
    @jwt_required()  # Requiere un JWT válido para acceder
    # Modificar categoría
    def put(self, id_categoria):
        try:
            categoria = Categoria.query.filter_by(id_categoria=id_categoria).first()
            if not categoria:
                return {"mensaje": "Categoría no encontrada."}, 404

            categoria.nombre = request.json.get("nombre", categoria.nombre)
            categoria.descripcion = request.json.get("descripcion", categoria.descripcion)

            db.session.commit()

            return {
                "mensaje": "Categoría actualizada exitosamente.",
                "categoria": {
                    "id_categoria": categoria.id_categoria,
                    "nombre": categoria.nombre,
                    "descripcion": categoria.descripcion
                }
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar la categoría: {str(e)}"}, 500
