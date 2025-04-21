from flask_restx import Namespace, Resource, fields
from .vistas import *  # Importa las vistas originales
from ..modelos import db, Usuario, Rol, Producto, DetalleFactura, Factura, Proveedor, TipoDoc, Rol, Categoria, Marca, Descuento, Animal, Carrito, DetalleCarrito, FormularioPago
from flask_jwt_extended import (
    jwt_required, 
    create_access_token, 
    get_jwt_identity,
    verify_jwt_in_request
)

# ======================================
# NAMESPACES PRINCIPALES
# ======================================

auth_ns = Namespace('auth', description='Operaciones de autenticación', security='Bearer')
usuarios_ns = Namespace('usuarios', description='Operaciones con usuarios', security='Bearer')
clientes_ns = Namespace('clientes', description='Operaciones con clientes', security='Bearer')
empleados_ns = Namespace('empleados', description='Operaciones con empleados', security='Bearer')
productos_ns = Namespace('productos', description='Operaciones con productos', security='Bearer')
categorias_ns = Namespace('categorias', description='Operaciones con categorías', security='Bearer')
marcas_ns = Namespace('marcas', description='Operaciones con marcas', security='Bearer')
animales_ns = Namespace('animales', description='Operaciones con animales', security='Bearer')
descuentos_ns = Namespace('descuentos', description='Operaciones con descuentos', security='Bearer')
facturas_ns = Namespace('facturas', description='Operaciones con facturas', security='Bearer')
pagos_ns = Namespace('pagos', description='Operaciones de pago', security='Bearer')
carrito_ns = Namespace('carrito', description='Operaciones del carrito de compras', security='Bearer')
reportes_ns = Namespace('reportes', description='Reportes del sistema', security='Bearer')
proveedores_ns = Namespace('proveedores', description='Operaciones con los proveedores', security='Bearer')
config_ns = Namespace('config', description='Configuraciones del sistema', security='Bearer')

# ======================================
# MODELOS PARA SWAGGER
# ======================================

# Modelo para cliente
cliente_model = clientes_ns.model('Cliente', {
    'id_usuario': fields.Integer(readOnly=True, description='ID del cliente'),
    'nombres': fields.String(required=True, description='Nombres del cliente'),
    'apellidos': fields.String(required=True, description='Apellidos del cliente'),
    'email': fields.String(required=True, description='Email del cliente'),
    'telefono': fields.String(description='Teléfono del cliente'),
    'tipo_doc': fields.Integer(description='Tipo de documento'),
    'num_documento': fields.String(description='Número de documento'),
    'direccion': fields.String(description='Dirección del cliente'),
    'estado': fields.String(description='Estado del cliente (Activo/Inactivo)')
})

# Modelo para creación de cliente
cliente_creacion_model = clientes_ns.model('ClienteCreacion', {
    'nombres': fields.String(required=True),
    'apellidos': fields.String(required=True),
    'email': fields.String(required=True),
    'telefono': fields.String(),
    'tipo_doc': fields.Integer(),
    'num_documento': fields.String(),
    'direccion': fields.String(),
    'contrasena': fields.String(required=True)
})

# Modelo para actualización de cliente
cliente_actualizacion_model = clientes_ns.model('ClienteActualizacion', {
    'nombres': fields.String(),
    'apellidos': fields.String(),
    'telefono': fields.String(),
    'email': fields.String(),
    'tipo_doc': fields.Integer(),
    'num_documento': fields.String(),
    'direccion': fields.String(),
    'contrasena': fields.String()
})

estado_model = clientes_ns.model('EstadoCliente', {
    'estado': fields.String(required=True, enum=['Activo', 'Inactivo'], description='Nuevo estado del cliente')
})

# Modelos para empleado
empleado_model = empleados_ns.model('Empleado', {
    'id_usuario': fields.Integer(readOnly=True, description='ID del empleado'),
    'nombres': fields.String(required=True, description='Nombres del empleado'),
    'apellidos': fields.String(required=True, description='Apellidos del empleado'),
    'email': fields.String(required=True, description='Email del empleado'),
    'telefono': fields.String(description='Teléfono del empleado'),
    'tipo_doc': fields.Integer(description='Tipo de documento'),
    'num_documento': fields.String(description='Número de documento'),
    'direccion': fields.String(description='Dirección del empleado'),
    'estado': fields.String(description='Estado del empleado (Activo/Inactivo)')
})

empleado_creacion_model = empleados_ns.model('EmpleadoCreacion', {
    'nombres': fields.String(required=True),
    'apellidos': fields.String(required=True),
    'email': fields.String(required=True),
    'telefono': fields.String(),
    'tipo_doc': fields.Integer(),
    'num_documento': fields.String(),
    'direccion': fields.String(),
    'contrasena': fields.String(required=True)
})

empleado_actualizacion_model = empleados_ns.model('EmpleadoActualizacion', {
    'nombres': fields.String(),
    'apellidos': fields.String(),
    'telefono': fields.String(),
    'email': fields.String(),
    'tipo_doc': fields.Integer(),
    'num_documento': fields.String(),
    'direccion': fields.String(),
    'contrasena': fields.String()
})

estado_empleado_model = empleados_ns.model('EstadoEmpleado', {
    'estado': fields.String(required=True, enum=['Activo', 'Inactivo'], description='Nuevo estado del empleado')
})




# Modelos para producto
producto_model = productos_ns.model('Producto', {
    'id_producto': fields.Integer(readOnly=True, description='ID del producto'),
    'nombre': fields.String(required=True, description='Nombre del producto'),
    'descripcion': fields.String(description='Descripción del producto'),
    'precio': fields.Float(required=True, description='Precio del producto'),
    'precio_descuento': fields.Float(description='Precio con descuento'),
    'stock': fields.Integer(required=True, description='Cantidad en stock'),
    'estado': fields.String(description='Estado del producto'),
    'id_categoria': fields.Integer(required=True, description='ID de la categoría'),
    'id_marca': fields.Integer(required=True, description='ID de la marca'),
    'id_animal': fields.Integer(required=True, description='ID del animal'),
    'categoria': fields.String(description='Nombre de la categoría'),
    'marca': fields.String(description='Nombre de la marca'),
    'animal': fields.String(description='Nombre del animal'),
    'imagen': fields.String(description='URL de la imagen del producto'),
    'tiene_descuento': fields.Boolean(description='Indica si tiene descuento activo')
})

producto_creacion_model = productos_ns.model('ProductoCreacion', {
    'nombre': fields.String(required=True),
    'descripcion': fields.String(),
    'precio': fields.Float(required=True),
    'stock': fields.Integer(required=True),
    'estado': fields.String(default='Disponible'),
    'id_categoria': fields.Integer(required=True),
    'id_marca': fields.Integer(required=True),
    'id_animal': fields.Integer(required=True),
    'imagen': fields.String(description='URL de la imagen (opcional)')
})

producto_actualizacion_model = productos_ns.model('ProductoActualizacion', {
    'nombre': fields.String(),
    'descripcion': fields.String(),
    'precio': fields.Float(),
    'stock': fields.Integer(),
    'estado': fields.String(),
    'id_categoria': fields.Integer(),
    'id_marca': fields.Integer(),
    'id_animal': fields.Integer(),
    'imagen': fields.String(description='URL de la imagen (opcional)')
})

estado_producto_model = productos_ns.model('EstadoProducto', {
    'estado': fields.String(required=True, enum=['Disponible', 'Agotado', 'Inactivo'], 
    description='Nuevo estado del producto')
})


# Modelos para facturas
factura_model = facturas_ns.model('Factura', {
    'id_factura': fields.Integer(readOnly=True, description='ID de la factura'),
    'fecha_factura': fields.DateTime(description='Fecha de creación de la factura'),
    'total': fields.Float(required=True, description='Total de la factura'),
    'iva_total': fields.Float(description='IVA total de la factura'),
    'estado': fields.String(required=True, enum=['Pendiente', 'Pagada', 'Cancelada'], description='Estado de la factura'),
    'fecha_vencimiento': fields.DateTime(description='Fecha de vencimiento del pago'),
    'id_cliente': fields.Integer(required=True, description='ID del cliente asociado'),
    'cliente': fields.Nested(cliente_model, description='Datos básicos del cliente') 
})

factura_creacion_model = facturas_ns.model('FacturaCreacion', {
    'total': fields.Float(required=True),
    'iva_total': fields.Float(default=0),
    'id_cliente': fields.Integer(required=True),
    'fecha_vencimiento': fields.DateTime(description='Fecha de vencimiento (opcional)')
})

factura_actualizacion_model = facturas_ns.model('FacturaActualizacion', {
    'total': fields.Float(),
    'iva_total': fields.Float(),
    'estado': fields.String(enum=['Pendiente', 'Pagada', 'Cancelada']),
    'fecha_vencimiento': fields.DateTime(),
    'id_cliente': fields.Integer()
})

estado_factura_model = facturas_ns.model('EstadoFactura', {
    'estado': fields.String(required=True, enum=['Pagada', 'Cancelada'], description='Nuevo estado de la factura')
})


# Modelos para pago
pago_model = pagos_ns.model('Pago', {
    'id_formulario': fields.Integer(readOnly=True, description='ID del pago'),
    'id_factura': fields.Integer(required=True, description='ID de la factura asociada'),
    'tipo_pago': fields.String(required=True, enum=['tarjeta', 'efectivo', 'transferencia'], description='Tipo de pago'),
    'titular': fields.String(description='Titular del pago (para tarjeta)'),
    'numero_tarjeta': fields.String(description='Número de tarjeta (enmascarado)'),
    'fecha_expiracion': fields.String(description='Fecha de expiración (MM/YY)'),
    'codigo_seguridad': fields.String(description='Código de seguridad (enmascarado)'),
    'estado_pago': fields.String(required=True, enum=['Procesando', 'Aprobado', 'Rechazado', 'Pendiente'], description='Estado del pago'),
    'referencia_pago': fields.String(description='Referencia única del pago'),
    'fecha_pago': fields.DateTime(description='Fecha y hora del pago')
})

