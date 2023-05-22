from sqladmin import ModelView

from app.models.user import User
from app.models.booking import Booking
from app.models.hotel import Hotel
from app.models.room import Room


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.booking]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    page_size = 20
    page_size_options = [10, 50, 100]


class HotelAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.columns] + [Hotel.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.columns] + [Room.hotel, Room.booking]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"


class BookingAdmin(ModelView, model=Booking):
    # Booking.__table__.columns - список колонок модели
    # [c.name for c in Booking.__table__.columns] - все названия колонок
    column_list = [c.name for c in Booking.__table__.columns] + [Booking.user]
    name = "Booking"
    name_plural = "Booking"
    icon = "fa-solid fa-book"
