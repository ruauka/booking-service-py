from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.storage.database import Base


class User(Base):
    """
    Модель пользователя.
    """
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False, default=False, server_default="false")

    booking = relationship("Booking", back_populates="user")

    def __str__(self):
        return f"email={self.email}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}, "
            f"id={self.id}, "
            f"email={self.email}, "
            f"hashed_password={self.hashed_password}, "
            f"admin={self.admin}"
        )