pago_creacion_model = pagos_ns.model('PagoCreacion', {
    'id_factura': fields.Integer(required=True),
    'tipo_pago': fields.String(required=True, enum=['tarjeta', 'efectivo', 'transferencia']),
    'titular': fields.String(),
    'numero_tarjeta': fields.String(),
    'fecha_expiracion': fields.String(),
    'codigo_seguridad': fields.String()
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='Email del usuario'),
    'contrasena': fields.String(required=True, description='Contraseña del usuario')
})

# Modelos de autenticacion
signup_model = auth_ns.model('SignUp', {
    'nombres': fields.String(required=True),
    'apellidos': fields.String(),
    'telefono': fields.String(),
    'email': fields.String(required=True),
    'tipo_doc': fields.Integer(),
    'num_documento': fields.String(),
    'direccion': fields.String(),
    'contrasena': fields.String(required=True)
})

token_response = auth_ns.model('TokenResponse', {
    'usuario': fields.String(description='ID del usuario'),
    'mensaje': fields.String(),
    'token_de_acceso': fields.String()
})

# Modelos de configuracion
tipo_doc_model = config_ns.model('TipoDocumento', {
    'id_TipoDocumento': fields.Integer(readOnly=True),
    'Nombre': fields.String(required=True),
    'Descripcion': fields.String()
})

rol_model = config_ns.model('Rol', {
    'id_Rol': fields.Integer(readOnly=True),
    'Nombre': fields.String(required=True),
    'Descripcion': fields.String()
})

# Modelos de categorias
categoria_model = categorias_ns.model('Categoria', {
    'id_categoria': fields.Integer(readOnly=True),
    'nombre': fields.String(required=True),
    'descripcion': fields.String(),
    'imagen': fields.String()
})

categoria_creacion_model = categorias_ns.model('CategoriaCreacion', {
    'nombre': fields.String(required=True),
    'descripcion': fields.String(),
    'imagen': fields.String(description='URL de imagen o archivo')
})

# Modelos de marcas

marca_model = marcas_ns.model('Marca', {
    'id_marca': fields.Integer(readOnly=True),
    'nombre': fields.String(required=True),
    'estado': fields.String(enum=['Activo', 'Inactivo']),
    'id_proveedor': fields.Integer(),
    'imagen': fields.String()
})

marca_creacion_model = marcas_ns.model('MarcaCreacion', {
    'nombre': fields.String(required=True),
    'estado': fields.String(default='Activo'),
    'id_proveedor': fields.Integer(required=True),
    'imagen': fields.String(description='URL de imagen o archivo')
})

# Modelos de animales
animal_model = animales_ns.model('Animal', {
    'id_animal': fields.Integer(readOnly=True),
    'nombre': fields.String(required=True),
    'imagen': fields.String(),
    'estado': fields.String(enum=['Activo', 'Inactivo'])
})

animal_creacion_model = animales_ns.model('AnimalCreacion', {
    'nombre': fields.String(required=True),
    'imagen': fields.String(description='URL de imagen o archivo'),
    'estado': fields.String(default='Activo')
})

# Modelos de reportes
reporte_ventas_model = reportes_ns.model('ReporteVentas', {
    'fecha': fields.String(),
    'total': fields.Float()
})

reporte_productos_model = reportes_ns.model('ReporteProductos', {
    'nombre': fields.String(),
    'vendidos': fields.Integer(),
    'ingresos': fields.Float()
})

reporte_stock_model = reportes_ns.model('ReporteStock', {
    'id_producto': fields.Integer(),
    'nombre': fields.String(),
    'stock': fields.Integer(),
    'precio': fields.Float()
})

reporte_usuarios_model = reportes_ns.model('ReporteUsuarios', {
    'usuarios_activos': fields.Integer(),
    'nuevos_clientes': fields.Integer()
})

# Modelos para carrito
producto_carrito_model = carrito_ns.model('ProductoCarrito', {
    'id_producto': fields.Integer(required=True, description='ID del producto'),
    'nombre': fields.String(description='Nombre del producto'),
    'cantidad': fields.Integer(required=True, description='Cantidad en el carrito'),
    'precio': fields.Float(description='Precio unitario'),
    'precio_original': fields.Float(description='Precio original sin descuento'),
    'precio_descuento': fields.Float(description='Precio con descuento'),
    'subtotal': fields.Float(description='Subtotal (cantidad x precio)'),
    'imagen': fields.String(description='URL de la imagen del producto')
})

carrito_model = carrito_ns.model('Carrito', {
    'id_carrito': fields.Integer(readOnly=True, description='ID del carrito'),
    'productos': fields.List(fields.Nested(producto_carrito_model), description='Productos en el carrito')
})

item_carrito_model = carrito_ns.model('ItemCarrito', {
    'id_producto': fields.Integer(required=True, description='ID del producto'),
    'cantidad': fields.Integer(required=True, description='Cantidad a agregar')
})


# Modelo de DetalleCarrito
detalle_carrito_model = carrito_ns.model('DetalleCarrito', {
    'id_detalle': fields.Integer(readOnly=True, description='ID del detalle'),
    'id_carrito': fields.Integer(required=True, description='ID del carrito'),
    'id_producto': fields.Integer(required=True, description='ID del producto'),
    'cantidad': fields.Integer(required=True, description='Cantidad del producto')
})

# Modelo de Reporte
reporte_model = reportes_ns.model('Reporte', {
    'tipo': fields.String(required=True, description='Tipo de reporte'),
    'fecha_inicio': fields.DateTime(description='Fecha de inicio'),
    'fecha_fin': fields.DateTime(description='Fecha de fin'),
    'datos': fields.Raw(description='Datos del reporte')
})

#modelo de proveedor
proveedor_model = proveedores_ns.model('Proveedor', {
    'id_proveedor': fields.Integer(readOnly=True, description='ID del proveedor'),
    'nombre': fields.String(required=True, description='Nombre del proveedor'),
    'telefono': fields.String(required=True, description='Teléfono del proveedor'),
    'correo': fields.String(required=True, description='Correo electrónico del proveedor'),
    'estado': fields.String(enum=['activo', 'inactivo'], description='Estado del proveedor')
})

proveedor_creacion_model = proveedores_ns.model('ProveedorCreacion', {
    'nombre': fields.String(required=True),
    'telefono': fields.String(required=True),
    'correo': fields.String(required=True),
    'estado': fields.String(default='activo')
})

proveedor_actualizacion_model = proveedores_ns.model('ProveedorActualizacion', {
    'nombre': fields.String(),
    'telefono': fields.String(),
    'correo': fields.String(),
    'estado': fields.String(enum=['activo', 'inactivo'])
})

# Modelos de descuentos

descuento_model = descuentos_ns.model('Descuento', {
    'id_descuento': fields.Integer(readOnly=True),
    'porcentaje_descuento': fields.Float(required=True),
    'fecha_inicio': fields.DateTime(),
    'fecha_fin': fields.DateTime(),
    'id_producto': fields.Integer(required=True),
    'producto': fields.Nested(producto_model, description='Operaciones con producto')  # Changed this line
})

descuento_creacion_model = descuentos_ns.model('DescuentoCreacion', {
    'id_producto': fields.Integer(required=True),
    'porcentaje_descuento': fields.Float(required=True),
    'fecha_inicio': fields.DateTime(),
    'fecha_fin': fields.DateTime()
})

producto_reporte_model = reportes_ns.model('ProductoReporte', {
    'nombre': fields.String(description='Nombre del producto'),
    'vendidos': fields.Integer(description='Cantidad vendida'),
    'ingresos': fields.Float(description='Ingresos generados')
})

# Model for low stock report
stock_reporte_model = reportes_ns.model('StockReporte', {
    'id_producto': fields.Integer(description='ID del producto'),
    'nombre': fields.String(description='Nombre del producto'),
    'stock': fields.Integer(description='Cantidad en stock'),
    'precio': fields.Float(description='Precio del producto')
})

# Main report model
reporte_productos_model = reportes_ns.model('ReporteProductos', {
    'top_productos': fields.List(fields.Nested(producto_reporte_model)),
    'stock_bajo': fields.List(fields.Nested(stock_reporte_model))
})

# ------------------------------------- vistas


# Vista para cliente
@clientes_ns.route('/')
class VistaClientes(Resource):
    @clientes_ns.doc(security='Bearer')
    @clientes_ns.marshal_list_with(cliente_model)
    @clientes_ns.response(200, 'Lista de clientes obtenida exitosamente')
    @clientes_ns.response(401, 'No autorizado')
    @clientes_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def get(self):
        """Obtiene todos los clientes registrados"""
        try:
            clientes = Usuario.query.filter_by(id_rol=2).all()
            return [{
                "id_usuario": cliente.id_usuario,
                "nombres": cliente.nombres,
                "apellidos": cliente.apellidos,
                "telefono": cliente.telefono,
                "email": cliente.email,
                "tipo_doc": cliente.tipo_doc,
                "num_documento": cliente.num_documento,
                "direccion": cliente.direccion,
                "estado": cliente.estado
            } for cliente in clientes], 200
        except Exception as e:
            clientes_ns.abort(500, f"Error al obtener los clientes: {str(e)}")

    @clientes_ns.doc(security='Bearer')
    @clientes_ns.expect(cliente_creacion_model)
    @clientes_ns.marshal_with(cliente_model, code=201)
    @clientes_ns.response(201, 'Cliente creado exitosamente')
    @clientes_ns.response(400, 'Datos faltantes o inválidos')
    @clientes_ns.response(401, 'No autorizado')
    @clientes_ns.response(500, 'Error al crear cliente')
    @jwt_required()
    def post(self):
        """Crea un nuevo cliente"""
        try:
            data = clientes_ns.payload
            
            if not all([data.get('nombres'), data.get('apellidos'), data.get('email'), data.get('contrasena')]):
                clientes_ns.abort(400, "Faltan datos obligatorios")
            
            nuevo_cliente = Usuario(
                nombres=data['nombres'],
                apellidos=data['apellidos'],
                telefono=data.get('telefono'),
                email=data['email'],
                tipo_doc=data.get('tipo_doc'),
                num_documento=data.get('num_documento'),
                direccion=data.get('direccion'),
                id_rol=2
            )
            nuevo_cliente.contrasena = data['contrasena']
            
            db.session.add(nuevo_cliente)
            db.session.commit()
            
            return nuevo_cliente, 201
        except IntegrityError:
            db.session.rollback()
            clientes_ns.abort(400, "El email o documento ya están registrados")
        except Exception as e:
            db.session.rollback()
            clientes_ns.abort(500, f"Error al crear cliente: {str(e)}")

