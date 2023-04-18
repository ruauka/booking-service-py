from app.storage.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey


class Room(Base):
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    def __str__(self):
        return (
            f"{self.__class__.__name__}, "
            f"(id={self.id}, "
            f"(hotel_id={self.hotel_id}, "
            f"(name={self.name}, "
            f"(description={self.description}, "
            f"(price={self.price}, "
            f"(services={self.services}, "
            f"(quantity={self.quantity}, "
            f"(image_id={self.image_id}, "
        )

    def __repr__(self):
        return str(self)
