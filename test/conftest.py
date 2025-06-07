from datetime import datetime
import pytest
import os
from flaskr import create_app
from flaskr.modelos import db, Usuario, Factura, DetalleFactura, Rol, TipoDoc, Categoria, Marca, Animal, Proveedor
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from flaskr.modelos.modelos import Descuento, DetalleCarrito, FormularioPago, Producto
from test.test_blueprints import create_test_blueprints
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('TEST_DB_USER')}:{os.getenv('TEST_DB_PASSWORD')}@\{os.getenv('TEST_DB_HOST')}/{os.getenv('TEST_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('TEST_JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = False
    PROPAGATE_EXCEPTIONS = True
    
@pytest.fixture(scope='session')
def app():
    """Fixture de aplicación para pruebas con blueprints de testing"""
    app = create_app(TestingConfig)
    
    # Registrar blueprints solo para testing
    for bp in create_test_blueprints():
        app.register_blueprint(bp)
    
    with app.app_context():
        # Configuración de la base de datos
        db.drop_all()
        db.create_all()
        _insertar_datos_minimos()
        
        yield app
        
        # Limpieza final
        db.session.remove()
        db.drop_all()

def _insertar_datos_minimos():
    """Inserta datos esenciales para pruebas"""

    # Roles
    roles = [
        Rol(id_rol=1, Nombre="Administrador", Descripcion="Admin"),
        Rol(id_rol=2, Nombre="Cliente", Descripcion="Cliente"),
        Rol(id_rol=3, Nombre="Empleado", Descripcion="Empleado")
    ]
    
    # Tipos de documento
    tipos_doc = [
        TipoDoc(id_tipodocumento=1, Nombre="CC", Descripcion="Cédula"),
        TipoDoc(id_tipodocumento=2, Nombre="TI", Descripcion="Tarjeta")
    ]
    
    # Proveedor
    proveedor = Proveedor(
        id_proveedor=1, 
        nombre="Proveedor Test", 
        telefono="123456789", 
        correo="proveedor@test.com",
        estado="Activo"
    )
    
    # Categoría
    categoria = Categoria(
        id_categoria=1, 
        nombre="Test Cat", 
        descripcion="Categoría de prueba",
        imagen="test.jpg"
    )
    
    # Marca
    marca = Marca(
        id_marca=1, 
        nombre="Test Marca", 
        id_proveedor=1, 
        estado="Activo",
        imagen="marca.jpg"
    )
    
    # Animal
    animal = Animal(
        id_animal=1, 
        nombre="Test Animal", 
        imagen="test.jpg",
        estado="Activo"
    )
    
    # Usuario admin
    admin = Usuario(
        id_usuario=1,
        nombres="Admin",
        apellidos="Test",
        email="admin@test.com",
        num_documento="123456789",
        tipo_doc=1,
        id_rol=1,
        estado="Activo",
        direccion="Calle 123",
        contrasena_hash=generate_password_hash("admin123")
    )

    # Añadir todos a la sesión
    for obj in [*roles, *tipos_doc, proveedor, categoria, marca, animal, admin]:
        db.session.merge(obj)
    
    db.session.commit()

@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()

@pytest.fixture
def headers(user_token):
    """Headers con autenticación de usuario normal"""
    return {
        'Authorization': f'Bearer {user_token}',
        'Content-Type': 'application/json'
    }

@pytest.fixture
def admin_headers(admin_token):
    """Headers con autenticación de admin"""
    return {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

@pytest.fixture
def admin_token(app):
    """Token de administrador"""
    with app.app_context():
        admin = Usuario.query.get(1)
        token = create_access_token(identity=str(admin.id_usuario))
        yield token

@pytest.fixture
def user_token(app):
    """Token de usuario normal"""
    with app.app_context():
        user = Usuario(
            id_usuario=2,
            nombres="Usuario",
            apellidos="Test",
            email="user@test.com",
            num_documento="987654321",
            tipo_doc=1,
            id_rol=2,
            estado="Activo",
            direccion="Calle 123",
            contrasena_hash=generate_password_hash("user123")
        )
        db.session.add(user)
        db.session.commit()
        
        token = create_access_token(identity=str(user.id_usuario))
        yield token

@pytest.fixture
def test_product(app, test_categoria, test_marca, test_animal):
    with app.app_context():
        producto = Producto(
            nombre="Producto Test",
            descripcion="Descripción test",
            precio=10000,
            stock=50,
            id_categoria=test_categoria.id_categoria,
            id_marca=test_marca.id_marca,
            id_animal=test_animal.id_animal,
            estado="Activo",
            imagen="producto.jpg"
        )
        db.session.add(producto)
        db.session.commit()
        db.session.refresh(producto)
        
        yield producto
        
        # Primero eliminar dependencias del producto
        Descuento.query.filter_by(id_producto=producto.id_producto).delete()
        DetalleCarrito.query.filter_by(id_producto=producto.id_producto).delete()
        DetalleFactura.query.filter_by(id_producto=producto.id_producto).delete()
        
        # Luego eliminar el producto
        db.session.delete(producto)
        db.session.commit()

@pytest.fixture
def test_categoria(app):
    with app.app_context():
        cat = Categoria(
            nombre="Categoria Test",
            descripcion="Descripción test",
            imagen="categoria.jpg"
        )
        db.session.add(cat)
        db.session.commit()
        db.session.refresh(cat)
        yield cat
        
        # Primero eliminar productos asociados
        Producto.query.filter_by(id_categoria=cat.id_categoria).delete()
        db.session.delete(cat)
        db.session.commit()

@pytest.fixture
def test_marca(app, test_proveedor):
    with app.app_context():
        marca = Marca(
            nombre="Marca Test",
            id_proveedor=test_proveedor.id_proveedor,
            estado="Activo",
            imagen="marca.jpg"
        )
        db.session.add(marca)
        db.session.commit()
        db.session.refresh(marca)
        yield marca
        
        # Primero eliminar productos asociados
        Producto.query.filter_by(id_marca=marca.id_marca).delete()
        db.session.delete(marca)
        db.session.commit()

@pytest.fixture
def test_animal(app):
    with app.app_context():
        animal = Animal(
            nombre="Animal Test",
            imagen="animal.jpg",
            estado="Activo"
        )
        db.session.add(animal)
        db.session.commit()
        db.session.refresh(animal)
        yield animal
        
        # Primero eliminar productos asociados
        Producto.query.filter_by(id_animal=animal.id_animal).delete()
        db.session.delete(animal)
        db.session.commit()

@pytest.fixture
def test_proveedor(app):
    with app.app_context():
        prov = Proveedor(
            nombre="Proveedor Test",
            telefono="123456789",
            correo="proveedor@test.com",
            estado="Activo"
        )
        db.session.add(prov)
        db.session.commit()
        db.session.refresh(prov)
        
        yield prov
        
        # PRIMERO eliminar las marcas asociadas
        Marca.query.filter_by(id_proveedor=prov.id_proveedor).delete()
        # LUEGO eliminar el proveedor
        db.session.delete(prov)
        db.session.commit()

@pytest.fixture
def test_factura(app, user_token):
    with app.app_context():
        fact = Factura(
            total=100000,
            iva_total=16000,
            estado="Pendiente",
            id_cliente=2,
            metodo_pago="tarjeta",
            referencia_pago="TEST123"
        )
        db.session.add(fact)
        db.session.commit()
        db.session.refresh(fact)
        
        yield fact
        
        # Primero eliminar registros dependientes
        FormularioPago.query.filter_by(id_factura=fact.id_factura).delete()
        DetalleFactura.query.filter_by(id_factura=fact.id_factura).delete()
        db.session.delete(fact)
        db.session.commit()


@pytest.fixture(autouse=True)
def setup_db(app):
    """Configuración inicial de la base de datos para pruebas"""
    with app.app_context():
        db.create_all()
        _insertar_datos_minimos()
        yield
        db.session.remove()
        db.drop_all()