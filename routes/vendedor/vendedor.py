from flask import Blueprint,request,jsonify,render_template,redirect
from sqlalchemy import exc 
from models import Vendedor
from app import db,bcrypt
##from routes.user import appuser
from auth import tokenCheck,verificarToken

appuser=Blueprint('appuser',__name__,template_folder="templates")

@appuser.route("/auth/registro",methods=["POST"])
def registro():
    user=request.get_json()
    userExist=Vendedor.query.filter_by(email=user['email']).first()
    if not userExist:
        usuario=Vendedor(email=user['email'],password=user['password'])
        try:
            db.session.add(usuario)
            db.session.commit()
            mensaje="Usuario creado"
        except exc.SQLAlchemyError as e:
            mensaje="ERROR"+e
    else: 
        mensaje =  "Usuario existente"
    return jsonify({"message":mensaje})

@appuser.route('/auth/login',methods=["POST"])
def login():
    user=request.get_json()
    usuario=Vendedor.query.filter_by(email=user['email'],password=user['password'],telefono=['telefono'])
    searchUser=Vendedor.query.filter_by(email=user['email']).first()
    if searchUser:
        validation =  bcrypt.check_password_hash(searchUser.password,user["password"])
        if validation:
            auth = usuario.encode_auth_token(user_id=searchUser.id)
            print(auth)
            response={
                "status":"success",
                "message":"Login exitoso",
                "auth_token":auth
            }
            return jsonify(response)
    return jsonify({"message":"Datos incorrectos"})

@appuser.route('/usuarios',methods=["GET"])
@tokenCheck
def getUsers(usuario):
    print(usuario)
    print(usuario['admin'])
    if(usuario['admin']):
        output=[]
        usuarios=Vendedor.query.all()
        for usuario in usuarios:
            usuarioData={}
            usuarioData['id']=usuario.id,
            usuarioData['email']=usuario.email,
            usuarioData['password']=usuario.password,
            usuarioData['telefono']=usuario.telefono,
            output.append(usuarioData)
        return jsonify({'usuarios':output})
    else:
        return jsonify({'Error':"No tienes permisios"})
            

@appuser.route('/main')
def main():
    return render_template('main.html')

@appuser.route('/login',methods=["GET","POST"])
def login_post():
    if(request.method=="GET"):
        token=request.args.get('token')
        if token:
            Info=verificarToken(token)
            if(Info['status']!="fail"):
                responseObject={
                    'status':"success",
                    'message':"valid token",
                    'info':Info
                }
                return jsonify(responseObject)
        return render_template('login.html')
    else:
        email = request.json['email']
        password = request.json['password']
        telefono = request.json['telefono']
        usuario = Vendedor(email=email,password=password,telefono=telefono)
        searchUser = Vendedor.query.filter_by(email=email).first()
        if searchUser:
            validation = bcrypt.check_password_hash(searchUser.password, password)
            if validation:
                auth_token =  usuario.encode_auth_token(user_id=searchUser.id)
                responseObject={
                    'status':"success",
                    'login':"Loggin exitoso",
                    'auth_token':auth_token
                }
                return jsonify(responseObject)
        return  jsonify({'message':"Datos incorrectos"})

@appuser.route('/sign',methods=["GET","POST"])
def login_post():
    if request.method=="GET":
        return render_template('registrar.html')
    else:
        email=request.json['email']
        password=request.json['password']
        telefono=request.json['telefono']
        usuario = Vendedor(email=email,password=password,telefono=telefono)
        userExist = Vendedor.query.filter_by(email=email).first()
        if not userExist:
            try:
                db.session.add(usuario)
                db.session.commit()
                responseObject={
                    'status':"success",
                    'message':"Registro exitoso"
                }
            except exc.SQLAlchemyError as e:
                responseObject={
                    'status':"error",
                    'message':e
                }
        else:
            responseObject={
                'status':"error",
                'message':"vendedor existente"
            }
        return jsonify(responseObject)