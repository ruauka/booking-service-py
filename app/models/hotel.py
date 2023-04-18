from app.storage.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Hotel(Base):
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    def __str__(self):
        return (
            f"{self.__class__.__name__}, "
            f"(id={self.id}, "
            f"(name={self.name}, "
            f"(location={self.location}, "
            f"(services={self.services}, "
            f"(rooms_quantity={self.rooms_quantity}, "
            f"(image_id={self.image_id}, "
        )

    def __repr__(self):
        return str(self)