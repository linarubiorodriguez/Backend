from flaskr import create_app
from flask_restx import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flaskr.vistas import (
    VistaSignIn, VistaLogIn, VistaPrivCliente, VistaPrivClientes,
    VistaAdminEmpleados, VistaAdminEmpleado, VistaPrivProducto,
    VistaPrivProductos, VistaPrivFactura, VistaPrivFacturas,
    VistaAdminProveedor,
    VistaAdminProveedores, VistaCarrito,
    VistaProductoCarrito, VistaProcesarCompra, VistaAgregarAlCarrito, VistaPrivCategoria,
    VistaPrivTipoDoc, VistaPrivRol,  VistaPrivCategorias, VistaPrivRoles, VistaFormularioPagos,
    VistaPrivTipoDocs,
    VistaMarcas, VistaMarca, VistaDescuentos, VistaDescuento, VistaAnimales, VistaAnimal, VistaProcesarPago, VistaConfirmarPago
)

app = create_app('default')
CORS(app)

# Configuración mínima de Swagger
api = Api(
    app,
    version='1.0',
    title='API El Escondite Animal',
    description='Documentación automática de la API',
    doc='/swagger',  # Ruta para la UI de Swagger
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Usar: 'Bearer <JWT>'"
        }
    },
    security='Bearer Auth'
)


# Autenticación
api.add_resource(VistaLogIn, '/login')  
api.add_resource(VistaSignIn, '/signin') 

# Rutas para TipoDoc
api.add_resource(VistaPrivTipoDoc, '/tipo_doc') 
api.add_resource(VistaPrivTipoDocs, '/tipo_doc/<int:id_TipoDocumento>')  

# Rutas para Rol
api.add_resource(VistaPrivRol, '/rol') 
api.add_resource(VistaPrivRoles, '/rol/<int:id_Rol>')  


# Rutas para el formulario de pago
api.add_resource(VistaFormularioPagos, '/FormPago/<int:id_formulario>')  


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

api.add_resource(VistaAgregarAlCarrito, '/Carrito/agregar')
api.add_resource(VistaCarrito, '/Carrito/<int:id_usuario>')
api.add_resource(VistaProductoCarrito, '/Carrito/producto/<int:id_carrito>/<int:id_producto>')
api.add_resource(VistaConfirmarPago, '/confirmar-pago/<int:id_factura>')
api.add_resource(VistaProcesarCompra, '/Carrito/procesar/<int:id_usuario>')
# Gestión de marcas
api.add_resource(VistaMarcas, '/PrivMarcas')
api.add_resource(VistaMarca, '/PrivMarca/<int:id_marca>')

# Gestión de descuentos
api.add_resource(VistaDescuentos, '/descuentosProd')
api.add_resource(VistaDescuento, '/descuentosProd/<int:id_descuento>')

# Gestión de animales
api.add_resource(VistaAnimales, '/animalesProd')
api.add_resource(VistaAnimal, '/animalesProd/<int:id_animal>')

api.add_resource(VistaProcesarPago, '/api/pagos/procesar')

# Inicializar JWT
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)