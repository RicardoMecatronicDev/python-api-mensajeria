import hmac

import jwt
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas import Message
from app.security import API_KEY, decode_jwt

app = FastAPI(title="DevOps", docs_url=None, redoc_url=None, openapi_url=None)

# jti ya usados (anti-replay). En memoria: por replica.
seen_jtis: set[str] = set()


@app.exception_handler(StarletteHTTPException)
async def http_error(_: Request, exc: StarletteHTTPException):
    return PlainTextResponse("ERROR", status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError):
    return JSONResponse({"detail": "ERROR"}, status_code=422)


def _unauthorized() -> PlainTextResponse:
    return PlainTextResponse("ERROR", status_code=401)


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}


@app.post("/DevOps")
async def devops(
    body: Message,
    x_parse_rest_api_key: str | None = Header(default=None),
    x_jwt_kwy: str | None = Header(default=None),
):
    if not x_parse_rest_api_key or not hmac.compare_digest(x_parse_rest_api_key, API_KEY):
        return _unauthorized()
    if not x_jwt_kwy:
        return _unauthorized()
    try:
        claims = decode_jwt(x_jwt_kwy)
    except jwt.PyJWTError:
        return _unauthorized()
    if claims["jti"] in seen_jtis:
        return _unauthorized()
    seen_jtis.add(claims["jti"])
    return {"message": f"Hello {body.to} your message will be sent"}
