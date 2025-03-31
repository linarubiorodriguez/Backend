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

    categorias = [
        {"id": 1, "nombre": "Camas", "descripcion": "Comodidad para tus mascotas.", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1740162149/camas_w31iw0.png"},
        {"id": 2, "nombre": "Juguetes", "descripcion": "Entretenimiento para tus mascotas.", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1740156258/xfamhkvn2kzklrxbcbgf.png"},
        {"id": 3, "nombre": "Accesorios", "descripcion": "Estética para tus mascotas.", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1740156259/fiuz63szmeexuvlm6s6u.png"},
        {"id": 4, "nombre": "Comida", "descripcion": "Alimento para tus mascotas.", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1740156258/ixxmvuvctk6jtx5qj1gv.png"}
    ]
    for cat in categorias:
        if not Categoria.query.get(cat["id"]):
            db.session.add(Categoria(id_categoria=cat["id"], nombre=cat["nombre"], descripcion=cat["descripcion"]))

    # Animales
    animales = [
        {"id": 1, "nombre": "Gatos", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743383469/r3rtvevdgp7bf4tsthzz.jpg"},
        {"id": 2, "nombre": "Perros", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743383524/ohpwe0ctjdwa6o3nvukw.jpg"},
        {"id": 3, "nombre": "Conejos", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743383533/ufssmdmu6u9pm2nr5lij.jpg"}
    ]
    for animal in animales:
        if not Animal.query.get(animal["id"]):
            nuevo_animal = Animal(
                id_animal=animal["id"], 
                nombre=animal["nombre"], 
                imagen=animal["imagen"]  # <-- Aquí agregamos la imagen
            )
            db.session.add(nuevo_animal)

    usuarios = [
        {"id_usuario": 2, "nombres": "Carlos", "apellidos": "Martínez", "telefono": "3111111111", "email": "carlos@example.com", "num_documento": "2222222222", "tipo_doc": 2, "direccion": "Calle 456", "id_rol": 2, "contrasena": "Carlos123"},
        {"id_usuario": 3, "nombres": "María", "apellidos": "Gómez", "telefono": "3222222222", "email": "maria@example.com", "num_documento": "3333333333", "tipo_doc": 1, "direccion": "Carrera 789", "id_rol": 2, "contrasena": "Maria456"},
        {"id_usuario": 4, "nombres": "Javier", "apellidos": "López", "telefono": "3333333333", "email": "javier@example.com", "num_documento": "4444444444", "tipo_doc": 3, "direccion": "Av. Siempre Viva", "id_rol": 3, "contrasena": "Javier789"},
        {"id_usuario": 5, "nombres": "Luisa", "apellidos": "Fernández", "telefono": "3444444444", "email": "luisa@example.com", "num_documento": "5555555555", "tipo_doc": 2, "direccion": "Calle Luna", "id_rol": 3, "contrasena": "Luisa159"},
        {"id_usuario": 6, "nombres": "Andrés", "apellidos": "Pérez", "telefono": "3555555555", "email": "andres@example.com", "num_documento": "6666666666", "tipo_doc": 4, "direccion": "Calle Sol", "id_rol": 2, "contrasena": "Andres753"},
        {"id_usuario": 7, "nombres": "Sofía", "apellidos": "Ramírez", "telefono": "3666666666", "email": "sofia@example.com", "num_documento": "7777777777", "tipo_doc": 1, "direccion": "Calle Estrella", "id_rol": 3, "contrasena": "Sofia852"},
        {"id_usuario": 8, "nombres": "Fernando", "apellidos": "García", "telefono": "3777777777", "email": "fernando@example.com", "num_documento": "8888888888", "tipo_doc": 3, "direccion": "Avenida Central", "id_rol": 2, "contrasena": "Fernando963"},
        {"id_usuario": 9, "nombres": "Elena", "apellidos": "Castro", "telefono": "3888888888", "email": "elena@example.com", "num_documento": "9999999999", "tipo_doc": 2, "direccion": "Carrera Norte", "id_rol": 3, "contrasena": "Elena741"},
        {"id_usuario": 10, "nombres": "David", "apellidos": "Torres", "telefono": "3999999999", "email": "david@example.com", "num_documento": "1010101010", "tipo_doc": 1, "direccion": "Calle Sur", "id_rol": 2, "contrasena": "David852"},
        {"id_usuario": 11, "nombres": "Ana", "apellidos": "Vargas", "telefono": "4000000000", "email": "ana@example.com", "num_documento": "1111111112", "tipo_doc": 4, "direccion": "Avenida Oeste", "id_rol": 3, "contrasena": "Ana369"},
    ]

    for user in usuarios:
        if not Usuario.query.get(user["id_usuario"]):
            nuevo_usuario = Usuario(
                id_usuario=user["id_usuario"],
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
            nuevo_usuario.contrasena = user["contrasena"]
            db.session.add(nuevo_usuario)

    db.session.commit()

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

