import enum
import jwt

from typing import Optional, Union
from datetime import timedelta, datetime
from src.core.settings import get_settings

from src.schemas.api.agent.schemas import AgentJWTTokenPayload
from src.schemas.api.auth.jwt import TokenPayload


settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
HASH_ALGORITHM = settings.HASH_ALGORITHM


class TokenLifespanType(enum.Enum):
    """
    JWT token lifespan type

    - `api` is designed to be used for **users** with API and WS endpoints of the app with token lifespan of 6 hours
    - `cli` is designed to be used for **agents** based on which the validation of the creator will occur.
    The lifespan of such token is indefinite
    """

    api = "api"
    cli = "cli"  # indefinite


def create_access_token(
    subject: str, lifespan_type: TokenLifespanType = TokenLifespanType.api, **kwargs
):
    """
    Creates an access token for authentication purposes.

    Args:
        subject (str): The subject identifier (e.g., user ID or username).
        lifespan_type (TokenLifespanType, optional): Determines the lifespan of the
    token in minutes.
            Defaults to TokenLifespanType.api.

    Returns:
        str: A JSON Web Token (JWT) encoded string containing the subject and
    expiration time.

    Note:
        The token is signed using the SECRET_KEY with the HASH_ALGORITHM.
    """
    expire = datetime.now() + timedelta(hours=6)
    if lifespan_type == TokenLifespanType.cli:
        to_encode = {"sub": subject, "exp": datetime.max, **kwargs}
        return jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=HASH_ALGORITHM)

    to_encode = {"sub": subject, "exp": expire, **kwargs}
    return jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=HASH_ALGORITHM)


def validate_token(
    token: str, lifespan_type: TokenLifespanType
) -> Optional[Union[AgentJWTTokenPayload, TokenPayload]]:
    try:
        payload: dict = jwt.decode(
            jwt=token, key=SECRET_KEY, algorithms=[HASH_ALGORITHM]
        )
        if lifespan_type == TokenLifespanType.cli:
            return AgentJWTTokenPayload(**payload)
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
