from typing import Optional, Any, List
from pydantic import BaseModel, Json
from datetime import date


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
