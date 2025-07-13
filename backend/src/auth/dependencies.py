from typing import Annotated

from pydantic import ValidationError

from src.schemas.api.agent.schemas import AgentJWTTokenPayload
from src.models import User
from src.db.session import AsyncDBSession
from src.auth.jwt import validate_token, TokenLifespanType
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.repositories.user import user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/access-token")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is not valid or expired. Please log in again",
    headers={"WWW-Authenticate": "Bearer"},
)


async def _get_user_by_token(
    token: str, db: AsyncDBSession, lifespan_type: TokenLifespanType
):
    try:
        payload = validate_token(token, lifespan_type=lifespan_type)
        if not payload:
            raise CREDENTIALS_EXCEPTION

        if isinstance(payload, AgentJWTTokenPayload):
            id_ = payload.user_id
        else:
            id_ = payload.sub

        user = await user_repo.get(db=db, id_=id_)
        if not user:
            return None
        return user
    except ValidationError:
        return None


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncDBSession
) -> User:
    user = await _get_user_by_token(
        token=token, db=db, lifespan_type=TokenLifespanType.api
    )
    if not user:
        raise CREDENTIALS_EXCEPTION
    return user


async def get_user_by_user_or_agent_token(
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncDBSession
):
    try:
        user_by_jwt = await _get_user_by_token(
            token=token, db=db, lifespan_type=TokenLifespanType.api
        )
        user_by_agent_jwt = await _get_user_by_token(
            token=token, db=db, lifespan_type=TokenLifespanType.cli
        )

        if not any([user_by_jwt, user_by_agent_jwt]):
            raise CREDENTIALS_EXCEPTION

        if user_by_jwt:
            return user_by_jwt

        if user_by_agent_jwt:
            return user_by_agent_jwt

    except ValidationError:
        raise HTTPException(
            status_code=400,
            detail="Expected either genai user JWT token or agent JWT token. Please verify your 'Authorization' header",  # noqa: E501
        )


CurrentUserDependency = Annotated[User, Depends(get_current_user)]
CurrentUserByAgentOrUserTokenDependency = Annotated[
    User, Depends(get_user_by_user_or_agent_token)
]
