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

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: str
    email: EmailStr

    @staticmethod
    def all_resp(users: list):
        users_result: list = []
        for user in users:
            resp_user = {
                "id": user.id,
                "email": user.email
            }
            users_result.append(resp_user)

        return users_result
