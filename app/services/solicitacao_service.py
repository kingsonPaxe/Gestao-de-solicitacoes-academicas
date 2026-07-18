import os
import uuid
from typing import Optional
from werkzeug.utils import secure_filename
from flask import current_app
from ..models import Solicitacao, StatusSolicitacao
from ..repositories.solicitacao_repo import SolicitacaoRepository
from ..repositories.historico_repo import HistoricoRepository


ALLOWED_EXT = {"pdf"}


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


class SolicitacaoService:
    @staticmethod
    def criar(usuario_id: int, tipo_id: int, descricao: str,
              usuario_nome: str) -> Solicitacao:
        s = Solicitacao(usuario_id=usuario_id, tipo_id=tipo_id,
                        descricao=descricao.strip(),
                        status=StatusSolicitacao.RECEBIDA)
        SolicitacaoRepository.save(s)
        HistoricoRepository.add(s.id, s.status, "Solicitação criada", usuario_nome)
        return s

    @staticmethod
    def editar_pelo_aluno(sid: int, usuario_id: int, tipo_id: int,
                          descricao: str) -> Solicitacao:
        s = SolicitacaoRepository.get(sid)
        if not s or s.usuario_id != usuario_id:
            raise ValueError("Solicitação não encontrada.")
        if s.status != StatusSolicitacao.RECEBIDA:
            raise ValueError("Só é possível editar enquanto a solicitação estiver "
                             "com status 'Recebida'.")
        s.tipo_id = tipo_id
        s.descricao = descricao.strip()
        return SolicitacaoRepository.save(s)

    @staticmethod
    def atualizar_status(sid: int, novo_status: str, observacao: str | None,
                         admin_nome: str, arquivo=None) -> Solicitacao:
        if novo_status not in StatusSolicitacao.ALL:
            raise ValueError("Status inválido.")
        s = SolicitacaoRepository.get(sid)
        if not s:
            raise ValueError("Solicitação não encontrada.")
        s.status = novo_status

        if arquivo and arquivo.filename:
            if not _allowed(arquivo.filename):
                raise ValueError("Apenas arquivos PDF são permitidos.")
            fname = secure_filename(arquivo.filename)
            unique = f"{uuid.uuid4().hex}_{fname}"
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique)
            arquivo.save(path)
            s.arquivo = unique

        SolicitacaoRepository.save(s)
        HistoricoRepository.add(s.id, novo_status, observacao, admin_nome)
        return s

    @staticmethod
    def excluir(sid: int) -> None:
        s = SolicitacaoRepository.get(sid)
        if not s:
            raise ValueError("Solicitação não encontrada.")
        if s.arquivo:
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], s.arquivo)
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
        SolicitacaoRepository.delete(s)

    @staticmethod
    def get_para_aluno(sid: int, usuario_id: int) -> Optional[Solicitacao]:
        s = SolicitacaoRepository.get(sid)
        if not s or s.usuario_id != usuario_id:
            return None
        return s
