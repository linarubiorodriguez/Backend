from flask import Blueprint
from flask_restx import Api
from flaskr.vistas.vistas import (
    VistaSignIn, VistaLogIn, VistaPrivCliente, VistaPrivClientes,
    VistaAdminEmpleados, VistaAdminEmpleado, VistaPrivProducto,
    VistaPrivProductos, VistaPrivFactura, VistaPrivFacturas,
    VistaAdminProveedor, VistaAdminProveedores, VistaCarrito, 
    VistaDetalleFactura, VistaProductoCarrito, VistaProcesarCompra, 
    VistaAgregarAlCarrito, VistaPrivCategoria, VistaPrivTipoDoc, 
    VistaPrivCategorias, VistaFormularioPagos, VistaPrivTipoDocs, 
    VistaHistorialCompras, VistaCancelarPago, VistaMarcas, VistaMarca,  
    VistaReporteVentas, VistaReporteProductos, VistaReporteUsuarios, 
    VistaDescuentos, VistaDescuento, VistaAnimales, VistaAnimal, 
    VistaProcesarPago
)

def create_test_blueprints():
    """Crea todos los blueprints para testing con prefijo /test"""
    
    # 1. Blueprint de Autenticación
    auth_bp = Blueprint('test_auth', __name__)
    auth_api = Api(auth_bp, prefix='/test/auth')
    auth_api.add_resource(VistaLogIn, '/login')
    auth_api.add_resource(VistaSignIn, '/signin')
    
    # 2. Blueprint de Usuarios y Roles
    users_bp = Blueprint('test_users', __name__)
    users_api = Api(users_bp, prefix='/test/users')
    users_api.add_resource(VistaPrivTipoDoc, '/tipo_doc')
    users_api.add_resource(VistaPrivTipoDocs, '/tipo_doc/<int:id_TipoDocumento>')
    users_api.add_resource(VistaPrivClientes, '/clientes')
    users_api.add_resource(VistaPrivCliente, '/clientes/<int:id_usuario>')
    users_api.add_resource(VistaAdminEmpleados, '/empleados')
    users_api.add_resource(VistaAdminEmpleado, '/empleados/<int:id_usuario>')
    
    # 3. Blueprint de Productos
    products_bp = Blueprint('test_products', __name__)
    products_api = Api(products_bp, prefix='/test/products')
    products_api.add_resource(VistaPrivProductos, '/')
    products_api.add_resource(VistaPrivProducto, '/<int:id_producto>')
    products_api.add_resource(VistaPrivCategoria, '/categorias')
    products_api.add_resource(VistaPrivCategorias, '/categorias/<int:id_categoria>')
    products_api.add_resource(VistaMarcas, '/marcas')
    products_api.add_resource(VistaMarca, '/marcas/<int:id_marca>')
    products_api.add_resource(VistaDescuentos, '/descuentos')
    products_api.add_resource(VistaDescuento, '/descuentos/<int:id_descuento>')
    products_api.add_resource(VistaAnimales, '/animales')
    products_api.add_resource(VistaAnimal, '/animales/<int:id_animal>')
    
    # 4. Blueprint de Ventas y Facturación
    sales_bp = Blueprint('test_sales', __name__)
    sales_api = Api(sales_bp, prefix='/test/sales')
    sales_api.add_resource(VistaPrivFacturas, '/facturas')
    sales_api.add_resource(VistaPrivFactura, '/facturas/<int:id_factura>')
    sales_api.add_resource(VistaDetalleFactura, '/facturas/detalle/<int:id_factura>')
    sales_api.add_resource(VistaFormularioPagos, '/pagos/<int:id_formulario>')
    sales_api.add_resource(VistaProcesarPago, '/pagos/procesar')
    sales_api.add_resource(VistaHistorialCompras, '/compras/historial')
    sales_api.add_resource(VistaCancelarPago, '/pagos/cancelar/<int:id_factura>')
    sales_api.add_resource(VistaReporteVentas, '/reportes/ventas')
    sales_api.add_resource(VistaReporteProductos, '/reportes/productos')
    sales_api.add_resource(VistaReporteUsuarios, '/reportes/usuarios')
    
    # 5. Blueprint de Carrito
    cart_bp = Blueprint('test_cart', __name__)
    cart_api = Api(cart_bp, prefix='/test/cart')
    cart_api.add_resource(VistaAgregarAlCarrito, '/agregar')
    cart_api.add_resource(VistaCarrito, '/<int:id_usuario>')
    cart_api.add_resource(VistaProductoCarrito, '/producto/<int:id_carrito>/<int:id_producto>')
    cart_api.add_resource(VistaProcesarCompra, '/procesar/<int:id_usuario>')
    
    # 6. Blueprint de Proveedores
    suppliers_bp = Blueprint('test_suppliers', __name__)
    suppliers_api = Api(suppliers_bp, prefix='/test/suppliers')
    suppliers_api.add_resource(VistaAdminProveedores, '/')
    suppliers_api.add_resource(VistaAdminProveedor, '/<int:id_proveedor>')
    
    return [auth_bp, users_bp, products_bp, sales_bp, cart_bp, suppliers_bp]