from typing import List, Optional
from sqlalchemy import or_, func
from ..database import db
from ..models import Solicitacao, Usuario


class SolicitacaoRepository:
    @staticmethod
    def get(sid: int) -> Optional[Solicitacao]:
        return db.session.get(Solicitacao, sid)

    @staticmethod
    def by_user(user_id: int, status: str | None = None,
                search: str | None = None) -> List[Solicitacao]:
        q = Solicitacao.query.filter_by(usuario_id=user_id)
        if status:
            q = q.filter_by(status=status)
        if search:
            like = f"%{search.lower()}%"
            q = q.filter(func.lower(Solicitacao.descricao).like(like))
        return q.order_by(Solicitacao.data_abertura.desc()).all()

    @staticmethod
    def all(status: str | None = None, search_aluno: str | None = None,
            tipo_id: int | None = None) -> List[Solicitacao]:
        q = Solicitacao.query.join(Usuario)
        if status:
            q = q.filter(Solicitacao.status == status)
        if tipo_id:
            q = q.filter(Solicitacao.tipo_id == tipo_id)
        if search_aluno:
            like = f"%{search_aluno.lower()}%"
            q = q.filter(or_(func.lower(Usuario.nome).like(like),
                             func.lower(Usuario.email).like(like)))
        return q.order_by(Solicitacao.data_abertura.desc()).all()

    @staticmethod
    def count(status: str | None = None) -> int:
        q = Solicitacao.query
        if status:
            q = q.filter_by(status=status)
        return q.count()

    @staticmethod
    def count_in(statuses: list[str]) -> int:
        return Solicitacao.query.filter(Solicitacao.status.in_(statuses)).count()

    @staticmethod
    def count_by_user(user_id: int, status: str | None = None) -> int:
        q = Solicitacao.query.filter_by(usuario_id=user_id)
        if status:
            q = q.filter_by(status=status)
        return q.count()

    @staticmethod
    def count_by_user_in(user_id: int, statuses: list[str]) -> int:
        return Solicitacao.query.filter_by(usuario_id=user_id).filter(
            Solicitacao.status.in_(statuses)).count()

    @staticmethod
    def group_by_status() -> dict[str, int]:
        rows = db.session.query(Solicitacao.status, func.count(Solicitacao.id)) \
            .group_by(Solicitacao.status).all()
        return {status: count for status, count in rows}

    @staticmethod
    def group_by_tipo() -> list[tuple[str, int]]:
        from ..models import TipoSolicitacao
        rows = db.session.query(TipoSolicitacao.nome, func.count(Solicitacao.id)) \
            .join(Solicitacao, Solicitacao.tipo_id == TipoSolicitacao.id) \
            .group_by(TipoSolicitacao.nome).all()
        return [(nome, count) for nome, count in rows]

    @staticmethod
    def latest(limit: int = 5, user_id: int | None = None) -> List[Solicitacao]:
        q = Solicitacao.query
        if user_id:
            q = q.filter_by(usuario_id=user_id)
        return q.order_by(Solicitacao.data_abertura.desc()).limit(limit).all()

    @staticmethod
    def save(s: Solicitacao) -> Solicitacao:
        db.session.add(s)
        db.session.commit()
        return s

    @staticmethod
    def delete(s: Solicitacao) -> None:
        db.session.delete(s)
        db.session.commit()
