from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class TransForm(FlaskForm):
    content = TextAreaField("Текст для перевода")
    submit = SubmitField('Перевести')




