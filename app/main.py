import logging

import uvicorn
from fastapi import FastAPI

LOGIN_URL = "http://localhost:8080/auth/realms/Clients/protocol/openid-connect/auth?client_id=app&response_type=code"


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

app = FastAPI()


@app.get("/")
async def root(code: str):
    logger.debug(f"code: {code}")
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, loop="asyncio")
