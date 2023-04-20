from typing import Any

from app.router.auth.auth import get_password_hash
from app.schemas.user import UserUpdateRequest


def set_user_new_fields(user, new_fields: UserUpdateRequest) -> dict[str, Any]:
    for key, value in new_fields:
        if not value:
            continue
        if key == "password":
            key = "hashed_password"
            value = get_password_hash(value)
        setattr(user, key, value)

    updated_fields = {
        "email": user.email,
        "hashed_password": user.hashed_password
    }

    return updated_fields
