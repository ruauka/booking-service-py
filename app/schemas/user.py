from typing import Optional
from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    email: EmailStr
    password: str

    def encode(self, pass_hash: str) -> dict[str, str]:
        self.password = pass_hash
        return {
            "email": self.email,
            "hashed_password": self.password
        }


class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]

    def is_empty(self) -> bool:
        return not any(vars(self).values())


class UserResponse(BaseModel):
    id: str
    email: EmailStr

    class Config:
        orm_mode = True
