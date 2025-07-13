from typing import Optional
from fastapi import Depends, Header, WebSocket, status

from src.auth.jwt import TokenLifespanType, validate_token
from src.models import User
from src.repositories.user import user_repo
from src.db.session import AsyncDBSession

import jwt


class WebSocketTokenValidator:
    async def __call__(
        self,
        websocket: WebSocket,
        db: AsyncDBSession,
        authorization: Optional[str] = Header(None),
        token: Optional[str] = None,
    ) -> Optional[User]:
        if token is None:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Invalid Authorization header format",
            )
            return None

        token = parts[1]
        try:
            payload = validate_token(token, lifespan_type=TokenLifespanType.api)
            if not payload:
                await websocket.close(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="JWT token is invalid or expired",
                )
                return None
            user = await user_repo.get(db=db, id_=payload.sub)
            if not user:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
            return user

        except jwt.ExpiredSignatureError:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None
        except jwt.DecodeError:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None


# get_current_ws_user = WebSocketTokenValidator()
# CurrentUserWSDependency = Annotated[User, Depends(get_current_ws_user)]


async def get_current_ws_user(
    websocket: WebSocket,
    db: AsyncDBSession = Depends(AsyncDBSession),
    token: Optional[str] = Header(None),
) -> Optional[User]:
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    try:
        payload = validate_token(token, lifespan_type=TokenLifespanType.api)
        if not payload:
            await websocket.close(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="JWT token is invalid or expired",
            )
            return None
        user = await user_repo.get(db=db, id_=payload.sub)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        return user

    except jwt.ExpiredSignatureError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
    except jwt.DecodeError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
