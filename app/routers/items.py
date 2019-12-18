from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


@router.post("/create")
async def create_item(item: Item):
    return item


@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str, x_token: str = Header(None)):
    # print(Header(...))
    print(x_token)
    return {"name": "Fake Specific Item", "item_id": item_id}


@router.get("/items/{item_id}")
async def read_item(item_id: str, q: str = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@router.put(
    "/{item_id}",
    operation_id="PUT /items/{item_id}",
    description="## decription of update_item",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    """
    not effect? decription of update_item
    :param item_id:
    :return:
    """
    if item_id != "foo":
        raise HTTPException(status_code=403, detail="You can only update the item: foo")
    return {"item_id": item_id, "name": "The Fighters"}
