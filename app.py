from flask import Flask, render_template
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/coding_dojo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

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
def index():
    usuarios = Usuario().obtener_todos()
    return render_template("perfil.html",usuarios=usuarios)
