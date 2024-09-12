""" 
Maneja el control sobre la información de la vista
y los modelos de bases de datos
"""
from models import Usuario, db

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