from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.storage.database import Base


class User(Base):
    """
    Модель пользователя.
    """
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    booking = relationship("Booking", back_populates="user")

    def __str__(self):
        return f"email={self.email}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}, "
            f"id={self.id}, "
            f"email={self.email}, "
            f"hashed_password={self.hashed_password}, "
        )
