import orjson
from pydantic import BaseModel # pylint: disable=no-name-in-module

def orjson_dumps(v, *, default) -> str:
    # orjson.dumps returns bytes, need to decode.
    return orjson.dumps(v, default=default).decode() # pylint: disable=maybe-no-member

class OrjsonBaseModel(BaseModel):

    class Config:
        json_loads = orjson.loads # pylint: disable=maybe-no-member
        json_dumps = orjson_dumps
