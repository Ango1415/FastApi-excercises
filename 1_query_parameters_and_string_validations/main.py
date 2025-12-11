from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

"""
This example demonstrates how to use FastAPI to define query parameters with string validation.
The `q` query parameter is optional and has a maximum length constraint of 10 characters.
and a minimum length constraint of 3 characters.
"""
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=10, min_length=3, pattern="^fixedquery$")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
This example demonstrates how to use FastAPI to define a query parameter that accepts a list of strings.
The `q` query parameter is optional and can accept multiple values that apears in the URL, for example:
http://localhost:8000/items/?q=foo&q=bar
"""
@app.get("/items/list/")
async def read_items_list(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items