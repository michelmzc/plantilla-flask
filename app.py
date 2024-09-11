"""
Archivo app.py 
    Se encuentra el módulo principal de la aplicación.
"""
# Importamos librerias necesarias 
from flask import Flask, render_template, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash #seguridad
from flask_sqlalchemy import SQLAlchemy #base de datos
from flask_migrate import Migrate #versiones de bases de datos
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user

#Iniciación y configuración de la app
app = Flask(__name__) 
app.config["SECRET_KEY"] = "mi clave!"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/coding_dojo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app) #iniciamos bases de datos
login_manager = LoginManager(app)
login_manager.login_view = "auth"

#Importación de módulos propios
from forms import FormularioRegistro, FormularioAcceso

#Modelos de bases de datos
class Usuario(db.Model, UserMixin):
    __tablename__  = "usuarios"
    id             = db.Column(db.Integer, primary_key = True)
    nombre         = db.Column(db.String(45),nullable=False)
    correo         = db.Column(db.String(45),nullable=False,unique=True)
    clave          = db.Column(db.String(255),nullable=False) 
    #Datos según proyecto
    
    def establecer_clave(self, clave):
        self.clave = generate_password_hash(clave)
    def chequeo_clave(self, clave):
        return check_password_hash(self.clave, clave)
    
    #función para obetener todos los registros de la db
    @staticmethod
    def obtener_todos():
        all_items = db.session.execute(db.select(Usuario)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)   
        print("Items de consulta:",all_items_list)
        return(all_items_list)     
    @staticmethod 
    def obtener_por_correo(correo):
        usuario = Usuario.query.filter_by(correo=correo).first()
        print(f"Consultando por el usuario {usuario} en db")
        return(usuario)
    @staticmethod
    def obtener_por_id(id):
        return Usuario.query.get(id)
#Inicialización de versiones de la bases de datos
Migrate(app,db)

#Inicialización de login_manager
@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(int(user_id))
#Rutas
# Rutas de autentificación
# Ruta índice: Si el usuario llega por primera vez los formularios es
# tan en blanco
# Si el usuario llega a través de acceso (login) o registro llegan con formulario relleanado
@app.route("/")
def auth(form_registro=None, form_acceso=None):
    if form_registro == None:
        form_registro = FormularioRegistro()
    if form_acceso == None: 
        form_acceso = FormularioAcceso()
    return render_template("auth.html",form_registro=form_registro,form_acceso=form_acceso)

#La ruta registro recibe un formulario y guarda en la base de datos
@app.route("/register", methods=["POST"])
def register():
    # Recibimos datos del formulario
    form  = FormularioRegistro()
    error = None 
    #Validos errores de formulario
    if form.validate_on_submit():
        print("form valido")
        flash("Form valido")
        nombre = form.nombre.data
        correo = form.correo.data 
        clave  = form.clave.data 
        
        #Generamos una instancia de datos
        usuario = Usuario()
        usuario.nombre = nombre 
        usuario.correo = correo 
        usuario.establecer_clave(clave)
        
        #Agregamos a la base datos
        db.session.add(usuario)
        db.session.commit()
        
        return redirect("/home")
    else:
        print("form invalido")
        flash("Form invalido")
        #devolvemos al índice con forumalario relleno
        return auth(form_registro=form)

#La ruta que nos hace el acceso (login)
@app.route("/login", methods=["POST"])
def login():
    #Recibimos los datos del login en frontend
    form_acceso = FormularioAcceso()
    if form_acceso.validate_on_submit():
        flash(f"Acceso solicitado para el usuario { form_acceso.correo.data }")
        usuario = Usuario().obtener_por_correo(form_acceso.correo.data)
        #Si el usuario no es nada (existe en la db)
        if usuario is not None:
            if usuario.chequeo_clave(form_acceso.clave.data):
                login_user(usuario)
                return(redirect("/home"))
            else:
                flash(f"Clave incorrecta")
                print(f"Clave incorrecta")
                return(redirect("/"))
        else:
            flash(f"El usuario no esta registrado")
            print(f"El usuario no esta registrado")
            return(redirect("/"))
        
    return(redirect("/home"))
    
#Ruta que nos lleva al inicio del usuario
@app.route("/home")
def home():
    usuarios = Usuario().obtener_todos()
    return render_template("perfil.html",usuarios=usuarios)