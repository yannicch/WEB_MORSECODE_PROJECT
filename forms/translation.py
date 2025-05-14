from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class TransForm(FlaskForm):
    content = TextAreaField("Текст для перевода")
    lang = SelectField(choices=[('English', 'English'), ('Russian', 'Russian'), ('Morsecode', 'Morsecode')], default='Russian')
    trans_lang = SelectField(choices=[('English', 'English'), ('Russian', 'Russian'), ('Morsecode', 'Morsecode')], default='Morsecode')
    submit = SubmitField('Перевести')




