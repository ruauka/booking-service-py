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

IncorrectEmailOrPasswordErr = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
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