from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    """
    You can use more complex singular types that inherit from str. To see all the options you have, checkout Pydantic's
    Type Overview. You will see some examples in the next chapter. For example, as in the Image model we have a url
    field, we can declare it to be an instance of Pydantic's HttpUrl instead of a str.
    The string will be checked to be a valid URL, and documented in JSON Schema / OpenAPI as such.
    """
    url: HttpUrl
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
    #image: Image | None = None
    images: list[Image] | None = None


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


class Offer(BaseModel):
    """
    You can define arbitrarily deeply nested models:
    """
    name: str
    description: str | None = None
    price: float
    items: list[ItemNested]


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
        "tags": [
            "rock",
            "metal",
            "bar"
        ],
        "images": [
            {
                "url": "http://example.com/baz.jpg",
                "name": "The Foo live"
            },
            {
                "url": "http://example.com/dave.jpg",
                "name": "The Baz"
            }
        ]
    }
    Note that the image attribute is itself an object with a specific structure.
    """
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers/")
async def create_offer(offer: Offer):
    """
    Notice how Offer has a list of Items, which in turn have an optional list of Images
    """
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    """
    If the top level value of the JSON body you expect is a JSON array (a Python list), you can declare the type in the parameter of the function
    :param images:
    :return: None
    """
    return images

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    """
    Bodies of arbitrary dicts: You can also declare a body as a dict with keys of some type and values of some other
    type. This way, you don't have to know beforehand what the valid field/attribute names are (as would be the case
    with Pydantic models). This would be useful if you want to receive keys that you don't already know.
    :param weights: weights dictionary with integer keys and float values
    :return: weights dictionary
    """
    return weights

"""
Another useful case is when you want to have keys of another type (e.g., int).
In this case, you would accept any dict as long as it has int keys with float values
Keep in mind that JSON only supports str as keys. But Pydantic has automatic data conversion.
This means that, even though your API clients can only send strings as keys, as long as those strings contain pure 
integers, Pydantic will convert them and validate them.
And the dict you receive as weights will actually have int keys and float values.
"""