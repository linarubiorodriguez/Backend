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

    from .modelos import TipoDoc, Rol, Categoria, MetodoPago, Animal, db

    tipos_documento = [
        {"id": 1, "nombre": "TI", "descripcion": "Tarjeta de identidad"},
        {"id": 2, "nombre": "CC", "descripcion": "Cédula de ciudadanía"},
        {"id": 3, "nombre": "CE", "descripcion": "Cédula de extranjería"},
        {"id": 4, "nombre": "TE", "descripcion": "Tarjeta de extranjería"}
    ]
    for tipo in tipos_documento:
        if not TipoDoc.query.get(tipo["id"]):
            nuevo_tipo = TipoDoc(id_TipoDocumento=tipo["id"], Nombre=tipo["nombre"], Descripcion=tipo["descripcion"])
            db.session.add(nuevo_tipo)

    roles = [
        {"id": 1, "nombre": "Administrador", "descripcion": "Administrador del sistema"},
        {"id": 2, "nombre": "Cliente", "descripcion": "Usuario del sistema"},
        {"id": 3, "nombre": "Empleado", "descripcion": "Registrado en el sistema"}
    ]
    for rol in roles:
        if not Rol.query.get(rol["id"]):
            nuevo_rol = Rol(id_Rol=rol["id"], Nombre=rol["nombre"], Descripcion=rol["descripcion"])
            db.session.add(nuevo_rol)

    categorias = [
        {"id": 1, "nombre": "Camas", "descripcion": "Comodidad para tus mascotas.", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1740162149/camas_w31iw0.png"},
        {"id": 2, "nombre": "Juguetes", "descripcion": "Entretenimiento para tus mascotas.", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1740156258/xfamhkvn2kzklrxbcbgf.png"},
        {"id": 3, "nombre": "Accesorios", "descripcion": "Estética para tus mascotas.", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1740156259/fiuz63szmeexuvlm6s6u.png"},
        {"id": 4, "nombre": "Comida", "descripcion": "Alimento para tus mascotas.", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1740156258/ixxmvuvctk6jtx5qj1gv.png"}
    ]
    
    for cat in categorias:
            categoria_existente = Categoria.query.filter_by(id_categoria=cat["id"]).first()
            if not categoria_existente:
                nueva_categoria = Categoria(
                    id_categoria=cat["id"],
                    nombre=cat["nombre"],
                    descripcion=cat["descripcion"],
                    imagen=cat["imagen"] 
                )
                db.session.add(nueva_categoria)

    metodos_pago = [
        {"id": 1, "nombre": "Paypal"},
        {"id": 2, "nombre": "VISA"},
        {"id": 3, "nombre": "Mastercard"},
        {"id": 4, "nombre": "Nequi"}
    ]

    for metodo in metodos_pago:
        if not MetodoPago.query.get(metodo["id"]):
            nuevo_metodo = MetodoPago(id_pago=metodo["id"], nombre=metodo["nombre"])
            db.session.add(nuevo_metodo)

    animales = [
        {"id": 1, "nombre": "Gatos"},
        {"id": 2, "nombre": "Perros"}
    ]

    for animal in animales:
        if not Animal.query.get(animal["id"]):
            nuevo_animal = Animal(id_animal=animal["id"], nombre=animal["nombre"])
            db.session.add(nuevo_animal)


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

