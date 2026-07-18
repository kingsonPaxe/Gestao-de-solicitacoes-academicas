from ..database import db
from ..models import Historico


class HistoricoRepository:
    @staticmethod
    def add(solicitacao_id: int, status: str, observacao: str | None,
            usuario_responsavel: str | None) -> Historico:
        h = Historico(
            solicitacao_id=solicitacao_id,
            status=status,
            observacao=observacao,
            usuario_responsavel=usuario_responsavel,
        )
        db.session.add(h)
        db.session.commit()
        return h
