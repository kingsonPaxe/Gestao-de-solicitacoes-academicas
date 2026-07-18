from datetime import datetime
from ..database import db


class Historico(db.Model):
    __tablename__ = "historico"

    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey("solicitacoes.id"), nullable=False)
    status = db.Column(db.String(40), nullable=False)
    observacao = db.Column(db.Text, nullable=True)
    usuario_responsavel = db.Column(db.String(120), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    solicitacao = db.relationship("Solicitacao", back_populates="historico")
