from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config import settings
from .repository import UserRepository
from app.database import get_db
from .schemas import UserCreate, User, Token, UserLogin
from .service import create_access_token, get_current_user
from .utils import verify_password

router = APIRouter(tags=["users"])


@router.post(
    "/register",
    response_model=User,
    responses={
        400: {"description": "Email already registered"},
        500: {"description": "Internal server error"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Returns:
    - User object if successful
    - 400 error if email exists
    - 500 error for server issues
    """
    try:
        user_repo = UserRepository(db)

        # Check if email exists
        if user_repo.get_user_by_email(email=user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Email already registered",
                    "code": "EMAIL_EXISTS",
                    "message": "This email address is already in use",
                },
            )

        # Create new user
        db_user = user_repo.create_user(user)
        return db_user

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Registration failed",
                "code": "REGISTRATION_ERROR",
                "message": "Could not complete registration",
            },
        ) from e


# Consolidated login function for swagger and direct client call to avoid code duplication
def get_login_token(email: str, password: str, db: Session):
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return access_token


@router.post("/login/form", response_model=Token)
def login_user_form(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    access_token = get_login_token(form_data.username, form_data.password, db)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    try:
        access_token = get_login_token(user_login.email, user_login.password, db)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong") from e


@router.get("/me", response_model=User)
def read_current_user(current_user: User = Depends(get_current_user)):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong") from e
