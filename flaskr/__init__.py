from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .modelos import db, Usuario
from flask_jwt_extended import JWTManager  # Importar JWTManager
from werkzeug.security import generate_password_hash
from functools import wraps
from datetime import datetime
from flask import current_app
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def create_app(config_name):
    app = Flask(__name__)
    USER_DB = 'root'
    PASS_DB = ''
    URL_DB = 'localhost'
    NAME_DB = 'bdelesconditeanimal'
    FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

    app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = '23989232klEl232Escondite2323'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hora

    db.init_app(app)
    Migrate(app, db)
    
    # Configurar JWT
    jwt = JWTManager(app)
    
    # Configurar callback para verificar claims del token
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        usuario = Usuario.query.get(identity)
        return {
            'rol': usuario.id_rol,
            'email': usuario.email
        }
    
    # Configurar callback para token expirado
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            'mensaje': 'El token ha expirado',
            'error': 'token_expired'
        }, 401

        # Agregar esta función dentro de create_app
    def verificar_clientes_inactivos():
        with app.app_context():
            limite = datetime.utcnow() - timedelta(days=7)
            clientes_inactivos = Usuario.query.filter(
                Usuario.id_rol == 2,  # Solo clientes
                Usuario.ultimo_login < limite,
                Usuario.estado == "Activo"
            ).all()
            
            for cliente in clientes_inactivos:
                cliente.estado = "Inactivo"
                current_app.logger.info(f"Cliente {cliente.email} marcado como inactivo")
            
            db.session.commit()
            return f"{len(clientes_inactivos)} clientes marcados como inactivos"

    # Configurar el scheduler solo si no estamos en modo testing
    if app.config.get('TESTING') != True:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            func=verificar_clientes_inactivos,
            trigger='interval',
            days=1,  # Ejecutar diariamente
            next_run_time=datetime.now() + timedelta(seconds=30)  # Primera ejecución 30 segs después del inicio
        )
        scheduler.start()

    with app.app_context():
        db.create_all()
        insertar_datos_iniciales() 
        crear_superadmin()

    return app

# Decorador para verificar rol de administrador
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] != 1:  # 1 es el id del rol Administrador
            return {'mensaje': 'Acceso no autorizado'}, 403
        return fn(*args, **kwargs)
    return wrapper

# Decorador para verificar rol de empleado o admin
def staff_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] not in [1, 3]:  # 1=Admin, 3=Empleado
            return {'mensaje': 'Acceso no autorizado'}, 403
        return fn(*args, **kwargs)
    return wrapper


