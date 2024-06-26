from pydantic import BaseModel, Field
from typing import List

class Element(BaseModel):
    name: str = Field(..., description="title of the element")
    description: str = Field(..., description="description of the contents of the element")
    asset: str = Field(None, description="asset associated with the element")
    prominence: str = Field(..., description="should be one of [high, medium, low]")
    instructions: str = Field(None, description="description of user instructions related to this element")

class Outline(BaseModel):
    width: int = Field(..., description="width of the poster in pixels")
    height: int = Field(..., description="height of the poster in pixels")
    theme: str = Field(..., description="theme of the poster")
    background: str = Field(..., description="description of the background image used in the poster")
    foreground: str = Field(None, description="description of the content of the foreground used in the poster. It is usually the main topic of the poster. This is optional.")
    prompt: str = Field(..., description="Prompt to create the poster image. It is combination of the background of the poster and the foreground of the poster.")
    color_scheme: str = Field(..., description="color schemes of the poster")
    font_theme: str = Field(..., description="the font styles, font weights, and font-sizes to match the vibe of the poster")
    elements: List[Element] = Field(..., description="list of the elements present in the poster. Do not include background image in this list.")