@clientes_ns.route('/<int:id_usuario>')
@clientes_ns.param('id_usuario', 'ID del cliente')
class VistaCliente(Resource):
    @clientes_ns.doc(security='Bearer')
    @clientes_ns.marshal_with(cliente_model)
    @clientes_ns.response(200, 'Cliente encontrado')
    @clientes_ns.response(404, 'Cliente no encontrado')
    @clientes_ns.response(401, 'No autorizado')
    @clientes_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def get(self, id_usuario):
        """Obtiene un cliente específico por su ID"""
        try:
            cliente = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=2).first()
            if not cliente:
                clientes_ns.abort(404, "Cliente no encontrado")
            return cliente, 200
        except Exception as e:
            clientes_ns.abort(500, f"Error al obtener cliente: {str(e)}")

    @clientes_ns.doc(security='Bearer')
    @clientes_ns.expect(cliente_actualizacion_model)
    @clientes_ns.marshal_with(cliente_model)
    @clientes_ns.response(200, 'Cliente actualizado exitosamente')
    @clientes_ns.response(400, 'Datos inválidos')
    @clientes_ns.response(401, 'No autorizado')
    @clientes_ns.response(404, 'Cliente no encontrado')
    @clientes_ns.response(500, 'Error al actualizar cliente')
    @jwt_required()
    def put(self, id_usuario):
        """Actualiza los datos de un cliente"""
        try:
            cliente = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=2).first()
            if not cliente:
                clientes_ns.abort(404, "Cliente no encontrado")
            
            data = clientes_ns.payload
            for campo in ['nombres', 'apellidos', 'telefono', 'email', 'tipo_doc', 'num_documento', 'direccion']:
                if campo in data:
                    setattr(cliente, campo, data[campo])
            
            if 'contrasena' in data:
                cliente.contrasena = data['contrasena']
            
            db.session.commit()
            return cliente, 200
        except Exception as e:
            db.session.rollback()
            clientes_ns.abort(500, f"Error al actualizar cliente: {str(e)}")

    @clientes_ns.doc(security='Bearer')
    @clientes_ns.expect(estado_model)
    @clientes_ns.marshal_with(cliente_model)
    @clientes_ns.response(200, 'Estado del cliente actualizado')
    @clientes_ns.response(400, 'Estado inválido')
    @clientes_ns.response(401, 'No autorizado (requiere rol admin)')
    @clientes_ns.response(404, 'Cliente no encontrado')
    @clientes_ns.response(500, 'Error al actualizar estado')
    @admin_required
    @jwt_required()
    def patch(self, id_usuario):
        """Actualiza el estado de un cliente (Requiere admin)"""
        try:
            cliente = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=2).first()
            if not cliente:
                clientes_ns.abort(404, "Cliente no encontrado")
            
            nuevo_estado = clientes_ns.payload['estado']
            if nuevo_estado not in ['Activo', 'Inactivo']:
                clientes_ns.abort(400, "Estado inválido")
            
            cliente.estado = nuevo_estado
            db.session.commit()
            
            return cliente, 200
        except Exception as e:
            db.session.rollback()
            clientes_ns.abort(500, f"Error al actualizar estado: {str(e)}")


# Vista para empleado


@empleados_ns.route('/')
class VistaAdminEmpleados(Resource):
    @empleados_ns.doc(security='Bearer')
    @empleados_ns.marshal_list_with(empleado_model)
    @empleados_ns.response(200, 'Lista de empleados obtenida exitosamente')
    @empleados_ns.response(401, 'No autorizado')
    @empleados_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @empleados_ns.response(500, 'Error interno del servidor')
    @admin_required
    @jwt_required()
    def get(self):
        """Obtiene todos los empleados registrados (Requiere admin)"""
        try:
            empleados = Usuario.query.filter_by(id_rol=3).all()
            return [{
                "id_usuario": empleado.id_usuario,
                "nombres": empleado.nombres,
                "apellidos": empleado.apellidos,
                "telefono": empleado.telefono,
                "email": empleado.email,
                "tipo_doc": empleado.tipo_doc,
                "num_documento": empleado.num_documento,
                "direccion": empleado.direccion,
                "estado": empleado.estado
            } for empleado in empleados], 200
        except Exception as e:
            empleados_ns.abort(500, f"Error al obtener los empleados: {str(e)}")

    @empleados_ns.doc(security='Bearer')
    @empleados_ns.expect(empleado_creacion_model)
    @empleados_ns.marshal_with(empleado_model, code=201)
    @empleados_ns.response(201, 'Empleado creado exitosamente')
    @empleados_ns.response(400, 'Datos faltantes o inválidos')
    @empleados_ns.response(401, 'No autorizado')
    @empleados_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @empleados_ns.response(500, 'Error al crear empleado')
    @admin_required
    @jwt_required()
    def post(self):
        """Crea un nuevo empleado (Requiere admin)"""
        try:
            data = empleados_ns.payload
            
            if not all([data.get('nombres'), data.get('apellidos'), data.get('email'), data.get('contrasena')]):
                empleados_ns.abort(400, "Faltan datos obligatorios")
            
            nuevo_empleado = Usuario(
                nombres=data['nombres'],
                apellidos=data['apellidos'],
                telefono=data.get('telefono'),
                email=data['email'],
                tipo_doc=data.get('tipo_doc'),
                num_documento=data.get('num_documento'),
                direccion=data.get('direccion'),
                id_rol=3
            )
            nuevo_empleado.contrasena = data['contrasena']
            
            db.session.add(nuevo_empleado)
            db.session.commit()
            
            return nuevo_empleado, 201
        except IntegrityError:
            db.session.rollback()
            empleados_ns.abort(400, "El email o documento ya están registrados")
        except Exception as e:
            db.session.rollback()
            empleados_ns.abort(500, f"Error al crear empleado: {str(e)}")

@empleados_ns.route('/<int:id_usuario>')
@empleados_ns.param('id_usuario', 'ID del empleado')
class VistaAdminEmpleado(Resource):
    @empleados_ns.doc(security='Bearer')
    @empleados_ns.marshal_with(empleado_model)
    @empleados_ns.response(200, 'Empleado encontrado')
    @empleados_ns.response(404, 'Empleado no encontrado')
    @empleados_ns.response(401, 'No autorizado')
    @empleados_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @empleados_ns.response(500, 'Error interno del servidor')
    @admin_required
    @jwt_required()
    def get(self, id_usuario):
        """Obtiene un empleado específico por su ID (Requiere admin)"""
        try:
            empleado = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=3).first()
            if not empleado:
                empleados_ns.abort(404, "Empleado no encontrado")
            return empleado, 200
        except Exception as e:
            empleados_ns.abort(500, f"Error al obtener empleado: {str(e)}")

    @empleados_ns.doc(security='Bearer')
    @empleados_ns.expect(empleado_actualizacion_model)
    @empleados_ns.marshal_with(empleado_model)
    @empleados_ns.response(200, 'Empleado actualizado exitosamente')
    @empleados_ns.response(400, 'Datos inválidos')
    @empleados_ns.response(401, 'No autorizado')
    @empleados_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @empleados_ns.response(404, 'Empleado no encontrado')
    @empleados_ns.response(500, 'Error al actualizar empleado')
    @admin_required
    @jwt_required()
    def put(self, id_usuario):
        """Actualiza los datos de un empleado (Requiere admin)"""
        try:
            empleado = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=3).first()
            if not empleado:
                empleados_ns.abort(404, "Empleado no encontrado")
            
            data = empleados_ns.payload
            for campo in ['nombres', 'apellidos', 'telefono', 'email', 'tipo_doc', 'num_documento', 'direccion']:
                if campo in data:
                    setattr(empleado, campo, data[campo])
            
            if 'contrasena' in data:
                empleado.contrasena = data['contrasena']
            
            db.session.commit()
            return empleado, 200
        except Exception as e:
            db.session.rollback()
            empleados_ns.abort(500, f"Error al actualizar empleado: {str(e)}")

    @empleados_ns.doc(security='Bearer')
    @empleados_ns.expect(estado_empleado_model)
    @empleados_ns.marshal_with(empleado_model)
    @empleados_ns.response(200, 'Estado del empleado actualizado')
    @empleados_ns.response(400, 'Estado inválido')
    @empleados_ns.response(401, 'No autorizado')
    @empleados_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @empleados_ns.response(404, 'Empleado no encontrado')
    @empleados_ns.response(500, 'Error al actualizar estado')
    @admin_required
    @jwt_required()
    def patch(self, id_usuario):
        """Actualiza el estado de un empleado (Activo/Inactivo) (Requiere admin)"""
        try:
            empleado = Usuario.query.filter_by(id_usuario=id_usuario, id_rol=3).first()
            if not empleado:
                empleados_ns.abort(404, "Empleado no encontrado")
            
            nuevo_estado = empleados_ns.payload['estado']
            if nuevo_estado not in ['Activo', 'Inactivo']:
                empleados_ns.abort(400, "Estado inválido")
            
            empleado.estado = nuevo_estado
            db.session.commit()
            
            return empleado, 200
        except Exception as e:
            db.session.rollback()
            empleados_ns.abort(500, f"Error al actualizar estado: {str(e)}")


# Vista para producto

