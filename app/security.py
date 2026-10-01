import os
import time
import uuid

import jwt

API_KEY = os.environ["API_KEY"]
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"
JWT_TTL_SEC = 300


def create_jwt(ttl: int = JWT_TTL_SEC) -> str:
    """Genera un JWT unico por transaccion (jti aleatorio) que dura ttl segundos."""
    now = int(time.time())
    claims = {"jti": str(uuid.uuid4()), "iat": now, "exp": now + ttl}
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt(token: str) -> dict:
    claims = jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
        options={"require": ["exp", "jti"]},
    )
    return claims
