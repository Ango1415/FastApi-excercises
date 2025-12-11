from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Image(BaseModel):
    url: str
    name: str


class ItemNested(BaseModel):
    """
    Each attribute of a Pydantic model has a type. But that type can itself be another Pydantic model.
    So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations.
    All that, arbitrarily nested.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


class Item(BaseModel):
    """
    When we think about it, and realize that tags shouldn't repeat, they would probably be unique strings.
    And Python has a special data type for sets of unique items, the set.
    Then we can declare tags as a set of strings:
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.put("/items/{item_id}/nested")
async def update_item_nested(item_id: int, item: ItemNested):
    """
    FastAPI would expect a body similar to:
    {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2,
        "tags": ["rock", "metal", "bar"],
        "image": {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        }
    }
    Note that the image attribute is itself an object with a specific structure.
    """
    results = {"item_id": item_id, "item": item}
    return results