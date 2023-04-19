from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    email: EmailStr
    password: str

    def encode(self, pass_hash: str):
        self.password = pass_hash
        return {
            "email": self.email,
            "hashed_password": self.password
        }

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: str
    email: EmailStr
