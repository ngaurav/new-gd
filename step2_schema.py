from pydantic import BaseModel, Field
from typing import List


class Asset(BaseModel):
    left: int = Field(..., description="x co-ordinate of the asset in pixels")
    top: int = Field(..., description="y co-ordinate of the asset in pixels")
    width: int
    height: int
    asset_uri: str

class Text(BaseModel):
    center_x: int = Field(..., description="x co-ordinate of the center of the text in pixels")
    center_y: int = Field(..., description="y co-ordinate of the center of the text in pixels")
    font_size: int
    font_family: str
    content: str

class Poster(BaseModel):
    assets: List[Asset]
    texts: List[Text]
