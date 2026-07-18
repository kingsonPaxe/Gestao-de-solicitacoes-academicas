from ..models import TipoSolicitacao
from ..repositories.tipo_repo import TipoRepository


class TipoService:
    @staticmethod
    def criar(nome: str, descricao: str | None) -> TipoSolicitacao:
        if TipoRepository.get_by_nome(nome.strip()):
            raise ValueError("Já existe um tipo com este nome.")
        t = TipoSolicitacao(nome=nome.strip(), descricao=(descricao or "").strip() or None)
        return TipoRepository.save(t)

    @staticmethod
    def excluir(tipo_id: int) -> None:
        t = TipoRepository.get(tipo_id)
        if not t:
            raise ValueError("Tipo não encontrado.")
        TipoRepository.delete(t)
