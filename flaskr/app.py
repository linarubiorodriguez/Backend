from flaskr import create_app
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flaskr.vistas import (
    VistaSignIn, VistaLogIn, VistaPrivCliente, VistaPrivClientes,
    VistaAdminEmpleados, VistaAdminEmpleado, VistaPrivProducto,
    VistaPrivProductos, VistaPrivFactura, VistaPrivFacturas,
    VistaAdminProveedor,
    VistaAdminProveedores, VistaCarrito,
    VistaProductoCarrito, VistaProcesarCompra, VistaAgregarAlCarrito, VistaPrivCategoria,
    VistaPrivTipoDoc, VistaPrivRol, VistaPrivMetodoPago,  VistaPrivCategorias, VistaPrivMetodoPagos, VistaPrivRoles,
    VistaPrivTipoDocs
)


app = create_app('default')
CORS(app)

api = Api(app)

# Autenticación
api.add_resource(VistaLogIn, '/login')  
api.add_resource(VistaSignIn, '/signin') 

# Rutas para TipoDoc
api.add_resource(VistaPrivTipoDoc, '/tipo_doc') 
api.add_resource(VistaPrivTipoDocs, '/tipo_doc/<int:id_TipoDocumento>')  

# Rutas para Rol
api.add_resource(VistaPrivRol, '/rol') 
api.add_resource(VistaPrivRoles, '/rol/<int:id_Rol>')  

# Rutas para MetodoPago
api.add_resource(VistaPrivMetodoPago, '/metodo_pago')  
api.add_resource(VistaPrivMetodoPagos, '/metodo_pago/<int:id_pago>')

# Rutas para Categoria
api.add_resource(VistaPrivCategoria, '/categoria')
api.add_resource(VistaPrivCategorias, '/categoria/<int:id_categoria>') 

# Gestión de clientes
api.add_resource(VistaPrivClientes, '/Priv')
api.add_resource(VistaPrivCliente, '/Priv/<int:id_usuario>')

# Gestión de empleados
api.add_resource(VistaAdminEmpleados, '/adminPrivEm')
api.add_resource(VistaAdminEmpleado, '/adminPrivEm/<int:id_usuario>')

# Gestión de productos
api.add_resource(VistaPrivProductos, '/PrivProd')
api.add_resource(VistaPrivProducto, '/PrivProd/<int:id_producto>')

# Gestión de facturas
api.add_resource(VistaPrivFacturas, '/PrivFactura')
api.add_resource(VistaPrivFactura, '/PrivFactura/<int:id_factura>')

# Gestión de proveedores
api.add_resource(VistaAdminProveedores, '/adminProveedor')
api.add_resource(VistaAdminProveedor, '/adminProveedor/<int:id_proveedor>')

# Gestión del carrito
api.add_resource(VistaCarrito, '/Carrito/<int:id_usuario>')
api.add_resource(VistaProductoCarrito, '/Compra/<int:id_usuario>')
api.add_resource(VistaProcesarCompra, '/ProductoCarrito/<int:id_carrito>/<int:id_producto>')

# Inicializar JWT
jwt = JWTManager(app)
