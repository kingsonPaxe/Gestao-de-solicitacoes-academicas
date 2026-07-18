from datetime import datetime
from ..database import db


class StatusSolicitacao:
    RECEBIDA = "Recebida"
    EM_ANALISE = "Em análise"
    AGUARDANDO_DOCS = "Aguardando documentos"
    APROVADA = "Aprovada"
    REJEITADA = "Rejeitada"
    DOCUMENTO_EMITIDO = "Documento emitido"
    CONCLUIDA = "Concluída"

    ALL = [
        RECEBIDA, EM_ANALISE, AGUARDANDO_DOCS, APROVADA,
        REJEITADA, DOCUMENTO_EMITIDO, CONCLUIDA,
    ]
    PENDENTES = [RECEBIDA, EM_ANALISE, AGUARDANDO_DOCS]
    FINALIZADAS = [CONCLUIDA, DOCUMENTO_EMITIDO, REJEITADA]


class Solicitacao(db.Model):
    __tablename__ = "solicitacoes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey("tipos_solicitacao.id"), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40), nullable=False, default=StatusSolicitacao.RECEBIDA)
    arquivo = db.Column(db.String(255), nullable=True)
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow,
                                   onupdate=datetime.utcnow, nullable=False)

    usuario = db.relationship("Usuario", back_populates="solicitacoes")
    tipo = db.relationship("TipoSolicitacao", back_populates="solicitacoes")
    historico = db.relationship("Historico", back_populates="solicitacao",
                                cascade="all, delete-orphan",
                                order_by="Historico.data.desc()")
