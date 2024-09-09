from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class FormularioRegistro(FlaskForm):    
    nombre     = StringField('Nombre', validators=[DataRequired(), Length(min=3)])
    apellido   = StringField('Apellido',validators=[DataRequired(), Length(min=3)])
    email      = EmailField('Email', validators=[DataRequired(), Email()])
    clave      = PasswordField('Clave', validators=[DataRequired(), EqualTo('password_confirm', message="Password must be equals.")])
    confirmar_clave = PasswordField('Confirmar clave', validators=[DataRequired()])
    submit = SubmitField('Registrarme')


class LoginForm(FlaskForm):    
    email    = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])    
    submit   = SubmitField('Login')

class ItemForm(FlaskForm):    
    name      = StringField('Item/Product', validators=[DataRequired(), Length(min=3)])
    submit    = SubmitField('Add')   