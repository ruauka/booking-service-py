from typing import Optional, Any, List
from pydantic import BaseModel, Json


class RoomRequest(BaseModel):
    hotel_id: int
    name: str
    description: str
    price: int
    services: Optional[List[str]]
    quantity: int
    image_id: Optional[int]


class RoomResponse(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        orm_mode = True
