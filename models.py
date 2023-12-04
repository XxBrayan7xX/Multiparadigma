import jwt
import datetime
from config import BaseConfig
from app import db,bcrypt

class Sensor(db.model):
    __tablename__="sensor"
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre=db.Column(db.String(255),nullable=False)
    posicion=db.Column(db.String(255),nullable=False)
    precio=db.Column(db.Real,nullable=False)
    garantia=db.Column(db.String(255),nullable=False)

class Lubricante(db.model):
    __tablename__="lubricante"
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre=db.Column(db.String(255),nullable=False)
    cantidad=db.Column(db.Integer,nullable=False)
    precio=db.Column(db.Real,nullable=False)
    grado=db.Column(db.String(255),nullable=False)

class Herramienta(db.model):
    __tablename__="herramienta"
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    marca=db.Column(db.String(255),nullable=False)
    cantidadpiezas=db.Column(db.Integer,nullable=False)
    precio=db.Column(db.Real,nullable=False)
    reposicion=db.Column(db.Boolean,nullable=False,default=False)

class Pieza(db.model):
    __tablename__="pieza"
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre=db.Column(db.String(255),nullable=False)
    posicion=db.Column(db.String(255),nullable=False)
    precio=db.Column(db.Real,nullable=False)
    tamaño=db.Column(db.String(255),nullable=False)

class Vendedor(db.model):
    __tablename__="vendedor"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(255),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    telefono=db.Column(db.Integer,nullable=False)
    admin=db.Column(db.Boolean,nullable=False,default=False)

    def __init__(self,email,password,telefono,admin=False)->None:
        self.email=email
        self.password=bcrypt.generate_password_hash(
            password,BaseConfig.BCRYPT_LOG_ROUNDS
        ).decode

        self.telefono=telefono
        self.admin=admin

    def encode_auth_token(self,user_id):
        try:
            payload={
                'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5),
                'iat':datetime.datetime.utcnow(),
                'sub':user_id
            }
            return jwt.encode(
                payload,
                BaseConfig.SECRET_KEY,
                algorithm="HS256"
            )
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token,BaseConfig.SECRET_KEY,algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError as e:
            return 'Signture Expired Please log in again'
        except jwt.InvalidTokenError as e:
            return 'Invlid token'
        