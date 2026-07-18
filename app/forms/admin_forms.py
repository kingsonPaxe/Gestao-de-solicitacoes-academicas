from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class AlunoForm(FlaskForm):
    nome = StringField("Nome completo", validators=[DataRequired(), Length(max=120)])
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    curso = StringField("Curso", validators=[Optional(), Length(max=120)])
    senha = PasswordField("Senha", validators=[Optional(), Length(min=4, max=128)])
    submit = SubmitField("Salvar")


class TipoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=120)])
    descricao = TextAreaField("Descrição", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Salvar")
