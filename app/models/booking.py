from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.storage.database import Base


class Booking(Base):
    """
    Модель бронирования.
    """
    room_id = Column(ForeignKey("rooms.id", ondelete="CASCADE"))
    user_id = Column(ForeignKey("users.id"))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
    total_days = Column(Integer, Computed("date_to - date_from"))

    user = relationship("User", back_populates="booking")
    room = relationship("Room", back_populates="booking")

    def __str__(self):
        return f"Booking #{self.id}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}, "
            f"id={self.id}, "
            f"room_id={self.room_id}, "
            f"user_id={self.user_id}, "
            f"date_from={self.date_from}, "
            f"date_to={self.date_to}, "
            f"price={self.price}, "
            f"total_cost={self.total_cost}, "
            f"total_days={self.total_days}, "
        )

    def todict(self):
        """
        Приведение модели к словарю.
        :return: словарь из некоторых полей модели
        """
        return {
            "id": self.id,
            "room_id": self.room_id,
            "user_id": self.user_id,
            "date_from": self.date_from,
            "date_to": self.date_to,
        }