@productos_ns.route('/')
class VistaPrivProductos(Resource):
    @productos_ns.doc(security='Bearer')
    @productos_ns.marshal_list_with(producto_model)
    @productos_ns.response(200, 'Lista de productos obtenida exitosamente')
    @productos_ns.response(401, 'No autorizado')
    @productos_ns.response(500, 'Error interno del servidor')
    def get(self):
        """Obtiene todos los productos registrados"""
        try:
            productos = Producto.query.all()
            return [{
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "precio_descuento": producto.precio_descuento,
                "tiene_descuento": producto.descuento_activo is not None,
                "stock": producto.stock,
                "estado": producto.estado,
                "id_categoria": producto.id_categoria,
                "id_marca": producto.id_marca,
                "id_animal": producto.id_animal,
                "categoria": producto.categoria.nombre if producto.categoria else None,
                "marca": producto.marca.nombre if producto.marca else None,
                "animal": producto.animal.nombre if producto.animal else None,
                "imagen": producto.imagen
            } for producto in productos], 200
        except Exception as e:
            productos_ns.abort(500, f"Error al obtener los productos: {str(e)}")

    @productos_ns.doc(security='Bearer')
    @productos_ns.expect(producto_creacion_model)
    @productos_ns.marshal_with(producto_model, code=201)
    @productos_ns.response(201, 'Producto creado exitosamente')
    @productos_ns.response(400, 'Datos faltantes o inválidos')
    @productos_ns.response(401, 'No autorizado')
    @productos_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @productos_ns.response(500, 'Error al crear producto')
    @admin_required
    @jwt_required()
    def post(self):
        """Crea un nuevo producto (Requiere admin)"""
        try:
            datos = request.form
            
            if not all([datos.get('nombre'), datos.get('precio'), datos.get('stock'),
                       datos.get('id_categoria'), datos.get('id_marca'), datos.get('id_animal')]):
                productos_ns.abort(400, "Faltan datos obligatorios")
            
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
            
            return nuevo_producto, 201
        except IntegrityError:
            db.session.rollback()
            productos_ns.abort(400, "Error de integridad en la base de datos")
        except Exception as e:
            db.session.rollback()
            productos_ns.abort(500, f"Error al crear producto: {str(e)}")

@productos_ns.route('/<int:id_producto>')
@productos_ns.param('id_producto', 'ID del producto')
class VistaPrivProducto(Resource):
    @productos_ns.doc(security='Bearer')
    @productos_ns.marshal_with(producto_model)
    @productos_ns.response(200, 'Producto encontrado')
    @productos_ns.response(404, 'Producto no encontrado')
    @productos_ns.response(401, 'No autorizado')
    @productos_ns.response(500, 'Error interno del servidor')
    def get(self, id_producto):
        """Obtiene un producto específico por su ID"""
        try:
            producto = Producto.query.filter_by(id_producto=id_producto).first()
            if not producto:
                productos_ns.abort(404, "Producto no encontrado")
            
            return {
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "stock": producto.stock,
                "estado": producto.estado,
                "id_categoria": producto.id_categoria,
                "categoria": producto.categoria.nombre if producto.categoria else None,
                "imagen": producto.imagen
            }, 200
        except Exception as e:
            productos_ns.abort(500, f"Error al obtener producto: {str(e)}")

    @productos_ns.doc(security='Bearer')
    @productos_ns.expect(producto_actualizacion_model)
    @productos_ns.marshal_with(producto_model)
    @productos_ns.response(200, 'Producto actualizado exitosamente')
    @productos_ns.response(400, 'Datos inválidos')
    @productos_ns.response(401, 'No autorizado')
    @productos_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @productos_ns.response(404, 'Producto no encontrado')
    @productos_ns.response(500, 'Error al actualizar producto')
    @jwt_required()
    def put(self, id_producto):
        """Actualiza los datos de un producto"""
        try:
            producto = Producto.query.filter_by(id_producto=id_producto).first()
            if not producto:
                productos_ns.abort(404, "Producto no encontrado")
            
            datos = request.form
            producto.nombre = datos.get("nombre", producto.nombre)
            producto.descripcion = datos.get("descripcion", producto.descripcion)
            producto.precio = float(datos.get("precio", producto.precio))
            producto.stock = int(datos.get("stock", producto.stock))
            producto.estado = datos.get("estado", producto.estado)
            producto.id_categoria = int(datos.get("id_categoria", producto.id_categoria))

            # Gestionar nueva imagen si se envía
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                producto.imagen = upload_result.get('secure_url')

            db.session.commit()
            return producto, 200
        except Exception as e:
            db.session.rollback()
            productos_ns.abort(500, f"Error al actualizar producto: {str(e)}")

    @productos_ns.doc(security='Bearer')
    @productos_ns.expect(estado_producto_model)
    @productos_ns.marshal_with(producto_model)
    @productos_ns.response(200, 'Estado del producto actualizado')
    @productos_ns.response(400, 'Estado inválido')
    @productos_ns.response(401, 'No autorizado')
    @productos_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @productos_ns.response(404, 'Producto no encontrado')
    @productos_ns.response(500, 'Error al actualizar estado')
    @admin_required
    @jwt_required()
    def patch(self, id_producto):
        """Actualiza el estado de un producto (Requiere admin)"""
        try:
            producto = Producto.query.filter_by(id_producto=id_producto).first()
            if not producto:
                productos_ns.abort(404, "Producto no encontrado")
            
            nuevo_estado = productos_ns.payload.get('estado', 'Inactivo')
            if nuevo_estado not in ['Disponible', 'Agotado', 'Inactivo']:
                productos_ns.abort(400, "Estado inválido")
            
            producto.estado = nuevo_estado
            db.session.commit()
            
            return producto, 200
        except Exception as e:
            db.session.rollback()
            productos_ns.abort(500, f"Error al actualizar estado: {str(e)}")

# Vista para factura

@facturas_ns.route('/')
class VistaPrivFacturas(Resource):
    @facturas_ns.doc(security='Bearer')
    @facturas_ns.marshal_list_with(factura_model)
    @facturas_ns.response(200, 'Lista de facturas obtenida exitosamente')
    @facturas_ns.response(401, 'No autorizado')
    @facturas_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def get(self):
        """Obtiene todas las facturas registradas"""
        try:
            # Verificar si la tabla existe
            inspector = inspect(db.engine)
            if 'factura' not in inspector.get_table_names():
                facturas_ns.abort(500, "Tabla de facturas no existe")
            
            facturas = Factura.query.all()
            
            if not facturas:
                return [], 200
            
            facturas_serializadas = []
            for factura in facturas:
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

            return facturas_serializadas, 200

        except Exception as e:
            current_app.logger.error(f"Error en VistaPrivFacturas: {str(e)}", exc_info=True)
            facturas_ns.abort(500, "Error interno al obtener las facturas")

    @facturas_ns.doc(security='Bearer')
    @facturas_ns.expect(factura_creacion_model)
    @facturas_ns.marshal_with(factura_model, code=201)
    @facturas_ns.response(201, 'Factura creada exitosamente')
    @facturas_ns.response(400, 'Datos faltantes o inválidos')
    @facturas_ns.response(401, 'No autorizado')
    @facturas_ns.response(500, 'Error al crear factura')
    @jwt_required()
    def post(self):
        """Crea una nueva factura"""
        try:
            data = facturas_ns.payload

            # Validar que los datos requeridos estén presentes
            if not data.get("total") or not data.get("id_cliente"):
                facturas_ns.abort(400, "Faltan datos obligatorios")

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

            return nueva_factura, 201

        except Exception as e:
            db.session.rollback()
            facturas_ns.abort(500, f"Error al crear la factura: {str(e)}")

