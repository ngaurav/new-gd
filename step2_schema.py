from pydantic import BaseModel, Field
from typing import List

class Image(BaseModel):
    x: int
    y: int
    width: int
    height: int
    prompt: str

class Asset(BaseModel):
    x: int
    y: int
    width: int
    height: int
    asset_uri: str

class TextBox(BaseModel):
    x: int
    y: int
    font_size: int
    font_style: str
    content: str

class Poster(BaseModel):
    assets: List[Asset]
    images: List[Image]
    texts: List[TextBox]
