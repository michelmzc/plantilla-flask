"""
    Archivo de modelos de bases de datos
"""
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash #seguridad

#Modelos de bases de datos
class Usuario(db.Model, UserMixin):
    __tablename__  = "usuarios"
    id             = db.Column(db.Integer, primary_key = True)
    nombre         = db.Column(db.String(45),nullable=False)
    apellidos      = db.Column(db.String(255), nullable = True)
    edad           = db.Column(db.Integer, nullable = True)
    correo         = db.Column(db.String(45),nullable=False,unique=True)
    clave          = db.Column(db.String(255),nullable=False) 
    #Datos según proyecto
    
    #Relaciones 
    estudiante     = db.relationship("Estudiante", back_populates = "usuario")

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
        print(f"Consultando por el usuario con id{id} en db")
        return Usuario.query.get(id)

class Curso(db.Model):
    __tablename__ = "cursos"
    id            = db.Column(db.Integer, primary_key = True)
    nombre        = db.Column(db.String(30), nullable = False)
    estudiantes   = db.relationship("Estudiante", back_populates = "curso")
    
class Estudiante(db.Model):
    __tablename__ = "estudiantes"
    id            = db.Column(db.Integer, primary_key = True)
    
    #Relaciones con demás tablas 
    #Llave foránea con relación a usuarios
    id_usuario    = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    #Relación entre la tabla usuario y estudiante en python (para ORM)
    usuario       = db.relationship("Usuario", back_populates = "estudiante")
    # Relación entre la tabla usuario y su curso
    id_curso      = db.Column(db.Integer, db.ForeignKey("cursos.id"))
    curso         = db.relationship("Curso", back_populates = "estudiantes")