@facturas_ns.route('/<int:id_factura>')
@facturas_ns.param('id_factura', 'ID de la factura')
class VistaPrivFactura(Resource):
    @facturas_ns.doc(security='Bearer')
    @facturas_ns.marshal_with(factura_model)
    @facturas_ns.response(200, 'Factura encontrada')
    @facturas_ns.response(404, 'Factura no encontrada')
    @facturas_ns.response(401, 'No autorizado')
    @facturas_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def get(self, id_factura):
        """Obtiene una factura específica por su ID"""
        try:
            factura = Factura.query.filter_by(id_factura=id_factura).first()

            if not factura:
                facturas_ns.abort(404, "Factura no encontrada")

            factura_serializada = {
                "id_factura": factura.id_factura,
                "fecha_factura": factura.fecha_factura.isoformat() if factura.fecha_factura else None,
                "total": factura.total,
                "iva_total": factura.iva_total,
                "estado": factura.estado,
                "fecha_vencimiento": factura.fecha_vencimiento.isoformat() if factura.fecha_vencimiento else None,
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

            return factura_serializada, 200

        except Exception as e:
            current_app.logger.error(f"Error al obtener factura {id_factura}: {str(e)}")
            facturas_ns.abort(500, "Error al obtener la factura")

    @facturas_ns.doc(security='Bearer')
    @facturas_ns.expect(factura_actualizacion_model)
    @facturas_ns.marshal_with(factura_model)
    @facturas_ns.response(200, 'Factura actualizada exitosamente')
    @facturas_ns.response(400, 'Datos inválidos')
    @facturas_ns.response(401, 'No autorizado')
    @facturas_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @facturas_ns.response(404, 'Factura no encontrada')
    @facturas_ns.response(500, 'Error al actualizar factura')
    @admin_required
    @jwt_required()
    def put(self, id_factura):
        """Actualiza los datos de una factura (Requiere admin)"""
        try:
            factura = Factura.query.filter_by(id_factura=id_factura).first()

            if not factura:
                facturas_ns.abort(404, "Factura no encontrada")

            data = facturas_ns.payload
            factura.fecha_factura = data.get("fecha_factura", factura.fecha_factura)
            factura.total = data.get("total", factura.total)
            factura.iva_total = data.get("iva_total", factura.iva_total)
            factura.estado = data.get("estado", factura.estado)
            factura.fecha_vencimiento = data.get("fecha_vencimiento", factura.fecha_vencimiento)
            factura.id_cliente = data.get("id_cliente", factura.id_cliente)

            db.session.commit()

            return factura, 200
        except Exception as e:
            db.session.rollback()
            facturas_ns.abort(500, f"Error al actualizar la factura: {str(e)}")

    @facturas_ns.doc(security='Bearer')
    @facturas_ns.expect(estado_factura_model)
    @facturas_ns.marshal_with(factura_model)
    @facturas_ns.response(200, 'Estado de la factura actualizado')
    @facturas_ns.response(400, 'Estado inválido')
    @facturas_ns.response(401, 'No autorizado')
    @facturas_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @facturas_ns.response(404, 'Factura no encontrada')
    @facturas_ns.response(500, 'Error al actualizar estado')
    @admin_required
    @jwt_required()
    def patch(self, id_factura):
        """Actualiza el estado de una factura (Requiere admin)"""
        try:
            factura = Factura.query.filter_by(id_factura=id_factura).first()

            if not factura:
                facturas_ns.abort(404, "Factura no encontrada")

            nuevo_estado = facturas_ns.payload.get('estado')
            if nuevo_estado not in ['Pagada', 'Cancelada']:
                facturas_ns.abort(400, "Estado inválido, debe ser 'Pagada' o 'Cancelada'")

            factura.estado = nuevo_estado
            db.session.commit()

            return factura, 200
        except Exception as e:
            db.session.rollback()
            facturas_ns.abort(500, f"Error al actualizar el estado de la factura: {str(e)}")


# Vista para pago

@pagos_ns.route('/factura/<int:id_factura>')
@pagos_ns.param('id_factura', 'ID de la factura')
class VistaFormularioPagos(Resource):
    @pagos_ns.doc(security='Bearer')
    @pagos_ns.marshal_with(pago_model)
    @pagos_ns.response(200, 'Pago encontrado')
    @pagos_ns.response(404, 'No hay pagos registrados para esta factura')
    @pagos_ns.response(401, 'No autorizado')
    @pagos_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def get(self, id_factura):
        """Obtiene el pago asociado a una factura"""
        try:
            pago = FormularioPago.query.filter_by(id_factura=id_factura).first()

            if not pago:
                pagos_ns.abort(404, "No hay pagos registrados para esta factura")

            return pago, 200
        except Exception as e:
            pagos_ns.abort(500, f"Error al obtener la información del pago: {str(e)}")

@pagos_ns.route('/procesar')
class VistaProcesarPago(Resource):
    @pagos_ns.doc(security='Bearer')
    @pagos_ns.expect(pago_creacion_model)
    @pagos_ns.marshal_with(pago_model, code=201)
    @pagos_ns.response(201, 'Pago procesado exitosamente')
    @pagos_ns.response(400, 'Datos faltantes o inválidos')
    @pagos_ns.response(401, 'No autorizado')
    @pagos_ns.response(404, 'Factura no encontrada')
    @pagos_ns.response(500, 'Error al procesar pago')
    @jwt_required()
    def post(self):
        """Procesa un nuevo pago"""
        try:
            data = pagos_ns.payload
            
            # Validación exhaustiva
            required_fields = ["id_factura", "tipo_pago"]
            if not all(field in data for field in required_fields):
                pagos_ns.abort(400, "Faltan campos obligatorios")
                
            if data["tipo_pago"] not in ['tarjeta', 'efectivo', 'transferencia']:
                pagos_ns.abort(400, "Tipo de pago no válido")

            factura = Factura.query.get(data["id_factura"])
            if not factura:
                pagos_ns.abort(404, "Factura no encontrada")
                
            if factura.estado != "Pendiente":
                pagos_ns.abort(400, "La factura ya fue procesada")

            # Validaciones específicas para tarjeta
            if data["tipo_pago"] == "tarjeta":
                card_fields = ["titular", "numero_tarjeta", "fecha_expiracion", "codigo_seguridad"]
                if not all(field in data for field in card_fields):
                    pagos_ns.abort(400, "Faltan datos de la tarjeta")
                
                if not data["numero_tarjeta"].isdigit() or len(data["numero_tarjeta"]) != 16:
                    pagos_ns.abort(400, "Número de tarjeta no válido")
                
                try:
                    month, year = map(int, data["fecha_expiracion"].split('/'))
                    current_year = datetime.now().year % 100
                    current_month = datetime.now().month
                    
                    if (year < current_year) or (year == current_year and month < current_month):
                        pagos_ns.abort(400, "Tarjeta expirada")
                except:
                    pagos_ns.abort(400, "Fecha de expiración no válida (use formato MM/YY)")
                
                if not data["codigo_seguridad"].isdigit() or len(data["codigo_seguridad"]) not in [3, 4]:
                    pagos_ns.abort(400, "Código de seguridad no válido")
            
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
            else:
                nuevo_pago.estado_pago = "Pendiente"
                factura.estado = "Pendiente"
            
            db.session.commit()
            
            return nuevo_pago, 201
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error en VistaProcesarPago: {str(e)}", exc_info=True)
            pagos_ns.abort(500, "Error interno al procesar el pago")


# vistas para proveedor


@proveedores_ns.route('/')
class VistaAdminProveedores(Resource):
    @proveedores_ns.doc(security='Bearer')
    @proveedores_ns.marshal_list_with(proveedor_model)
    @proveedores_ns.response(200, 'Lista de proveedores obtenida exitosamente')
    @proveedores_ns.response(401, 'No autorizado')
    @proveedores_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @proveedores_ns.response(500, 'Error interno del servidor')
    @admin_required
    @jwt_required()
    def get(self):
        """Obtiene todos los proveedores registrados (Requiere admin)"""
        try:
            proveedores = Proveedor.query.all()
            return proveedores, 200
        except Exception as e:
            proveedores_ns.abort(500, f"Error al obtener los proveedores: {str(e)}")

    @proveedores_ns.doc(security='Bearer')
    @proveedores_ns.expect(proveedor_creacion_model)
    @proveedores_ns.marshal_with(proveedor_model, code=201)
    @proveedores_ns.response(201, 'Proveedor creado exitosamente')
    @proveedores_ns.response(400, 'Datos faltantes o inválidos')
    @proveedores_ns.response(401, 'No autorizado')
    @proveedores_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @proveedores_ns.response(500, 'Error al crear proveedor')
    @admin_required
    @jwt_required()
    def post(self):
        """Crea un nuevo proveedor (Requiere admin)"""
        try:
            data = proveedores_ns.payload
            
            if not all([data.get('nombre'), data.get('telefono'), data.get('correo')]):
                proveedores_ns.abort(400, "Faltan datos obligatorios")

            nuevo_proveedor = Proveedor(
                nombre=data['nombre'],
                telefono=data['telefono'],
                correo=data['correo'],
                estado=data.get('estado', 'activo')
            )

            db.session.add(nuevo_proveedor)
            db.session.commit()

            return nuevo_proveedor, 201
        except Exception as e:
            proveedores_ns.abort(500, f"Error al agregar el proveedor: {str(e)}")

@proveedores_ns.route('/<int:id_proveedor>')
@proveedores_ns.param('id_proveedor', 'ID del proveedor')
class VistaAdminProveedor(Resource):
    @proveedores_ns.doc(security='Bearer')
    @proveedores_ns.marshal_with(proveedor_model)
    @proveedores_ns.response(200, 'Proveedor encontrado')
    @proveedores_ns.response(404, 'Proveedor no encontrado')
    @proveedores_ns.response(401, 'No autorizado')
    @proveedores_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @proveedores_ns.response(500, 'Error interno del servidor')
    @admin_required
    @jwt_required()
    def get(self, id_proveedor):
        """Obtiene un proveedor específico por su ID (Requiere admin)"""
        try:
            proveedor = Proveedor.query.filter_by(id_proveedor=id_proveedor).first()
            if not proveedor:
                proveedores_ns.abort(404, "Proveedor no encontrado")
            return proveedor, 200
        except Exception as e:
            proveedores_ns.abort(500, f"Error al obtener el proveedor: {str(e)}")

    @proveedores_ns.doc(security='Bearer')
    @proveedores_ns.expect(proveedor_actualizacion_model)
    @proveedores_ns.marshal_with(proveedor_model)
    @proveedores_ns.response(200, 'Proveedor actualizado exitosamente')
    @proveedores_ns.response(400, 'Datos inválidos')
    @proveedores_ns.response(401, 'No autorizado')
    @proveedores_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @proveedores_ns.response(404, 'Proveedor no encontrado')
    @proveedores_ns.response(500, 'Error al actualizar proveedor')
    @admin_required
    @jwt_required()
    def put(self, id_proveedor):
        """Actualiza los datos de un proveedor (Requiere admin)"""
        try:
            proveedor = Proveedor.query.filter_by(id_proveedor=id_proveedor).first()
            if not proveedor:
                proveedores_ns.abort(404, "Proveedor no encontrado")

            data = proveedores_ns.payload
            proveedor.nombre = data.get('nombre', proveedor.nombre)
            proveedor.telefono = data.get('telefono', proveedor.telefono)
            proveedor.correo = data.get('correo', proveedor.correo)
            proveedor.estado = data.get('estado', proveedor.estado)

            db.session.commit()
            return proveedor, 200
        except Exception as e:
            proveedores_ns.abort(500, f"Error al actualizar el proveedor: {str(e)}")

    @proveedores_ns.doc(security='Bearer')
    @proveedores_ns.response(200, 'Proveedor desactivado exitosamente')
    @proveedores_ns.response(401, 'No autorizado')
    @proveedores_ns.response(403, 'Acceso denegado (requiere rol admin)')
    @proveedores_ns.response(404, 'Proveedor no encontrado')
    @proveedores_ns.response(500, 'Error al desactivar proveedor')
    @admin_required
    @jwt_required()
    def patch(self, id_proveedor):
        """Desactiva un proveedor (Requiere admin)"""
        try:
            proveedor = Proveedor.query.filter_by(id_proveedor=id_proveedor).first()
            if not proveedor:
                proveedores_ns.abort(404, "Proveedor no encontrado")

            proveedor.estado = "inactivo"
            db.session.commit()
            return {"mensaje": "Proveedor desactivado exitosamente"}, 200
        except Exception as e:
            proveedores_ns.abort(500, f"Error al desactivar el proveedor: {str(e)}")


# Vistas de ventas

@carrito_ns.route('/<int:id_usuario>')
@carrito_ns.param('id_usuario', 'ID del usuario')
class VistaCarrito(Resource):
    @carrito_ns.doc(security='Bearer')
    @carrito_ns.marshal_with(carrito_model)
    @carrito_ns.response(200, 'Carrito obtenido exitosamente')
    @carrito_ns.response(401, 'No autorizado')
    @carrito_ns.response(404, 'Carrito no encontrado')
    @carrito_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def get(self, id_usuario):
        """Obtiene el carrito de un usuario"""
        try:
            carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
            if not carrito:
                carrito_ns.abort(404, "Carrito no encontrado")

            productos_serializados = []
            for detalle in carrito.detalles:
                producto = detalle.producto
                if not producto:
                    continue
                    
                precio = producto.precio_descuento if producto.precio_descuento is not None else producto.precio
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
            carrito_ns.abort(500, f"Error al obtener el carrito: {str(e)}")

@carrito_ns.route('/agregar')
class VistaAgregarAlCarrito(Resource):
    @carrito_ns.doc(security='Bearer')
    @carrito_ns.expect(item_carrito_model)
    @carrito_ns.response(201, 'Producto agregado al carrito exitosamente')
    @carrito_ns.response(400, 'Datos inválidos o producto no disponible')
    @carrito_ns.response(401, 'No autorizado')
    @carrito_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def post(self):
        """Agrega un producto al carrito"""
        try:
            data = carrito_ns.payload
            id_usuario = get_jwt_identity()
            id_producto = data.get("id_producto")
            cantidad = data.get("cantidad", 1)

            producto = Producto.query.get(id_producto)
            if not producto or producto.precio is None:
                carrito_ns.abort(400, "Producto no disponible")
            
            carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
            if not carrito:
                carrito = Carrito(id_usuario=id_usuario)
                db.session.add(carrito)
                db.session.commit()

            detalle = DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito, id_producto=id_producto).first()
            if detalle:
                detalle.cantidad += cantidad
            else:
                nuevo_detalle = DetalleCarrito(
                    id_carrito=carrito.id_carrito, 
                    id_producto=id_producto, 
                    cantidad=cantidad
                )
                db.session.add(nuevo_detalle)

            db.session.commit()
            return {"mensaje": "Producto agregado al carrito exitosamente."}, 201
        except Exception as e:
            carrito_ns.abort(500, f"Error al agregar producto al carrito: {str(e)}")

