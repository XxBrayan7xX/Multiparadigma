from models import User
from functools import wraps
from flask import jsonify, request

def obtenerInfo(token):
    if token:
        resp =User.decode_auth_token(token)
        user=User.query.filter_by(id=resp).first()
        if user:
            usuario = {
                'status':'success',
                'data':{
                    'user_id':user.id,
                    'email':user.email,
                    'admin':user.admin,
                    'telefono':user.telefono
                }
            }
            return usuario
        else:
            error={
                'status':'fail',
                'message':resp
            }
            return error
def tokenCheck(f):
    @wraps(f)
    def verificar(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message':'Token no encontrado'})
        try:
            info=obtenerInfo(token)
            print(info)
            if info['status']=='fail':
                return jsonify({'message':'Token invlido'})
        except:
            return jsonify({'message':'token invalido'})
        return f(info['data'],*args,**kwargs)
    return verificar

def verificarToken(token):
    if not token:
        return jsonify({'message':'token no encontrado'})
    try:
        info = obtenerInfo(token)
        if info['status']=='fail':
            return jsonify({'message':'token invalido'})
    except:
        return jsonify({'message':'token invalidio'})
    return info