from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

"""
This example demonstrates how to use FastAPI to define query parameters with string validation.
The `q` query parameter is optional and has a maximum length constraint of 10 characters.
"""
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=10)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results