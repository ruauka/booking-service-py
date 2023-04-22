from typing import Optional, Any, List
from pydantic import BaseModel, Json


class HotelRequest(BaseModel):
    name: str
    location: str
    services: Optional[List[str]]
    rooms_quantity: int
    image_id: Optional[int]


class HotelResponse(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True
