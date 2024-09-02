from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/coding_dojo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Mascota(db.Model):
    __tablename__  = "mascotas"
    id             = db.Column(db.Integer, primary_key = True)
    nombres        = db.Column(db.String(45), nullable = False)

Migrate(app,db)