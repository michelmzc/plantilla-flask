from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class FormularioRegistro(FlaskForm):    
    nombre     = StringField('Nombre', validators=[DataRequired(), Length(min=3)])
    correo     = EmailField('Email', validators=[DataRequired(), Email()])
    clave      = PasswordField('Clave', validators=[DataRequired(), EqualTo('confirmar_clave', message="Las claves deben ser iguales.")])
    confirmar_clave = PasswordField('Confirmar clave', validators=[DataRequired()])
    submit = SubmitField('Registrarme')

class LoginForm(FlaskForm):    
    email    = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])    
    submit   = SubmitField('Login')

class ItemForm(FlaskForm):    
    name      = StringField('Item/Product', validators=[DataRequired(), Length(min=3)])
    submit    = SubmitField('Add')   