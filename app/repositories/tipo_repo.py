from typing import List, Optional
from ..database import db
from ..models import TipoSolicitacao


class TipoRepository:
    @staticmethod
    def all() -> List[TipoSolicitacao]:
        return TipoSolicitacao.query.order_by(TipoSolicitacao.nome).all()

    @staticmethod
    def get(tipo_id: int) -> Optional[TipoSolicitacao]:
        return db.session.get(TipoSolicitacao, tipo_id)

    @staticmethod
    def get_by_nome(nome: str) -> Optional[TipoSolicitacao]:
        return TipoSolicitacao.query.filter_by(nome=nome).first()

    @staticmethod
    def save(tipo: TipoSolicitacao) -> TipoSolicitacao:
        db.session.add(tipo)
        db.session.commit()
        return tipo

    @staticmethod
    def delete(tipo: TipoSolicitacao) -> None:
        db.session.delete(tipo)
        db.session.commit()
