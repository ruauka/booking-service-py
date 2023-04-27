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


class RoomUpdateRequest(BaseModel):
    hotel_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    services: Optional[List[str]]
    quantity: Optional[int]
    image_id: Optional[int]

    def is_empty(self) -> bool:
        return not any(vars(self).values())


class RoomResponse(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        orm_mode = True
