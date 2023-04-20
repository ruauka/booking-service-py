from sqlalchemy import Column, String
from app.storage.database import Base


class User(Base):
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    def __str__(self):
        return (
            f"{self.__class__.__name__}, "
            f"id={self.id}, "
            f"email={self.email}, "
            f"hashed_password={self.hashed_password}, "
        )

    def __repr__(self):
        return str(self)
