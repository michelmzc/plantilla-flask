"""
Archivo app.py: módulo principal de la aplicación.
"""
# Importamos librerias necesarias 
from flask import Flask, render_template, flash, redirect, request

from flask_sqlalchemy import SQLAlchemy #base de datos
from flask_migrate import Migrate #versiones de bases de datos
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

#Iniciación y configuración de la app
app = Flask(__name__) 
app.config["SECRET_KEY"] = "mi clave!"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:12345678@localhost:3306/coding_dojo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app) #iniciamos bases de datos

login_manager = LoginManager(app) #iniciamos uso de sesiones
login_manager.login_view = "auth"

#Importación de módulos propios
from forms import FormularioRegistro, FormularioAcceso, FormularioAgregarCurso
from models import Usuario, Curso
from controllers import ControladorUsuarios, ControladorCursos

#Inicialización de versiones de la bases de datos
Migrate(app,db)

#Inicialización de login_manager y configuración
@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(int(user_id))
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

#Rutas
# Rutas de autentificación
# Ruta índice: Si el usuario llega por primera vez los formularios es
# tan en blanco
# Si el usuario llega a través de acceso (login) o registro llegan con formulario relleanado
@app.route("/")
def auth(form_registro=None, form_acceso=None):
    if current_user.is_authenticated:
        return redirect("/home")
    
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
        #Consultamos si existe en la db 
        usuario = Usuario().obtener_por_correo(correo)
        if usuario is not None:
            error = f"El correo {correo} ya se encuentra registrado"
            print(error)
            flash(error)
            return(redirect("/"))
        else:
            flash(f'Registro solicitado para el usuario { correo }')
            #Utilización de un controlador entre Vista y Modelo
            ControladorUsuarios().crear_usuario(nombre, correo, clave)
            #Generamos una instancia de datos            
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
        #Consultamos por el correo en la db
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
    
@app.route("/logout")
def logout():
    logout_user()
    flash(f"El usuario ha cerrado sesión")
    print(f"El usuario ha cerrado sesión")
    return(redirect("/"))

#Ruta que nos lleva al inicio del usuario
@app.route("/home")
@login_required
def home():
    formulario_curso = FormularioAgregarCurso() 
    todos_los_cursos = ControladorCursos.obtener_todos()
    return render_template("index.html", formulario_curso=formulario_curso, cursos=todos_los_cursos)

@app.route("/agregar_curso", methods=["POST"])
@login_required
def agregar_curso():
    formulario_curso = FormularioAgregarCurso()
    if formulario_curso.validate_on_submit:
        ControladorCursos().crear_curso(formulario_curso.nombre.data)

    return(redirect("/home"))

@app.route("/cursos/<int:id>")
@login_required 
def ver_curso(id):
    curso = ControladorCursos.obtener_por_id(id)
    return render_template("curso.html", curso=curso)

