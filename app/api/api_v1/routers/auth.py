from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, services
from app.api import deps
from app.constants.errors import Error
from app.core import security
from app.core.exception import raise_http_exception

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/token-swagger', response_model=schemas.Token)
def login_access_token_swagger(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = services.user.authenticate_by_email(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise_http_exception(Error.USER_PASS_WRONG_ERROR)
    elif not user.is_active:
        raise_http_exception(Error.INACTIVE_USER)

    return security.create_token(user=user)
