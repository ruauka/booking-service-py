from fastapi import HTTPException, status

UserAlreadyExistsErr = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
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

NoUserErr = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
