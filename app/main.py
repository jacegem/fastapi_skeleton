import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from app.routers import users
from app.routers import items

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http:localhost",
    "http:localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

    # kwargs['greeting'] = 'hello'


app.include_router(users.router)
app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header),
    #               Depends(token)],
    responses={404: {"description": "Not found"}},
)


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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
