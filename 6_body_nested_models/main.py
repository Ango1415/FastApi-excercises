from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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