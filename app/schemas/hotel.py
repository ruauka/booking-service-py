from typing import Optional, Any, List
from pydantic import BaseModel, Json


class HotelRequest(BaseModel):
    name: str
    location: str
    services: Optional[List[str]]
    rooms_quantity: int
    image_id: Optional[int]


class HotelUpdateRequest(BaseModel):
    name: Optional[str]
    location: Optional[str]
    services: Optional[List[str]]
    rooms_quantity: Optional[int]
    image_id: Optional[int]

    def is_empty(self) -> bool:
        return not any(vars(self).values())


class HotelResponse(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True
