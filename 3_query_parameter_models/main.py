from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

"""
If you have a group of query parameters that are related, you can create a Pydantic model to declare them.
This would allow you to re-use the model in multiple places and also to declare validations and metadata for 
all the parameters at once.
"""
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

class FilterParamsRestricted(BaseModel):
    """
    If a client tries to send some extra data in the query parameters, they will receive an error response.
    For example, if the client tries to send a tool query parameter with a value of plumbus, like:
    https://example.com/items/?limit=10&tool=plumbus
    They will receive an error response telling them that the query parameter tool is not allowed.
    """
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

@app.get("/items/restricted/")
async def read_items_restricted(filter_query: Annotated[FilterParamsRestricted, Query()]):
    return filter_query