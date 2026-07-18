from typing import Optional
from ..models import Usuario
from ..repositories.user_repo import UserRepository


class AuthService:
    @staticmethod
    def authenticate(email: str, senha: str) -> Optional[Usuario]:
        user = UserRepository.get_by_email(email)
        if user and user.check_password(senha):
            return user
        return None