@carrito_ns.route('/<int:id_carrito>/producto/<int:id_producto>')
@carrito_ns.param('id_carrito', 'ID del carrito')
@carrito_ns.param('id_producto', 'ID del producto')
class VistaProductoCarrito(Resource):
    @carrito_ns.doc(security='Bearer')
    @carrito_ns.expect(item_carrito_model)
    @carrito_ns.response(200, 'Producto modificado exitosamente')
    @carrito_ns.response(400, 'Cantidad inválida')
    @carrito_ns.response(401, 'No autorizado')
    @carrito_ns.response(404, 'Producto no encontrado en el carrito')
    @carrito_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def put(self, id_carrito, id_producto):
        """Modifica la cantidad de un producto en el carrito"""
        try:
            data = carrito_ns.payload
            nueva_cantidad = data.get("cantidad")

            if nueva_cantidad is None or nueva_cantidad < 1:
                carrito_ns.abort(400, "La cantidad debe ser mayor a 0")

            detalle = DetalleCarrito.query.filter_by(
                id_carrito=id_carrito, 
                id_producto=id_producto
            ).first()
            
            if not detalle:
                carrito_ns.abort(404, "Producto no encontrado en el carrito")

            detalle.cantidad = nueva_cantidad
            db.session.commit()
            return {"mensaje": "Producto modificado exitosamente."}, 200
        except Exception as e:
            carrito_ns.abort(500, f"Error al modificar producto: {str(e)}")

    @carrito_ns.doc(security='Bearer')
    @carrito_ns.response(200, 'Producto eliminado del carrito exitosamente')
    @carrito_ns.response(401, 'No autorizado')
    @carrito_ns.response(404, 'Producto no encontrado en el carrito')
    @carrito_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def delete(self, id_carrito, id_producto):
        """Elimina un producto del carrito"""
        try:
            detalle = DetalleCarrito.query.filter_by(
                id_carrito=id_carrito, 
                id_producto=id_producto
            ).first()
            
            if not detalle:
                carrito_ns.abort(404, "Producto no encontrado en el carrito")

            db.session.delete(detalle)
            db.session.commit()
            return {"mensaje": "Producto eliminado del carrito exitosamente."}, 200
        except Exception as e:
            carrito_ns.abort(500, f"Error al eliminar producto: {str(e)}")

@carrito_ns.route('/procesar/<int:id_usuario>')
@carrito_ns.param('id_usuario', 'ID del usuario')
class VistaProcesarCompra(Resource):
    @carrito_ns.doc(security='Bearer')
    @carrito_ns.response(200, 'Factura creada exitosamente')
    @carrito_ns.response(400, 'Carrito vacío o stock insuficiente')
    @carrito_ns.response(401, 'No autorizado')
    @carrito_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def post(self, id_usuario):
        """Procesa la compra del carrito y genera una factura"""
        try:
            carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
            if not carrito or not carrito.detalles:
                carrito_ns.abort(400, "El carrito está vacío o no existe")

            # Verificar stock antes de crear la factura
            for detalle in carrito.detalles:
                producto = detalle.producto
                if not producto or producto.stock < detalle.cantidad:
                    carrito_ns.abort(400, {
                        "mensaje": f"No hay suficiente stock para {producto.nombre if producto else 'producto desconocido'}",
                        "producto": producto.nombre if producto else None,
                        "stock_disponible": producto.stock if producto else 0,
                        "solicitado": detalle.cantidad
                    })

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
            carrito_ns.abort(500, f"Error al procesar la compra: {str(e)}")

@pagos_ns.route('/confirmar/<int:id_factura>')
@pagos_ns.param('id_factura', 'ID de la factura')
class VistaConfirmarPago(Resource):
    @pagos_ns.doc(security='Bearer')
    @pagos_ns.response(200, 'Pago confirmado exitosamente')
    @pagos_ns.response(400, 'Factura ya pagada')
    @pagos_ns.response(401, 'No autorizado')
    @pagos_ns.response(404, 'Factura no encontrada')
    @pagos_ns.response(500, 'Error interno del servidor')
    @jwt_required()
    def post(self, id_factura):
        """Confirma el pago de una factura y actualiza stock"""
        try:
            factura = Factura.query.get(id_factura)
            if not factura:
                pagos_ns.abort(404, "Factura no encontrada")
                
            if factura.estado == "Pagada":
                pagos_ns.abort(400, "La factura ya fue pagada anteriormente")

            # Obtener el carrito del usuario
            carrito = Carrito.query.filter_by(id_usuario=factura.id_cliente).first()

            # Procesar cada producto (reducir stock)
            productos_actualizados = []
            for detalle_factura in factura.detalles:
                producto = Producto.query.get(detalle_factura.id_producto)
                if producto:
                    if producto.stock < detalle_factura.cantidad:
                        pagos_ns.abort(400, {
                            "mensaje": f"Stock insuficiente para {producto.nombre}",
                            "producto": producto.nombre,
                            "stock_actual": producto.stock,
                            "solicitado": detalle_factura.cantidad
                        })
                    
                    producto.stock -= detalle_factura.cantidad
                    productos_actualizados.append({
                        "id_producto": producto.id_producto,
                        "nombre": producto.nombre,
                        "nuevo_stock": producto.stock
                    })

            # Vaciar el carrito si existe
            if carrito:
                DetalleCarrito.query.filter_by(id_carrito=carrito.id_carrito).delete()
                db.session.commit()

            # Actualizar estado de la factura
            factura.estado = "Pagada"
            factura.fecha_pago = datetime.utcnow()

            # Crear registro de pago
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
            pagos_ns.abort(500, f"Error al confirmar el pago: {str(e)}")

