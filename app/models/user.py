from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    curso = db.Column(db.String(120), nullable=True)
    tipo = db.Column(db.String(20), nullable=False, default="aluno")  # 'aluno' | 'admin'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    solicitacoes = db.relationship("Solicitacao", back_populates="usuario",
                                   cascade="all, delete-orphan")

    def set_password(self, senha: str) -> None:
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    @property
    def is_admin(self) -> bool:
        return self.tipo == "admin"
