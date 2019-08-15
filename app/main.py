import json
import logging
from typing import Dict

import jwt
import requests
import uvicorn
from fastapi import FastAPI
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.responses import RedirectResponse

APP_BASE_URL = "http://localhost:8000/"
KEYCLOAK_BASE_URL = "http://localhost:8080"
AUTH_URL = (
    f"{KEYCLOAK_BASE_URL}/auth/realms/Clients"
    "/protocol/openid-connect/auth?client_id=app&response_type=code"
)
TOKEN_URL = (
    f"{KEYCLOAK_BASE_URL}/auth/realms/Clients/protocol/openid-connect/token"
)


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()


@app.get("/login")
async def login() -> RedirectResponse:
    return RedirectResponse(AUTH_URL)


@app.get("/auth")
async def auth(code: str) -> RedirectResponse:
    payload = (
        f"grant_type=authorization_code&code={code}"
        f"&redirect_uri={APP_BASE_URL}&client_id=app"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_response = requests.request(
        "POST", TOKEN_URL, data=payload, headers=headers
    )

    token_body = json.loads(token_response.content)
    access_token = token_body["access_token"]

    response = RedirectResponse(url="/")
    response.set_cookie("Authorization", value=f"Bearer {access_token}")
    return response


@app.get("/")
async def root(request: Request,) -> Dict:
    authorization: str = request.cookies.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)

    decoded = jwt.decode(
        credentials, verify=False
    )  # TODO input keycloak public key as key, disable option to verify aud
    logger.debug(decoded)

    return {"message": "You're logged in!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, loop="asyncio")