def insertar_datos_iniciales():
    from .modelos import TipoDoc, Rol, Categoria, Animal, Usuario, Proveedor, Marca, Producto, db

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
            db.session.add(Categoria(id_categoria=cat["id"], nombre=cat["nombre"], descripcion=cat["descripcion"], imagen=cat["imagen"]))

    # Animales
    animales = [
        {"id": 1, "nombre": "Gato", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743612220/m5tiluc3fpyujvap7hnx.jpg"},
        {"id": 2, "nombre": "Perro", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743542374/gzs5svkdfbsy22kys33g.avif"},
        {"id": 3, "nombre": "Conejos", "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743542800/i89nzssblhlyjh1fc2pa.avif"}
    ]
    for animal in animales:
        if not Animal.query.get(animal["id"]):
            nuevo_animal = Animal(
                id_animal=animal["id"], 
                nombre=animal["nombre"], 
                imagen=animal["imagen"] 
            )
            db.session.add(nuevo_animal)

    usuarios = [
        {"id_usuario": 2, "nombres": "Carlos", "apellidos": "Martínez", "telefono": "3111111111", "email": "carlos@gmail.com", "num_documento": "2222222222", "tipo_doc": 2, "direccion": "Calle 456", "id_rol": 2, "contrasena": "Carlos123"},
        {"id_usuario": 3, "nombres": "María", "apellidos": "Gómez", "telefono": "3222222222", "email": "maria@gmail.com", "num_documento": "3333333333", "tipo_doc": 1, "direccion": "Carrera 789", "id_rol": 2, "contrasena": "Maria456"},
        {"id_usuario": 4, "nombres": "Javier", "apellidos": "López", "telefono": "3333333333", "email": "javier@gmail.com", "num_documento": "4444444444", "tipo_doc": 3, "direccion": "Av. Siempre Viva", "id_rol": 3, "contrasena": "Javier789"},
        {"id_usuario": 5, "nombres": "Luisa", "apellidos": "Fernández", "telefono": "3444444444", "email": "luisa@gmail.com", "num_documento": "5555555555", "tipo_doc": 2, "direccion": "Calle Luna", "id_rol": 3, "contrasena": "Luisa159"},
        {"id_usuario": 6, "nombres": "Andrés", "apellidos": "Pérez", "telefono": "3555555555", "email": "andres@gmail.com", "num_documento": "6666666666", "tipo_doc": 4, "direccion": "Calle Sol", "id_rol": 2, "contrasena": "Andres753"},
        {"id_usuario": 7, "nombres": "Sofía", "apellidos": "Ramírez", "telefono": "3666666666", "email": "sofia@gmail.com", "num_documento": "7777777777", "tipo_doc": 1, "direccion": "Calle Estrella", "id_rol": 3, "contrasena": "Sofia852"},
        {"id_usuario": 8, "nombres": "Fernando", "apellidos": "García", "telefono": "3777777777", "email": "fernando@gmail.com", "num_documento": "8888888888", "tipo_doc": 3, "direccion": "Avenida Central", "id_rol": 2, "contrasena": "Fernando963"},
        {"id_usuario": 9, "nombres": "Elena", "apellidos": "Castro", "telefono": "3888888888", "email": "elena@gmail.com", "num_documento": "9999999999", "tipo_doc": 2, "direccion": "Carrera Norte", "id_rol": 3, "contrasena": "Elena741"},
        {"id_usuario": 10, "nombres": "David", "apellidos": "Torres", "telefono": "3999999999", "email": "david@gmail.com", "num_documento": "1010101010", "tipo_doc": 1, "direccion": "Calle Sur", "id_rol": 2, "contrasena": "David852"},
        {"id_usuario": 11, "nombres": "Ana", "apellidos": "Vargas", "telefono": "4000000000", "email": "ana@gmail.com", "num_documento": "1111111112", "tipo_doc": 4, "direccion": "Avenida Oeste", "id_rol": 3, "contrasena": "Ana369"},
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
        {"nombre": "Whiskas", "id_proveedor": 1, "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743781699/fjawzkxyzjdi2ul26jcm.png"},
        {"nombre": "Purina", "id_proveedor": 2, "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743781822/y0lusfbfb4xwywao52k4.png"},
        {"nombre": "Pedigree", "id_proveedor": 3, "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743781881/xbmdxnjiwsyvtax5ofgm.jpg"},
        {"nombre": "Royal Canin", "id_proveedor": 4, "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743781929/zzfi1egafo0iwprl2lb1.svg"},
        {"nombre": "Eukanuba", "id_proveedor": 5, "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743782022/kvayev3eepxybxyyvdi4.png"},
        {"nombre": "Hill's Science Diet", "id_proveedor": 6, "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743782058/zlnizvrvnlmpne2x5iq2.jpg"}
    ]

    for marca in marcas:
        if not Marca.query.filter_by(nombre=marca["nombre"]).first():
            db.session.add(Marca(
                nombre=marca["nombre"], 
                id_proveedor=marca["id_proveedor"],
                imagen=marca["imagen"] 
            ))

    productos = [
        {
            "nombre": "Comida Gatos Whiskas Adulto 1kg",
            "descripcion": "Alimento balanceado para gatos adultos. Rico en proteínas y con sabor a carne.",
            "precio": 10000.00,
            "stock": 50,
            "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1744085164/m6kjatsjge2pxeabuhkp.webp",
            "id_categoria": 4, 
            "id_marca": 1,      
            "id_animal": 1     
        },
        {
            "nombre": "Comida Perros Pedigree Adulto 3kg",
            "descripcion": "Alimento completo para perros adultos. Ayuda a la digestión y fortalece el sistema inmune.",
            "precio": 10000.00,
            "stock": 30,
            "imagen": "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1744085236/bpqbmowqpakwcpnzlg84.webp",
            "id_categoria": 4, 
            "id_marca": 3,      
            "id_animal": 2     
        }
    ]

    for p in productos:
        if not Producto.query.filter_by(nombre=p["nombre"]).first():
            nuevo_producto = Producto(
                nombre=p["nombre"],
                descripcion=p["descripcion"],
                precio=p["precio"],
                stock=p["stock"],
                imagen=p["imagen"],
                id_categoria=p["id_categoria"],
                id_marca=p["id_marca"],
                id_animal=p["id_animal"],
                fecha_inicio_descuento=None,
                fecha_fin_descuento=None
            )
            db.session.add(nuevo_producto)

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
            email='paola01@gmail.com',
            num_documento='1111111111',
            tipo_doc=2,
            direccion='Calle 123',
            estado='Activo',
            id_rol=1
        )
        nuevo_admin.contrasena = 'El1234Escondite5656Animal42224235'  # Usar el setter
        db.session.add(nuevo_admin)
        db.session.commit()

