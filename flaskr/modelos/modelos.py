from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
import enum
from datetime import datetime
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


class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255))
    imagen = db.Column(db.String(255))  


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
    ultimo_login = db.Column(db.DateTime, nullable=True)  

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

    def verificar_inactividad(self):
        if self.ultimo_login and self.id_rol == 2:  # Solo para clientes (rol 2)
            dias_inactividad = (datetime.utcnow() - self.ultimo_login).days
            if dias_inactividad >= 7 and self.estado == "Activo":
                self.estado = "Inactivo"
                db.session.commit()
                return True
        return False
    
    def esta_inactivo(self):
        if self.ultimo_login and self.id_rol == 2:
            return (datetime.utcnow() - self.ultimo_login).days >= 7
        return False


class Proveedor(db.Model):
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    estado = db.Column(db.String(50))

class Marca(db.Model):
    __tablename__ = 'marca'
    id_marca = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), default="Activo", nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id_proveedor'), nullable=False)
    imagen = db.Column(db.String(255))  
    
    proveedor = db.relationship('Proveedor', backref='marcas')

class Producto(db.Model):
    __tablename__ = 'producto'
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False)
    precio_descuento = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(255))
    estado = db.Column(db.String(50), default="Disponible")
    fecha_inicio_descuento = db.Column(db.DateTime)
    fecha_fin_descuento = db.Column(db.DateTime)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    categoria = db.relationship('Categoria', backref='productos')

    id_marca = db.Column(db.Integer, db.ForeignKey('marca.id_marca'), nullable=False)
    marca = db.relationship('Marca', backref='productos')

    id_animal = db.Column(db.Integer, db.ForeignKey('animal.id_animal'), nullable=False)
    animal = db.relationship('Animal', backref='productos')

    # Relación corregida con descuentos
    descuentos = db.relationship('Descuento', backref='producto', lazy=True)
    
    @property
    def descuento_activo(self):
        from datetime import datetime
        ahora = datetime.utcnow()
        descuento_activo = Descuento.query.filter(
            Descuento.id_producto == self.id_producto,
            Descuento.fecha_inicio <= ahora,
            Descuento.fecha_fin >= ahora
        ).first()
        return descuento_activo
    
    @property
    def precio_descuento(self):
        descuento = self.descuento_activo
        if descuento:
            return self.precio * (1 - descuento.porcentaje_descuento / 100)
        return None
    
class Animal(db.Model):
    __tablename__ = 'animal'
    id_animal = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(255))
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    estado = db.Column(db.String(50), default="Activo", nullable=False)
    
class Factura(db.Model):
    __tablename__ = 'factura'
    id_factura = db.Column(db.Integer, primary_key=True)
    fecha_factura = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    total = db.Column(db.Float, nullable=True)  
    iva_total = db.Column(db.Float, nullable=True)  
    estado = db.Column(db.String(50), default="Pendiente", nullable=False)  
    fecha_vencimiento = db.Column(db.DateTime, nullable=True) 

    id_cliente = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    cliente = db.relationship('Usuario', backref='facturas')


class DetalleFactura(db.Model):
    id_detalle = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    id_factura = db.Column(db.Integer, db.ForeignKey('factura.id_factura'))
    factura = db.relationship('Factura', backref='detalles')

    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'))
    producto = db.relationship('Producto', backref='detalles')


class Carrito(db.Model):
    __tablename__ = 'carrito'
    id_carrito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    detalles = db.relationship('DetalleCarrito', backref='carrito', lazy=True, cascade="all, delete-orphan")

class DetalleCarrito(db.Model):
    __tablename__ = 'detalle_carrito'
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_carrito = db.Column(db.Integer, db.ForeignKey('carrito.id_carrito'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    
    producto = db.relationship('Producto')

class Descuento(db.Model):
    __tablename__ = 'descuento'
    id_descuento = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    porcentaje_descuento = db.Column(db.Float, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)

class FormularioPago(db.Model):
    __tablename__ = 'formulario_pago'
    id_formulario = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('factura.id_factura'), nullable=False)
    tipo_pago = db.Column(db.String(50), nullable=False)  
    titular = db.Column(db.String(100), nullable=True)  
    numero_tarjeta = db.Column(db.String(16), nullable=True)  
    fecha_expiracion = db.Column(db.String(7), nullable=True)  
    codigo_seguridad = db.Column(db.String(4), nullable=True)  
    estado_pago = db.Column(db.String(50), default="Pendiente", nullable=False)  
    referencia_pago = db.Column(db.String(50), unique=True, nullable=True)  
    fecha_pago = db.Column(db.DateTime, nullable=True)  

    factura = db.relationship('Factura', backref='formulario_pago')


class MarcaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Marca
        include_relationships = True
        load_instance = True

class FormularioPagoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FormularioPago
        include_relationships = True
        load_instance = True


class DescuentoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Descuento
        include_relationships = True
        load_instance = True

class AnimalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Animal  
        include_relationships = True
        load_instance = True



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
        model = TipoDoc  
        include_relationships = True
        load_instance = True

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol  
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
        include_relationships = True 
        load_instance = True

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        include_relationships = True  
        load_instance = True
        include_fk = True 

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