# Vistas para autenticacion
@auth_ns.route('/login')
class VistaLogIn(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Inicio de sesión exitoso', token_response)
    @auth_ns.response(401, 'Credenciales inválidas')
    def post(self):
        """Inicio de sesión de usuario"""
        u_email = request.json["email"]
        u_contrasena = request.json["contrasena"]
        
        usuario = Usuario.query.filter_by(email=u_email).first()  
        if usuario and usuario.verificar_contrasena(u_contrasena):
            usuario.ultimo_login = datetime.utcnow()
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

@auth_ns.route('/signup')
class VistaSignIn(Resource):
    @auth_ns.expect(signup_model)
    @auth_ns.response(201, 'Usuario creado exitosamente')
    @auth_ns.response(400, 'Email o documento ya registrado')
    @auth_ns.response(500, 'Error al crear usuario')
    def post(self):
        """Registro de nuevo usuario"""
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


# Vistas de configuracion

@config_ns.route('/tipo-documento')
class VistaPrivTipoDoc(Resource):
    @config_ns.marshal_list_with(tipo_doc_model)
    @config_ns.response(200, 'Lista de tipos de documento')
    @config_ns.response(500, 'Error al obtener tipos de documento')
    def get(self):
        """Obtener todos los tipos de documento"""
        try:
            tipo_docs = TipoDoc.query.all()
            return tipo_docs
        except Exception as e:
            return {"mensaje": f"Error al obtener los tipos de documento: {str(e)}"}, 500

    @config_ns.expect(tipo_doc_model)
    @config_ns.response(201, 'Tipo de documento creado')
    @config_ns.response(400, 'Datos faltantes')
    @config_ns.response(500, 'Error al crear tipo de documento')
    @jwt_required()
    def post(self):
        """Crear nuevo tipo de documento"""
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
                "tipo_doc": nuevo_tipo_doc
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar el tipo de documento: {str(e)}"}, 500

@config_ns.route('/tipo-documento/<int:id_TipoDocumento>')
class VistaPrivTipoDocs(Resource):
    @config_ns.expect(tipo_doc_model)
    @config_ns.response(200, 'Tipo de documento actualizado')
    @config_ns.response(404, 'Tipo de documento no encontrado')
    @config_ns.response(500, 'Error al actualizar')
    @jwt_required()
    def put(self, id_TipoDocumento):
        """Actualizar tipo de documento"""
        try:
            tipo_doc = TipoDoc.query.filter_by(id_TipoDocumento=id_TipoDocumento).first()
            if not tipo_doc:
                return {"mensaje": "Tipo de documento no encontrado."}, 404

            tipo_doc.Nombre = request.json.get("Nombre", tipo_doc.Nombre)
            tipo_doc.Descripcion = request.json.get("Descripcion", tipo_doc.Descripcion)

            db.session.commit()

            return {
                "mensaje": "Tipo de documento actualizado exitosamente.",
                "tipo_doc": tipo_doc
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el tipo de documento: {str(e)}"}, 500

@config_ns.route('/roles')
class VistaPrivRol(Resource):
    @config_ns.marshal_list_with(rol_model)
    @config_ns.response(200, 'Lista de roles')
    @config_ns.response(500, 'Error al obtener roles')
    @jwt_required()
    def get(self):
        """Obtener todos los roles"""
        try:
            roles = Rol.query.all()
            return roles
        except Exception as e:
            return {"mensaje": f"Error al obtener los roles: {str(e)}"}, 500

    @config_ns.expect(rol_model)
    @config_ns.response(201, 'Rol creado')
    @config_ns.response(400, 'Datos faltantes')
    @config_ns.response(403, 'Requiere rol admin')
    @config_ns.response(500, 'Error al crear rol')
    @admin_required
    @jwt_required()
    def post(self):
        """Crear nuevo rol (Requiere admin)"""
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
                "rol": nuevo_rol
            }, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar el rol: {str(e)}"}, 500

@config_ns.route('/roles/<int:id_Rol>')
class VistaPrivRoles(Resource):
    @config_ns.expect(rol_model)
    @config_ns.response(200, 'Rol actualizado')
    @config_ns.response(404, 'Rol no encontrado')
    @config_ns.response(403, 'Requiere rol admin')
    @config_ns.response(500, 'Error al actualizar')
    @admin_required
    @jwt_required()
    def put(self, id_Rol):
        """Actualizar rol (Requiere admin)"""
        try:
            rol = Rol.query.filter_by(id_Rol=id_Rol).first()
            if not rol:
                return {"mensaje": "Rol no encontrado."}, 404

            rol.Nombre = request.json.get("Nombre", rol.Nombre)
            rol.Descripcion = request.json.get("Descripcion", rol.Descripcion)

            db.session.commit()

            return {
                "mensaje": "Rol actualizado exitosamente.",
                "rol": rol
            }, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar el rol: {str(e)}"}, 500

# Vistas de categorias
@categorias_ns.route('/')
class VistaPrivCategoria(Resource):
    @categorias_ns.marshal_list_with(categoria_model)
    @categorias_ns.response(200, 'Lista de categorías')
    @categorias_ns.response(500, 'Error al obtener categorías')
    def get(self):
        """Obtener todas las categorías"""
        try:
            categorias = Categoria.query.all()
            return categorias
        except Exception as e:
            return {"mensaje": f"Error al obtener las categorías: {str(e)}"}, 500

    @categorias_ns.expect(categoria_creacion_model)
    @categorias_ns.marshal_with(categoria_model)
    @categorias_ns.response(201, 'Categoría creada')
    @categorias_ns.response(400, 'Datos faltantes')
    @categorias_ns.response(403, 'Requiere rol admin')
    @categorias_ns.response(500, 'Error al crear categoría')
    @admin_required
    @jwt_required()
    def post(self):
        """Crear nueva categoría (Requiere admin)"""
        try:
            datos = request.form
            if not datos.get("nombre"):
                return {"mensaje": "El nombre es obligatorio."}, 400

            imagen_url = None
            if 'imagen' in request.files and request.files['imagen'].filename:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                imagen_url = upload_result.get("secure_url")

            nueva_categoria = Categoria(
                nombre=datos["nombre"],
                descripcion=datos.get("descripcion"),
                imagen=imagen_url
            )

            db.session.add(nueva_categoria)
            db.session.commit()

            return nueva_categoria, 201
        except Exception as e:
            return {"mensaje": f"Error al agregar la categoría: {str(e)}"}, 500

@categorias_ns.route('/<int:id_categoria>')
class VistaPrivCategorias(Resource):
    @categorias_ns.marshal_with(categoria_model)
    @categorias_ns.response(200, 'Categoría encontrada')
    @categorias_ns.response(404, 'Categoría no encontrada')
    @categorias_ns.response(500, 'Error al obtener categoría')
    def get(self, id_categoria):
        """Obtener una categoría específica"""
        try:
            categoria = Categoria.query.get(id_categoria)
            if not categoria:
                return {"mensaje": "Categoría no encontrada"}, 404
            return categoria
        except Exception as e:
            return {"mensaje": f"Error al obtener categoría: {str(e)}"}, 500

    @categorias_ns.expect(categoria_creacion_model)
    @categorias_ns.marshal_with(categoria_model)
    @categorias_ns.response(200, 'Categoría actualizada')
    @categorias_ns.response(400, 'Datos inválidos')
    @categorias_ns.response(403, 'Requiere rol admin')
    @categorias_ns.response(404, 'Categoría no encontrada')
    @categorias_ns.response(500, 'Error al actualizar')
    @admin_required
    @jwt_required()
    def put(self, id_categoria):
        """Actualizar categoría (Requiere admin)"""
        try:
            categoria = Categoria.query.filter_by(id_categoria=id_categoria).first()
            if not categoria:
                return {"mensaje": "Categoría no encontrada."}, 404

            datos = request.form
            categoria.nombre = datos.get("nombre", categoria.nombre)
            categoria.descripcion = datos.get("descripcion", categoria.descripcion)

            if 'imagen' in request.files and request.files['imagen'].filename:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                categoria.imagen = upload_result.get("secure_url")
            elif 'imagen_url' in datos and datos['imagen_url'].strip():
                categoria.imagen = datos["imagen_url"]

            db.session.commit()

            return categoria, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar la categoría: {str(e)}"}, 500

# Vistas de marcas

@marcas_ns.route('/')
class VistaMarcas(Resource):
    @marcas_ns.marshal_list_with(marca_model)
    @marcas_ns.response(200, 'Lista de marcas')
    @marcas_ns.response(500, 'Error al obtener marcas')
    def get(self):
        """Obtener todas las marcas"""
        try:
            marcas = Marca.query.all()
            return marcas
        except Exception as e:
            return {"mensaje": f"Error al obtener las marcas: {str(e)}"}, 500

    @marcas_ns.expect(marca_creacion_model)
    @marcas_ns.marshal_with(marca_model)
    @marcas_ns.response(201, 'Marca creada')
    @marcas_ns.response(400, 'Datos faltantes o inválidos')
    @marcas_ns.response(403, 'Requiere rol admin')
    @marcas_ns.response(500, 'Error al crear marca')
    @admin_required
    @jwt_required()
    def post(self):
        """Crear nueva marca (Requiere admin)"""
        try:
            datos = request.form
            if not datos.get("nombre") or not datos.get("id_proveedor"):
                return {"mensaje": "Faltan datos obligatorios."}, 400

            imagen_url = None
            if 'imagen' in request.files and request.files['imagen'].filename:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                imagen_url = upload_result.get("secure_url")

            nueva_marca = Marca(
                nombre=datos["nombre"],
                estado=datos.get("estado", "Activo"),
                id_proveedor=datos["id_proveedor"],
                imagen=imagen_url
            )

            db.session.add(nueva_marca)
            db.session.commit()

            return nueva_marca, 201
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error: La marca ya existe o el proveedor no es válido."}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al agregar la marca: {str(e)}"}, 500

@marcas_ns.route('/<int:id_marca>')
class VistaMarca(Resource):
    @marcas_ns.marshal_with(marca_model)
    @marcas_ns.response(200, 'Marca encontrada')
    @marcas_ns.response(404, 'Marca no encontrada')
    @marcas_ns.response(500, 'Error al obtener marca')
    def get(self, id_marca):
        """Obtener una marca específica"""
        try:
            marca = Marca.query.get(id_marca)
            if not marca:
                return {"mensaje": "Marca no encontrada."}, 404
            return marca
        except Exception as e:
            return {"mensaje": f"Error al obtener la marca: {str(e)}"}, 500

    @marcas_ns.expect(marca_creacion_model)
    @marcas_ns.marshal_with(marca_model)
    @marcas_ns.response(200, 'Marca actualizada')
    @marcas_ns.response(400, 'Datos inválidos')
    @marcas_ns.response(403, 'Requiere rol admin')
    @marcas_ns.response(404, 'Marca no encontrada')
    @marcas_ns.response(500, 'Error al actualizar')
    @admin_required
    @jwt_required()
    def put(self, id_marca):
        """Actualizar marca (Requiere admin)"""
        try:
            marca = Marca.query.get(id_marca)
            if not marca:
                return {"mensaje": "Marca no encontrada."}, 404

            datos = request.form
            marca.nombre = datos.get("nombre", marca.nombre)
            marca.id_proveedor = datos.get("id_proveedor", marca.id_proveedor)
            marca.estado = datos.get("estado", marca.estado)

            if 'imagen' in request.files and request.files['imagen'].filename:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                marca.imagen = upload_result.get("secure_url")
            elif 'imagen_url' in datos and datos['imagen_url'].strip():
                marca.imagen = datos["imagen_url"]

            db.session.commit()

            return marca, 200
        except Exception as e:
            return {"mensaje": f"Error al actualizar la marca: {str(e)}"}, 500

    @marcas_ns.response(200, 'Estado actualizado')
    @marcas_ns.response(400, 'Estado inválido')
    @marcas_ns.response(403, 'Requiere rol admin')
    @marcas_ns.response(404, 'Marca no encontrada')
    @marcas_ns.response(500, 'Error al actualizar estado')
    @admin_required
    @jwt_required()
    def patch(self, id_marca):
        """Actualizar estado de marca (Requiere admin)"""
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
        
# Vista de animales

@animales_ns.route('/')
class VistaAnimales(Resource):
    @animales_ns.marshal_list_with(animal_model)
    @animales_ns.response(200, 'Lista de animales')
    @animales_ns.response(500, 'Error al obtener animales')
    def get(self):
        """Obtener todos los animales"""
        try:
            animales = Animal.query.all()
            return animales
        except Exception as e:
            return {"mensaje": f"Error al obtener los animales: {str(e)}"}, 500

    @animales_ns.expect(animal_creacion_model)
    @animales_ns.marshal_with(animal_model)
    @animales_ns.response(201, 'Animal creado')
    @animales_ns.response(400, 'Datos faltantes o inválidos')
    @animales_ns.response(403, 'Requiere rol admin')
    @animales_ns.response(500, 'Error al crear animal')
    @admin_required
    @jwt_required()
    def post(self):
        """Crear nuevo animal (Requiere admin)"""
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
                estado=datos.get("estado", "Activo")
            )

            db.session.add(nuevo_animal)
            db.session.commit()

            return nuevo_animal, 201
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error: El nombre del animal ya existe."}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al agregar el animal: {str(e)}"}, 500

