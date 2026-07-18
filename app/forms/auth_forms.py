from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=4, max=128)])
    submit = SubmitField("Entrar")
