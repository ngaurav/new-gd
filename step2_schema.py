from pydantic import BaseModel, Field
from typing import List


class Asset(BaseModel):
    x: int
    y: int
    width: int
    height: int
    asset_uri: str

class Text(BaseModel):
    x: int
    y: int
    font_size: int
    font_family: str
    content: str

class Poster(BaseModel):
    assets: List[Asset]
    texts: List[Text]
