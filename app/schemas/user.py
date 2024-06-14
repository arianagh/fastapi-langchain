from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRegisterByEmail(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str