@animales_ns.route('/<int:id_animal>')
class VistaAnimal(Resource):
    @animales_ns.marshal_with(animal_model)
    @animales_ns.response(200, 'Animal encontrado')
    @animales_ns.response(404, 'Animal no encontrado')
    @animales_ns.response(500, 'Error al obtener animal')
    def get(self, id_animal):
        """Obtener un animal específico"""
        try:
            animal = Animal.query.get(id_animal)
            if not animal:
                return {"mensaje": "Animal no encontrado."}, 404
            return animal
        except Exception as e:
            return {"mensaje": f"Error al obtener el animal: {str(e)}"}, 500

    @animales_ns.expect(animal_creacion_model)
    @animales_ns.marshal_with(animal_model)
    @animales_ns.response(200, 'Animal actualizado')
    @animales_ns.response(400, 'Datos inválidos')
    @animales_ns.response(403, 'Requiere rol admin')
    @animales_ns.response(404, 'Animal no encontrado')
    @animales_ns.response(500, 'Error al actualizar')
    @admin_required
    @jwt_required()
    def put(self, id_animal):
        """Actualizar animal (Requiere admin)"""
        try:
            animal = Animal.query.get(id_animal)
            if not animal:
                return {"mensaje": "Animal no encontrado."}, 404

            datos = request.form
            if 'nombre' in datos:
                animal.nombre = datos['nombre']

            if 'imagen' in request.files and request.files['imagen'].filename:
                imagen = request.files['imagen']
                upload_result = cloudinary.uploader.upload(imagen)
                animal.imagen = upload_result.get('secure_url')
            elif 'imagen_url' in datos and datos['imagen_url'].strip():
                animal.imagen = datos['imagen_url']

            db.session.commit()

            return animal, 200
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error: El nombre del animal ya existe."}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al actualizar el animal: {str(e)}"}, 500

    @animales_ns.response(200, 'Estado actualizado')
    @animales_ns.response(400, 'Estado inválido')
    @animales_ns.response(403, 'Requiere rol admin')
    @animales_ns.response(404, 'Animal no encontrado')
    @animales_ns.response(500, 'Error al actualizar estado')
    @admin_required
    @jwt_required()
    def patch(self, id_animal):
        """Actualizar estado de animal (Requiere admin)"""
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
                "animal": animal
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al actualizar el estado del animal: {str(e)}"}, 500

# Vista de descuentos

@descuentos_ns.route('/')
class VistaDescuentos(Resource):
    @descuentos_ns.marshal_list_with(descuento_model)
    @descuentos_ns.response(200, 'Lista de descuentos')
    @descuentos_ns.response(500, 'Error al obtener descuentos')
    def get(self):
        """Obtener todos los descuentos"""
        try:
            descuentos = Descuento.query.options(db.joinedload(Descuento.producto)).all()
            return descuentos
        except Exception as e:
            return {"mensaje": f"Error al obtener los descuentos: {str(e)}"}, 500

    @descuentos_ns.expect(descuento_creacion_model)
    @descuentos_ns.marshal_with(descuento_model)
    @descuentos_ns.response(201, 'Descuento creado')
    @descuentos_ns.response(400, 'Datos faltantes o inválidos')
    @descuentos_ns.response(403, 'Requiere rol admin')
    @descuentos_ns.response(500, 'Error al crear descuento')
    @admin_required
    @jwt_required()
    def post(self):
        """Crear nuevo descuento (Requiere admin)"""
        try:
            data = request.get_json()
            if not data:
                return {"mensaje": "No se proporcionaron datos"}, 400
                
            if not data.get("id_producto"):
                return {"mensaje": "El id_producto es obligatorio"}, 400
            if not data.get("porcentaje_descuento"):
                return {"mensaje": "El porcentaje es obligatorio"}, 400

            producto = Producto.query.get(data["id_producto"])
            if not producto:
                return {"mensaje": "El producto especificado no existe"}, 400

            nuevo_descuento = Descuento(
                id_producto=data["id_producto"],
                porcentaje_descuento=data["porcentaje_descuento"],
                fecha_inicio=data.get("fecha_inicio"),
                fecha_fin=data.get("fecha_fin")
            )

            db.session.add(nuevo_descuento)
            db.session.commit()

            return nuevo_descuento, 201
            
        except IntegrityError as e:
            db.session.rollback()
            return {"mensaje": f"Error de integridad: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error inesperado al agregar descuento: {str(e)}"}, 500

@descuentos_ns.route('/<int:id_descuento>')
class VistaDescuento(Resource):
    @descuentos_ns.marshal_with(descuento_model)
    @descuentos_ns.response(200, 'Descuento encontrado')
    @descuentos_ns.response(404, 'Descuento no encontrado')
    @descuentos_ns.response(500, 'Error al obtener descuento')
    def get(self, id_descuento):
        """Obtener un descuento específico"""
        try:
            descuento = Descuento.query.get(id_descuento)
            if not descuento:
                return {"mensaje": "Descuento no encontrado."}, 404
            return descuento
        except Exception as e:
            return {"mensaje": f"Error al obtener el descuento: {str(e)}"}, 500

    @descuentos_ns.expect(descuento_creacion_model)
    @descuentos_ns.marshal_with(descuento_model)
    @descuentos_ns.response(200, 'Descuento actualizado')
    @descuentos_ns.response(400, 'Datos inválidos')
    @descuentos_ns.response(403, 'Requiere rol admin')
    @descuentos_ns.response(404, 'Descuento no encontrado')
    @descuentos_ns.response(500, 'Error al actualizar')
    @admin_required
    @jwt_required()
    def put(self, id_descuento):
        """Actualizar descuento (Requiere admin)"""
        try:
            descuento = Descuento.query.get(id_descuento)
            if not descuento:
                return {"mensaje": "Descuento no encontrado."}, 404

            data = request.json
            
            if 'id_producto' in data:
                producto = Producto.query.get(data['id_producto'])
                if not producto:
                    return {"mensaje": "El producto especificado no existe"}, 400
            
            descuento.id_producto = data.get("id_producto", descuento.id_producto)
            descuento.porcentaje_descuento = data.get("porcentaje_descuento", descuento.porcentaje_descuento)
            descuento.fecha_inicio = data.get("fecha_inicio", descuento.fecha_inicio)
            descuento.fecha_fin = data.get("fecha_fin", descuento.fecha_fin)

            db.session.commit()

            return descuento, 200
        except Exception as e:
            db.session.rollback()
            return {"mensaje": f"Error al actualizar el descuento: {str(e)}"}, 500

    @descuentos_ns.response(200, 'Descuento eliminado')
    @descuentos_ns.response(403, 'Requiere rol admin')
    @descuentos_ns.response(404, 'Descuento no encontrado')
    @descuentos_ns.response(500, 'Error al eliminar')
    @admin_required
    @jwt_required()
    def delete(self, id_descuento):
        """Eliminar descuento (Requiere admin)"""
        try:
            descuento = Descuento.query.get(id_descuento)
            if not descuento:
                return {"mensaje": "Descuento no encontrado."}, 404

            db.session.delete(descuento)
            db.session.commit()

            return {"mensaje": "Descuento eliminado exitosamente."}, 200
        except Exception as e:
            return {"mensaje": f"Error al eliminar el descuento: {str(e)}"}, 500

# vista de reportes

@reportes_ns.route('/ventas')
class VistaReporteVentas(Resource):
    @reportes_ns.marshal_list_with(reporte_ventas_model)
    @reportes_ns.response(200, 'Reporte generado')
    @reportes_ns.response(403, 'Requiere rol admin')
    @reportes_ns.response(500, 'Error generando reporte')
    @admin_required
    def get(self):
        """Reporte de ventas por fecha (Requiere admin)"""
        try:
            start_date = request.args.get('start', default=(datetime.now() - timedelta(days=30)).isoformat())
            end_date = request.args.get('end', default=datetime.now().isoformat())
            
            ventas = db.session.query(
                func.date(Factura.fecha_factura).label('fecha'),
                func.sum(Factura.total).label('total')
            ).filter(
                Factura.fecha_factura.between(start_date, end_date),
                Factura.estado == 'Pagada'
            ).group_by(func.date(Factura.fecha_factura)).all()

            return ventas
            
        except Exception as e:
            return {'mensaje': f'Error generando reporte: {str(e)}'}, 500

@reportes_ns.route('/productos')
class VistaReporteProductos(Resource):
    @reportes_ns.marshal_with(reporte_productos_model)
    @reportes_ns.response(200, 'Reporte generado')
    @reportes_ns.response(403, 'Requiere rol admin')
    @reportes_ns.response(500, 'Error generando reporte')
    @admin_required
    def get(self):
        """Reporte de productos (Requiere admin)"""
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

            return {
                'top_productos': [{
                    'nombre': p.nombre,
                    'vendidos': p.vendidos,
                    'ingresos': float(p.ingresos) if p.ingresos else 0
                } for p in productos_top],
                'stock_bajo': [{
                    'id_producto': p.id_producto,
                    'nombre': p.nombre,
                    'stock': p.stock,
                    'precio': float(p.precio) if p.precio else 0
                } for p in stock_bajo]
            }
        except Exception as e:
            reportes_ns.abort(500, f'Error generando reporte: {str(e)}')

@reportes_ns.route('/usuarios')
class VistaReporteUsuarios(Resource):
    @reportes_ns.marshal_with(reporte_usuarios_model)
    @reportes_ns.response(200, 'Reporte generado')
    @reportes_ns.response(403, 'Requiere rol admin')
    @reportes_ns.response(500, 'Error generando reporte')
    @admin_required
    def get(self):
        """Reporte de usuarios (Requiere admin)"""
        try:
            usuarios_activos = Usuario.query.filter_by(estado='Activo').count()
            nuevos_clientes = Usuario.query.filter(
                Usuario.id_rol == 2,
                Usuario.ultimo_login >= (datetime.now() - timedelta(days=30))
            ).count()

            return {
                'usuarios_activos': usuarios_activos,
                'nuevos_clientes': nuevos_clientes
            }
        except Exception as e:
            return {'mensaje': f'Error generando reporte: {str(e)}'}, 500