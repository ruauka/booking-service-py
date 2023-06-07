from typing import Optional

from jose import jwt
from pydantic import EmailStr
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth.auth import create_JWT_token, verify_user
from app.errors import NoAdminErr, UserNotFoundErr
from app.storage.database import async_session_maker
from app.storage.user import UserDAO
from config import cfg


class AdminAuth(AuthenticationBackend):
    """
    Класс авторизации и аутентификации в админку.
    """
    session: AsyncSession = None

    async def login(self, request: Request) -> bool:
        """
        Логин админа. Выписывается JWT кука.
        :param request: входящий запрос
        :return: bool
        """
        form = await request.form()
        email, password = form["username"], form["password"]
        # python <= 3.9 - __anext__()
        # python >= 3.10 - await next(get_session())
        # session = await get_session().__anext__()
        async with async_session_maker() as session:
            self.session = session

        user = await verify_user(self.session, EmailStr(email), password)
        if not user:
            raise UserNotFoundErr
        if not user.admin:
            raise NoAdminErr

        token = create_JWT_token({"sub": str(user.id)})
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        """
        Логаут админа.
        :param request: входящий запрос
        :return: bool
        """
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        """
        Аутентификация админа.
        :param request:
        :return: опциональный редирект на страницу аутентификации админки в случае неуспешной аутентификации админа.
        """
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        # парсинг куки
        payload = jwt.decode(token, cfg.secret_key, cfg.sha_algorithm)
        # получение id пользователя (админа)
        user_id: str = payload.get("sub")

        try:
            user = await UserDAO.get_one(self.session, id=int(user_id))
            if not user:
                return RedirectResponse(request.url_for("admin:login"), status_code=302)
        except AttributeError:
            # на случай, когда админ не вылогинился до остановки сервиса и кука осталась висеть в браузере
            request.session.clear()
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(secret_key="...")
