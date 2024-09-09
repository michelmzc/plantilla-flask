from flask import Flask, render_template, flash, redirect
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
    apellido       = db.Column(db.String(45), nullable = False)
    correo         = db.Column(db.String(45), nullable = False)
    clave          = db.Column(db.String(255), nullable = False) 
    foto           = db.Column(db.Text, nullable=True)
    #Datos según proyecto

    @staticmethod
    def obtener_todos():
        all_items = db.session.execute(db.select(Usuario)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)   
        print("Items de consulta:",all_items_list)
        return(all_items_list)     

Migrate(app,db)

@app.route("/")
def auth(form_registro=None):
    if form_registro == None:
        form_registro = FormularioRegistro()
    return render_template("auth.html",form_registro=form_registro)

@app.route("/register", methods=["POST"])
def register():
    form = FormularioRegistro()
    error = None 
    
    print(form.errors)
        
    if form.validate_on_submit():
        print("form valido")
        flash("Form valido")
    else:
        print("form invalido")
        flash("Form invalido")
        return auth(form_registro=form)
    return redirect("/")