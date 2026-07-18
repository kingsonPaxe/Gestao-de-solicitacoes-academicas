from ..database import db


class TipoSolicitacao(db.Model):
    __tablename__ = "tipos_solicitacao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    descricao = db.Column(db.String(500), nullable=True)

    solicitacoes = db.relationship("Solicitacao", back_populates="tipo")
