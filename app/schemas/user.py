from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    """
    Валидационная схема входящего запроса полей пользователя.
    """
    email: EmailStr
    password: str
    admin: Optional[bool] = False

    def hash_pass_replace(self, pass_hash: str) -> dict[str, str]:
        """
        Изменение навзвания поля входящего пароля для корректного маппинга с моделью.
        :param pass_hash: хэш пароля
        :return: словарь данных пользователя
        """
        self.password = pass_hash
        return {
            "email": self.email,
            "hashed_password": self.password,
            "admin": self.admin
        }


class UserLoginRequest(BaseModel):
    """
    Валидационная схема входящего запроса полей логина пользователя.
    """
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    """
     Валидационная схема входящего запроса полей обновления пользователя.
    """
    email: Optional[EmailStr]
    password: Optional[str]
    admin: Optional[bool] = False

    def is_empty(self) -> bool:
        """
        Проверка на пустые поля, включая bool.
        :return: bool
        """
        for field_val in vars(self).values():
            if field_val is not None:
                return False

        return True


class UserResponse(BaseModel):
    """
    Валидационная схема исходящего запроса полей пользователя.
    """
    id: str
    email: EmailStr
    admin: bool = False

    # парсинг ответа sqlalchemy в pydantic
    class Config:
        orm_mode = True
