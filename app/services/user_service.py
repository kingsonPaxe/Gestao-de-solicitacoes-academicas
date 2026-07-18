from ..models import Usuario
from ..repositories.user_repo import UserRepository


class UserService:
    @staticmethod
    def criar_aluno(nome: str, email: str, senha: str, curso: str | None) -> Usuario:
        if UserRepository.get_by_email(email):
            raise ValueError("Já existe um usuário com este e-mail.")
        u = Usuario(nome=nome.strip(), email=email.lower().strip(),
                    curso=(curso or "").strip() or None, tipo="aluno")
        u.set_password(senha)
        return UserRepository.save(u)

    @staticmethod
    def atualizar_aluno(user_id: int, nome: str, email: str,
                       curso: str | None, senha: str | None = None) -> Usuario:
        u = UserRepository.get(user_id)
        if not u:
            raise ValueError("Aluno não encontrado.")
        existing = UserRepository.get_by_email(email)
        if existing and existing.id != u.id:
            raise ValueError("Já existe outro usuário com este e-mail.")
        u.nome = nome.strip()
        u.email = email.lower().strip()
        u.curso = (curso or "").strip() or None
        if senha:
            u.set_password(senha)
        return UserRepository.save(u)

    @staticmethod
    def excluir_aluno(user_id: int) -> None:
        u = UserRepository.get(user_id)
        if not u:
            raise ValueError("Aluno não encontrado.")
        if u.is_admin:
            raise ValueError("Não é possível excluir administradores por aqui.")
        UserRepository.delete(u)
