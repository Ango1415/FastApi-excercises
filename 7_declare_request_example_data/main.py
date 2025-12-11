"""
You can declare examples of the data your app can receive. Here are several ways to do it.
That extra info will be added as-is to the output JSON Schema for that model, and it will be used in the API docs.
"""
from typing import Annotated
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

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


class ItemField(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.put("/items/{item_id}/no_example")
async def update_item_no_example(item_id: int, item: ItemNoExample):
    results = {"item_id": item_id, "item": item}
    return results

@app.put("/items/{item_id}/field_example")
async def update_item_field(item_id: int, item: ItemField):
    results = {"item_id": item_id, "item": item}
    return results

"""
examples in JSON Schema - OpenAPI: When using any of:
    Path()
    Query()
    Header()
    Cookie()
    Body()
    Form()
    File()
You can also declare a group of examples with additional information that will be added to their JSON Schemas inside 
of OpenAPI.
"""
@app.put("/items/{item_id}/multiple_body_examples/")
async def update_item_multiple_body_examples(
    item_id: int,
    item: Annotated[
        ItemNoExample,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ],
        ),
    ],
):
    """
    Here we pass examples containing one example of the data expected in Body().
    You can of course also pass multiple examples.
    :param item_id:
    :param item:
    :return:
    """
    results = {"item_id": item_id, "item": item}
    return results


"""
Using the openapi_examples Parameter: You can declare the OpenAPI-specific examples in FastAPI with the parameter
openapi_examples for:
    Path()
    Query()
    Header()
    Cookie()
    Body()
    Form()
    File()
The keys of the dict identify each example, and each value is another dict.
Each specific example dict in the examples can contain:
    summary: Short description for the example.
    description: A long description that can contain Markdown text.
    value: This is the actual example shown, e.g. a dict.
    externalValue: alternative to value, a URL pointing to the example. Although this might not be supported by as many tools as value.
You can use it like this:
"""
@app.put("/items/{item_id}/openapi-example/")
async def update_item_openapi_example(
    *,
    item_id: int,
    item: Annotated[
        ItemNoExample,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
