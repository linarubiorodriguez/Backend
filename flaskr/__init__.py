from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .modelos import db
# __init__.py de flaskr
from .modelos import db, Usuario, Rol, Producto, Categoria, Factura, DetalleFactura, Proveedor, Carrito, DetalleCarrito
from werkzeug.security import generate_password_hash

def create_app(config_name):
    app = Flask(__name__)
    USER_DB = 'root'
    PASS_DB = ''
    URL_DB = 'localhost'
    NAME_DB = 'bdelesconditeanimal'
    FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

    app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta_segura'

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()
        insertar_datos_iniciales() 
        crear_superadmin()

    return app


def insertar_datos_iniciales():
    from .modelos import TipoDoc, Rol, Categoria, Animal, Usuario, Proveedor, Marca, db

    # Tipos de Documento
    tipos_documento = [
        {"id": 1, "nombre": "TI", "descripcion": "Tarjeta de identidad"},
        {"id": 2, "nombre": "CC", "descripcion": "Cédula de ciudadanía"},
        {"id": 3, "nombre": "CE", "descripcion": "Cédula de extranjería"},
        {"id": 4, "nombre": "TE", "descripcion": "Tarjeta de extranjería"}
    ]
    for tipo in tipos_documento:
        if not TipoDoc.query.get(tipo["id"]):
            db.session.add(TipoDoc(id_TipoDocumento=tipo["id"], Nombre=tipo["nombre"], Descripcion=tipo["descripcion"]))

    # Roles
    roles = [
        {"id": 1, "nombre": "Administrador", "descripcion": "Administrador del sistema"},
        {"id": 2, "nombre": "Cliente", "descripcion": "Usuario del sistema"},
        {"id": 3, "nombre": "Empleado", "descripcion": "Registrado en el sistema"}
    ]
    for rol in roles:
        if not Rol.query.get(rol["id"]):
            db.session.add(Rol(id_Rol=rol["id"], Nombre=rol["nombre"], Descripcion=rol["descripcion"]))

    # Categorías
    categorias = [
        {"id": 1, "nombre": "Camas", "descripcion": "Comodidad para tus mascotas."},
        {"id": 2, "nombre": "Juguetes", "descripcion": "Entretenimiento para tus mascotas."},
        {"id": 3, "nombre": "Accesorios", "descripcion": "Estética para tus mascotas."},
        {"id": 4, "nombre": "Comida", "descripcion": "Alimento para tus mascotas."}
    ]
    for cat in categorias:
        if not Categoria.query.get(cat["id"]):
            db.session.add(Categoria(id_categoria=cat["id"], nombre=cat["nombre"], descripcion=cat["descripcion"]))

    # Animales
    animales = [
        {"id": 1, "nombre": "Gato"},
        {"id": 2, "nombre": "Perro"},
        {"id": 3, "nombre": "Conejo"}
    ]
    for animal in animales:
        if not Animal.query.get(animal["id"]):
            db.session.add(Animal(id_animal=animal["id"], nombre=animal["nombre"]))

    # Usuarios (sin admins)
    usuarios = [
        {"nombres": "Carlos", "apellidos": "Gómez", "telefono": "3123456789", "email": "carlos@example.com",
         "num_documento": "12343533331", "tipo_doc": 2, "direccion": "Av. Siempre Viva 123", "id_rol": 2},
        {"nombres": "Andrea", "apellidos": "Martínez", "telefono": "3109876543", "email": "andrea@example.com",
         "num_documento": "1234353232", "tipo_doc": 1, "direccion": "Calle Luna 45", "id_rol": 3},
        {"nombres": "Luis", "apellidos": "Fernández", "telefono": "3201234567", "email": "luis@example.com",
         "num_documento": "123435121333", "tipo_doc": 3, "direccion": "Cra. del Sol 67", "id_rol": 2},
        {"nombres": "Sofía", "apellidos": "Ramírez", "telefono": "3112233445", "email": "sofia@example.com",
         "num_documento": "12343523234", "tipo_doc": 2, "direccion": "Cll Primavera 99", "id_rol": 3},
        {"nombres": "Daniel", "apellidos": "López", "telefono": "3145678901", "email": "daniel@example.com",
         "num_documento": "123435345435", "tipo_doc": 1, "direccion": "Calle Rosas 111", "id_rol": 2},
        {"nombres": "María", "apellidos": "García", "telefono": "3156789012", "email": "maria@example.com",
         "num_documento": "12343533126", "tipo_doc": 3, "direccion": "Cra. Flores 222", "id_rol": 3},
        {"nombres": "Pedro", "apellidos": "Torres", "telefono": "3167890123", "email": "pedro@example.com",
         "num_documento": "12343533467", "tipo_doc": 2, "direccion": "Av. Palmeras 333", "id_rol": 2},
        {"nombres": "Laura", "apellidos": "Vargas", "telefono": "3178901234", "email": "laura@example.com",
         "num_documento": "1234353323428", "tipo_doc": 1, "direccion": "Calle Orquídea 444", "id_rol": 3},
        {"nombres": "Javier", "apellidos": "Rojas", "telefono": "3189012345", "email": "javier@example.com",
         "num_documento": "1234353356569", "tipo_doc": 3, "direccion": "Cra. Sauce 555", "id_rol": 2},
        {"nombres": "Ana", "apelli32423": "Castro", "telefono": "3190123456", "email": "ana@example.com",
         "num_documento": "1000000010", "tipo_doc": 2, "direccion": "Av. Tulipanes 666", "id_rol": 3}
    ]
    for user in usuarios:
        if not Usuario.query.filter_by(email=user["email"]).first():
            nuevo_usuario = Usuario(
                nombres=user["nombres"],
                apellidos=user["apellidos"],
                telefono=user["telefono"],
                email=user["email"],
                num_documento=user["num_documento"],
                tipo_doc=user["tipo_doc"],
                direccion=user["direccion"],
                estado="Activo",
                id_rol=user["id_rol"]
            )
            nuevo_usuario.contrasena = "Contraseña123"
            db.session.add(nuevo_usuario)

    proveedores = [
        {"nombre": "Alimentos Felices S.A.", "telefono": "3001234567", "correo": "contacto@alimentosfelices.com", "estado": "Activo"},
        {"nombre": "NutriPet Ltda.", "telefono": "3012345678", "correo": "ventas@nutripet.com", "estado": "Activo"},
        {"nombre": "PetLife Distribuciones", "telefono": "3023456789", "correo": "info@petlifedistribuciones.com", "estado": "Activo"},
        {"nombre": "Mascota Premium", "telefono": "3034567890", "correo": "contacto@mascotapremium.com", "estado": "Activo"},
        {"nombre": "Animal Care", "telefono": "3045678901", "correo": "info@animalcare.com", "estado": "Activo"},
        {"nombre": "VitalPet Supplies", "telefono": "3056789012", "correo": "soporte@vitalpet.com", "estado": "Activo"}
    ]
    for prov in proveedores:
        if not Proveedor.query.filter_by(nombre=prov["nombre"]).first():
            db.session.add(Proveedor(nombre=prov["nombre"], telefono=prov["telefono"], correo=prov["correo"], estado=prov["estado"]))

    # Marcas
    marcas = [
        {"nombre": "Whiskas", "id_proveedor": 1},
        {"nombre": "Purina", "id_proveedor": 2},
        {"nombre": "Pedigree", "id_proveedor": 3},
        {"nombre": "Royal Canin", "id_proveedor": 4},
        {"nombre": "Eukanuba", "id_proveedor": 5},
        {"nombre": "Hill's Science Diet", "id_proveedor": 6}
    ]
    for marca in marcas:
        if not Marca.query.filter_by(nombre=marca["nombre"]).first():
            db.session.add(Marca(nombre=marca["nombre"], id_proveedor=marca["id_proveedor"]))

    db.session.commit()



def crear_superadmin():
    from .modelos import Usuario, db
    superadmin = Usuario.query.filter_by(id_usuario=1).first()
    if not superadmin:
        nuevo_admin = Usuario(
            id_usuario=1,
            nombres='Paola',
            apellidos='Sanchez',
            telefono='3133334',
            email='paola01@example.com',
            num_documento='1111111111',
            tipo_doc=2,
            direccion='Calle 123',
            estado='Activo',
            id_rol=1
        )
        nuevo_admin.contrasena = 'El1234Escondite5656Animal42224235'  # Usar el setter
        db.session.add(nuevo_admin)
        db.session.commit()

