from flask import Flask, render_template, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) 
app.config["SECRET_KEY"] = 'mi clave!'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/coding_dojo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

from forms import FormularioRegistro

class Usuario(db.Model):
    __tablename__  = "usuarios"
    id             = db.Column(db.Integer, primary_key = True)
    nombre         = db.Column(db.String(45), nullable = False)
    correo         = db.Column(db.String(45), nullable = False)
    clave          = db.Column(db.String(255), nullable = False) 
    #Datos según proyecto

    @staticmethod
    def obtener_todos():
        all_items = db.session.execute(db.select(Usuario)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)   
        print("Items de consulta:",all_items_list)
        return(all_items_list)     

    def establecer_clave(self, clave):
        self.clave = generate_password_hash(clave)
    def chequeo_clave(self, clave):
        return check_password_hash(self.clave, clave)
    
Migrate(app,db)

@app.route("/")
def auth(form_registro=None):
    if form_registro == None:
        form_registro = FormularioRegistro()
    return render_template("auth.html",form_registro=form_registro)

@app.route("/register", methods=["POST"])
def register():
    form  = FormularioRegistro()
    error = None 
    if form.validate_on_submit():
        print("form valido")
        flash("Form valido")
        nombre = form.nombre.data
        correo = form.correo.data 
        clave  = form.clave.data 
        
        usuario = Usuario()
        usuario.nombre = nombre 
        usuario.correo = correo 
        usuario.establecer_clave(clave)
        
        db.session.add(usuario)
        db.session.commit()
        
        return redirect("/home")
    else:
        print("form invalido")
        flash("Form invalido")
        return auth(form_registro=form)

@app.route("/home")
def home():
    usuarios = Usuario().obtener_todos()
    return render_template("perfil.html",usuarios=usuarios)