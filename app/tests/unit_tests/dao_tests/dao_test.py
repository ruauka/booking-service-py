import pytest

from app.storage.user import UserDAO


@pytest.mark.parametrize(
    "email",
    [
        "ruauka@test.com",
        "ushakov@example.com",
        "....."
    ]
)
async def test_find_user_by_id(session, email):
    """ Тест dao поиска пользователя по ID """
    user = await UserDAO.get_one(session, email=email)

    if user:
        assert user.email == email
    else:
        assert not user
