from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class TipoDoc(db.Model):
    __tablename__ = 'tipo_doc'
    id_TipoDocumento = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Descripcion = db.Column(db.String(255))

class Rol(db.Model):
    __tablename__ = 'rol'
    id_Rol = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Descripcion = db.Column(db.String(255))

class MetodoPago(db.Model):
    __tablename__ = 'metodo_pago'
    id_pago = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255))

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    num_documento = db.Column(db.String(50), unique=True, nullable=False)
    tipo_doc = db.Column(db.Integer, db.ForeignKey('tipo_doc.id_TipoDocumento'), nullable=False)
    direccion = db.Column(db.String(50))
    contrasena_hash = db.Column(db.String(128))
    estado = db.Column(db.String(50), default="Activo", nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id_Rol'), nullable=False)

    tipo_documento = db.relationship('TipoDoc', backref='usuarios')
    rol = db.relationship('Rol', backref='usuarios')

    @property
    def contrasena(self):
        raise AttributeError("La contraseña no es un atributo legible.")
    
    @contrasena.setter
    
    def contrasena(self, contrasena):
        self.contrasena_hash = generate_password_hash(contrasena, method='pbkdf2:sha256')

    def verificar_contrasena(self, contrasena):
        resultado = check_password_hash(self.contrasena_hash, contrasena)
        return resultado

    def tiene_rol(self, rol_nombre):
        return self.rol and self.rol.Nombre == rol_nombre
    
    def esta_activo(self):
        return self.estado == "Activo"

# Clase Proveedor
class Proveedor(db.Model):
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    estado = db.Column(db.String(50))

# Clase Producto
class Producto(db.Model):
    __tablename__ = 'producto'
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(255))
    estado = db.Column(db.String(50), default="Disponible")

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    categoria = db.relationship('Categoria', backref='productos')

class Factura(db.Model):
    __tablename__ = 'factura'
    id_factura = db.Column(db.Integer, primary_key=True)
    fecha_factura = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    iva_total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default="Pendiente")
    fecha_vencimiento = db.Column(db.DateTime, nullable=False)

    id_cliente = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    cliente = db.relationship('Usuario', backref='facturas')

    id_metodo_pago = db.Column(db.Integer, db.ForeignKey('metodo_pago.id_pago'), nullable=False)
    metodo_pago = db.relationship('MetodoPago', backref='facturas')

# Modelo DetalleFactura
class DetalleFactura(db.Model):
    id_detalle = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    id_factura = db.Column(db.Integer, db.ForeignKey('factura.id_factura'))
    factura = db.relationship('Factura', backref='detalles')

    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'))
    producto = db.relationship('Producto', backref='detalles')



class Carrito(db.Model):
    id_carrito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    productos = db.relationship('DetalleCarrito', backref='carrito', lazy=True)

class DetalleCarrito(db.Model):
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_carrito = db.Column(db.Integer, db.ForeignKey('carrito.id_carrito'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)


class EnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.name if value else None

    def _deserialize(self, value, attr, data, **kwargs):
        return self.enum[value]

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class TipoDocSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class MetodoPagoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MetodoPago
        include_relationships = True
        load_instance = True

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        load_instance = True

class ProveedorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proveedor
        include_relationship = True
        load_instance = True


class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        include_relationship = True
        load_instance = True

class FacturaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Factura
        include_relationship = True
        load_instance = True

class DetalleFacturaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DetalleFactura
        include_relationship = True
        load_instance = True