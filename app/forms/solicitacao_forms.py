from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class SolicitacaoForm(FlaskForm):
    tipo_id = SelectField("Tipo de solicitação", coerce=int, validators=[DataRequired()])
    descricao = TextAreaField("Descrição / Justificativa",
                              validators=[DataRequired(), Length(min=5, max=2000)])
    submit = SubmitField("Enviar solicitação")


class AtualizarStatusForm(FlaskForm):
    status = SelectField("Novo status", validators=[DataRequired()])
    observacao = TextAreaField("Observação", validators=[Length(max=2000)])
    arquivo = FileField("Anexar PDF (opcional)",
                        validators=[FileAllowed(["pdf"], "Somente arquivos PDF.")])
    submit = SubmitField("Atualizar")
