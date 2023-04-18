from app.storage.database import Base
from sqlalchemy import Column, String
from app.schemas.user import UserRequest


class User(Base):
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    @staticmethod
    def parse(user: UserRequest):
        return {
            "email": user.email,
            "hashed_password": user.password
        }

    def __str__(self):
        return (
            f"{self.__class__.__name__}, "
            f"id={self.id}, "
            f"email={self.email}, "
            f"hashed_password={self.hashed_password}, "
        )

    def __repr__(self):
        return str(self)
