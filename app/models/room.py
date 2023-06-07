from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.storage.database import Base


class Room(Base):
    """
    Модель комнаты.
    """
    hotel_id = Column(ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(ARRAY(String(255)), nullable=True)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    hotel = relationship("Hotel", back_populates="rooms")
    booking = relationship("Booking", back_populates="room", cascade="all, delete", passive_deletes=True)

    def __str__(self):
        return f"Room {self.name}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}, "
            f"id={self.id}, "
            f"hotel_id={self.hotel_id}, "
            f"name={self.name}, "
            f"description={self.description}, "
            f"price={self.price}, "
            f"services={self.services}, "
            f"quantity={self.quantity}, "
            f"image_id={self.image_id}, "
        )

    def todict(self):
        """
        Приведение модели к словарю.
        :return: словарь из некоторых полей модели
        """
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "services": self.services,
            "quantity": self.quantity,
            "image_id": self.image_id,
        }

    @classmethod
    def add_id(cls, hotel_id, room):
        return {
            "hotel_id": hotel_id,
            "name": room.name,
            "description": room.description,
            "price": room.price,
            "services": room.services,
            "quantity": room.quantity,
            "image_id": room.image_id,
        }
