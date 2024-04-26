from pydantic import BaseModel, Field
from typing import List

class Element(BaseModel):
    name: str = Field(..., description="title of the element")
    description: str = Field(..., description="description of the contents of the element")
    asset: str = Field(None, description="asset associated with the element")
    style: str = Field(None, description="description of the design theme related to this element")
    placement: str = Field(None, description="placement of the element in the poster")

class Outline(BaseModel):
    width: int = Field(..., description="width of the poster in pixels")
    height: int = Field(..., description="height of the poster in pixels")
    theme: str = Field(..., description="theme of the poster")
    background: str = Field(..., description="description of the background image used in the poster")
    foreground: str = Field(None, description="description of the foreground image used in the poster. This is optional.")
    color_scheme: str = Field(..., description="color schemes of the poster")
    font_theme: str = Field(..., description="the font styles, font weights, and font-sizes to match the vibe of the poster")
    elements: List[Element] = Field(..., description="list of the elements present in the poster. Do not include background image in this list.")
