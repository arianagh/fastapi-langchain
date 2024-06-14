from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import schemas, services
from app.api import deps
from app.constants.errors import Error
from app.core import utils
from app.core.exception import raise_http_exception

router = APIRouter(prefix='/user', tags=['User'])


@router.post('/register-by-email', status_code=status.HTTP_201_CREATED)
def register_user_by_email(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserRegisterByEmail,
):
    user = services.user.get_by_email(db, email=user_in.email)

    if user and user.is_active:
        raise_http_exception(Error.USER_EXIST_ERROR)
    if not utils.validate_password(user_in.password):
        raise_http_exception(Error.NOT_ACCEPTABLE_PASSWORD)
    obj_in = schemas.UserRegisterByEmail(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        password=user_in.password,
    )
    services.user.register(db, obj_in=obj_in)
    return
