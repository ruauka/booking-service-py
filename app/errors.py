from fastapi import HTTPException, status

UserAlreadyExistsErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already exists",
)

InstanceAlreadyExistsErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Instance already exists",
)

UserNotFoundErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User not found",
)

NoUsersErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="No users yet",
)

IncorrectEmailOrPasswordErr = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
)

HotelAlreadyExistsErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Hotel already exists",
)

HotelNotFoundErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Hotel not found",
)

NoHotelsErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="No hotels yet",
)

RoomAlreadyExistsErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Room already exists",
)

RoomNotFoundErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Room not found",
)

NoRoomsErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="No rooms yet",
)

NoAvailableRooms = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="No available rooms",
)

NoBookingsErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="No bookings yet",
)

BookingNotFoundErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Booking not found",
)

JWTExpiredErr = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="JWT expired",
)

TokenAbsentErr = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="JWT absent",
)

IncorrectJWTFormatErr = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect JWT Format",
)

UnauthorizedUserErr = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

EmptyFieldsToUpdateErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="No fields to update",
)

NoAdminErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Yuo'r not admin",
)

DBErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Db error",
)

UnknownErr = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Unknown error",
)
