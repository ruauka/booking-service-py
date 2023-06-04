from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ARRAY

from app.storage.database import Base


class Hotel(Base):
    """
    Модель гостиницы.
    """
    name = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)
    services = Column(ARRAY(String(255)))
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer, unique=True)

    rooms = relationship("Room", back_populates="hotel", cascade="all, delete", passive_deletes=True)

    def __str__(self):
        return f"Отель {self.name} {self.location[:30]}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}, "
            f"id={self.id}, "
            f"name={self.name}, "
            f"location={self.location}, "
            f"services={self.services}, "
            f"rooms_quantity={self.rooms_quantity}, "
            f"image_id={self.image_id}, "
        )

    def todict(self):
        """
        Приведение модели к словарю.
        :return: словарь из некоторых полей модели
        """
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "services": self.services,
            "rooms_quantity": self.rooms_quantity,
            "image_id": self.image_id
        }
