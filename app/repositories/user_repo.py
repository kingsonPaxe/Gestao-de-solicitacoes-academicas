from typing import Optional, List
from ..database import db
from ..models import Usuario


class UserRepository:
    @staticmethod
    def get(user_id: int) -> Optional[Usuario]:
        return db.session.get(Usuario, user_id)

    @staticmethod
    def get_by_email(email: str) -> Optional[Usuario]:
        return Usuario.query.filter_by(email=email.lower().strip()).first()

    @staticmethod
    def list_alunos(search: str | None = None) -> List[Usuario]:
        q = Usuario.query.filter_by(tipo="aluno")
        if search:
            like = f"%{search.lower()}%"
            q = q.filter(db.or_(db.func.lower(Usuario.nome).like(like),
                                db.func.lower(Usuario.email).like(like)))
        return q.order_by(Usuario.nome).all()

    @staticmethod
    def count_alunos() -> int:
        return Usuario.query.filter_by(tipo="aluno").count()

    @staticmethod
    def save(user: Usuario) -> Usuario:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete(user: Usuario) -> None:
        db.session.delete(user)
        db.session.commit()
