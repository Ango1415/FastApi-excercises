"""
You can declare examples of the data your app can receive. Here are several ways to do it.
That extra info will be added as-is to the output JSON Schema for that model, and it will be used in the API docs.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    In Pydantic version 2, you would use the attribute model_config, that takes a dict.
    You can set "json_schema_extra" with a dict containing any additional data you would like to show up in the
    generated JSON Schema, including examples.
    You could use the same technique to extend the JSON Schema and add your own custom extra info.
    For example, you could use it to add metadata for a frontend user interface, etc.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

class ItemNoExample(BaseModel):
    """
    No JSON schema extra example defined here.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.put("/items/{item_id}/no_example")
async def update_item_no_example(item_id: int, item: ItemNoExample):
    results = {"item_id": item_id, "item": item}
    return results

