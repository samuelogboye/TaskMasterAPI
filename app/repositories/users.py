from sqlalchemy.orm import Session
from app.auth.models import User
from app.auth.schemas import UserCreate
from app.auth.utils import get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: str):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserCreate):
        db_user = User(
            email=user.email, hashed_password=get_password_hash(user.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
