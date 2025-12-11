from typing import Annotated

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


"""
This example demonstrates how to use FastAPI to define path, query and body parameters.
First, of course, you can mix Path, Query and request body parameter declarations freely and FastAPI will know 
what to do.
Expected body example:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
"""
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


class User(BaseModel):
    username: str
    full_name: str | None = None

"""
You can also declare multiple body parameters, e.g. item and user.
In this case, FastAPI will notice that there is more than one body parameter in the function (there are two parameters 
that are Pydantic models).
So, it will then use the parameter names as keys (field names) in the body, and expect a body like:
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
"""
@app.put("/items/{item_id}/multiple_body/")
async def update_item_multiple_body(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

"""
You could decide that you want to have another key importance in the same body, besides the item and user.
If you declare it as is, because it is a singular value, FastAPI will assume that it is a query parameter.
But you can instruct FastAPI to treat it as another body key using Body
Expected body example:
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
"""
@app.put("/items/{item_id}/single_body_param/")
async def update_item_single_body_param(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
