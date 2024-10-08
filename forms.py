"""
    Archivo donde se definen los formularios del sistema
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class FormularioRegistro(FlaskForm):    
    nombre          = StringField('Nombre', validators=[DataRequired(), Length(min=3)])
    correo          = EmailField('Correo', validators=[DataRequired(), Email()])
    clave           = PasswordField('Clave', validators=[DataRequired(), EqualTo('confirmar_clave', message="Las claves deben ser iguales.")])
    confirmar_clave = PasswordField('Confirmar clave', validators=[DataRequired()])
    submit          = SubmitField('Registrarme')

class FormularioAcceso(FlaskForm):    
    correo = EmailField('Correo', validators=[DataRequired(), Email()])
    clave  = PasswordField('Clave', validators=[DataRequired()])    
    submit = SubmitField('Acceder')

class FormularioAgregarCurso(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=1,max=30)])
    submit = SubmitField('Agregar')

class FormularioNuevoEstudiante(FlaskForm):
    cursos    = SelectField('Curso')
    nombre    = StringField('Nombre', validators=[DataRequired(), Length(min=1,max=255)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=1,max=255)])
    edad      = IntegerField('Edad')
    submit    = SubmitField('Crear')
