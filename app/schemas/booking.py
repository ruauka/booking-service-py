from typing import Optional, Any, List
from pydantic import BaseModel, Json
from datetime import date


class BookingUpdateRequest(BaseModel):
    room_id: Optional[int]
    date_from: Optional[date]
    date_to: Optional[date]

    def is_empty(self) -> bool:
        return not any(vars(self).values())


class BookingResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:
        orm_mode = True
