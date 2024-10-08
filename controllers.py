""" 
Maneja el control sobre la información de la vista
y los modelos de bases de datos
"""
from models import db, Usuario, Curso

class ControladorUsuarios:
    @staticmethod
    def crear_usuario(nombre,correo,clave):
        usuario = Usuario()
        usuario.nombre = nombre 
        usuario.correo = correo 
        usuario.establecer_clave(clave)
            
        #Agregamos a la base datos
        db.session.add(usuario)
        db.session.commit()
        return usuario
    #def editar_usuario()
    #def obtener_usuarios()
    #def borrar_usuario()

class ControladorCursos:
    @staticmethod
    def crear_curso(nombre):
        nuevo_curso        = Curso()
        nuevo_curso.nombre = nombre 
        db.session.add(nuevo_curso)
        db.session.commit()
        print("Nuevo curso agregado")
    
    @staticmethod
    def obtener_todos():
        all_items = db.session.execute(db.select(Curso)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)
        return all_items_list
    
    @staticmethod
    def obtener_por_id(id):
        item = db.session.execute(db.select(Curso).filter_by(id=id)).scalar_one()
        return item
    