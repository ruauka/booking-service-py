from typing import Any

from app.auth.auth import get_password_hash
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


def set_new_fields(instance, new_fields) -> dict[str, Any]:
    for key, value in new_fields:
        if not value:
            continue
        setattr(instance, key, value)

    return instance.todict()

# def set_new_fields(instance, **new_fields) -> dict[str, Any]:
#     for key in new_fields.keys():
#         setattr(instance, key, new_fields[key])
#
#     return instance.todict()
