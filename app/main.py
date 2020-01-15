import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from app.core.config import PROJECT_NAME, ALLOWED_HOSTS, API_V1_STR
from app.db.mongodb_util import connect_to_mongo, close_mongo_connection
from app.routers import users
from app.routers import items

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.api.v1.api import router as api_router

app = FastAPI(title=PROJECT_NAME)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http:localhost",
#     "http:localhost:8080",
# ]

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

    # kwargs['greeting'] = 'hello'


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/device")
def read_root():
    a = 1 / 0
    return {"Hello": "World"}


app.include_router(api_router, prefix=API_V1_STR)


# app.include_router(users.router)
# app.include_router(
#     items.router,
#     prefix="/items",
#     tags=["items"],
#     # dependencies=[Depends(get_token_header),
#     #               Depends(token)],
#     responses={404: {"description": "Not found"}},
# )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

dsn = "https://8e4d36e41faf4dbc92cb8509fb6b1b8b@sentry.io/1882082"
sentry_sdk.init(dsn=dsn)
app = SentryAsgiMiddleware(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
