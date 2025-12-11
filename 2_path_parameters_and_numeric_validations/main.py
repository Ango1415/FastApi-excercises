from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],    # Path param
    q: str,                                                                             # Query param
):
    """
    This example demonstrates how to use FastAPI to define path parameters with numeric validations.
    The `item_id` path parameter is required and must be an integer between 1 and 1000 (inclusive).
    """
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results