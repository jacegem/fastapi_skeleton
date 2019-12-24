from fastapi import APIRouter


router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    print('in users')

    db = main.client['test-database']
    collection = db.test_collection
    print(collection)

    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
