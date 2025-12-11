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
To declare a query parameter with a type of list, like in the example below, you need to explicitly use Query, 
otherwise it would be interpreted as a request body.
"""
@app.get("/items/list/")
async def read_items_list(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items


"""
Imagine that you want the parameter to be item-query. Like in: http://127.0.0.1:8000/items/?item-query=foobaritems
But item-query is not a valid Python variable name. The closest would be item_query. But you still need it to be 
exactly item-query. Then you can declare an alias, and that alias is what will be used to find the parameter value:
"""
@app.get("/items/alias/")
async def read_items_alias(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Custom Validation: There could be cases where you need to do some custom validation that can't be done with the 
parameters shown above. In those cases, you can use a custom validator function that is applied after the normal 
validation (e.g. after validating that the value is a str).
You can achieve that using Pydantic's 'AfterValidator' inside of Annotated.
(Pydantic also has BeforeValidator and others)
"""
from pydantic import AfterValidator
import random

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    """
    For example, this custom validator checks that the item ID starts with 'isbn-' for an ISBN book number or with
    'imdb-' for an IMDB movie URL ID
    :param id:
    :return:
    """
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/items/custom_validation/")
async def read_items_custom_validation(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    """
    These custom validators are for things that can be checked with only the same data provided in the request.
    If you need to do any type of validation that requires communicating with any external component, like a database or
    another API, you should instead use FastAPI Dependencies, you will learn about them later.
    """
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}
