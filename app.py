from flask import Flask, render_template
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/coding_dojo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Mascota(db.Model):
    __tablename__  = "mascotas"
    id             = db.Column(db.Integer, primary_key = True)
    nombre         = db.Column(db.String(45), nullable = False)
    tipo           = db.Column(db.String(45), nullable = False)
    color          = db.Column(db.String(45), nullable = False)
    updated_at     = db.Column(db.DateTime(), nullable = False)
    created_at     = db.Column(db.DateTime(), nullable = False)
    
    @staticmethod
    def get_all():
        all_items = db.session.execute(db.select(Mascota)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)   
        print(all_items)
        return(all_items_list)     

Migrate(app,db)

@app.route("/")
def index():
    mascotas = Mascota().get_all()
    return render_template("index.html",mascotas=mascotas)
