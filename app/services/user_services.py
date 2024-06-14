from typing import Optional

from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import get_password_hash, verify_password
from app.services.base import BaseServices


class UserServices(BaseServices[models.User]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[models.User]:
        user = db.query(self.model).filter(self.model.email == email).first()
        return user

    def authenticate_by_email(
        self, db: Session, *, email: str, password: str
    ) -> Optional[models.User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def register(self, db: Session, *, obj_in: schemas.UserRegisterByEmail) -> models.User:

        db_obj = models.User(
            hashed_password=get_password_hash(obj_in.password),
            email=obj_in.email,
            is_active=False,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = UserServices(models.User)
