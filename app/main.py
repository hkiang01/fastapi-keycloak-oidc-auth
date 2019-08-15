import json
import logging

import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.responses import RedirectResponse

BASE_URL = "http://localhost:8000/"
AUTH_LOGIN_URL = "http://localhost:8080/auth/realms/Clients/protocol/openid-connect/auth?client_id=app&response_type=code"


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()


@app.get("/login")
async def login():
    return RedirectResponse(AUTH_LOGIN_URL)


@app.get("/auth")
async def auth(code: str):
    url = "http://localhost:8080/auth/realms/Clients/protocol/openid-connect/token"

    payload = (
        f"grant_type=authorization_code&code={code}"
        f"&redirect_uri={BASE_URL}&client_id=app"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code != 200:
        return HTTPException(
            status_code=response.status_code, detail=response.content
        )

    body = json.loads(response.content)
    access_token = body["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    response = RedirectResponse(url="/", headers=headers)
    response.set_cookie("Authorization", value=f"Bearer {access_token}")
    return response


@app.get("/")
async def root(request: Request,):
    authorization: str = request.cookies.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)
    logger.debug(f"credentials: {credentials}")
    return {"message": "You're logged in!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, loop="asyncio")
