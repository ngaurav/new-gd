from pydantic import BaseModel, Field
from typing import List

class GroupElement(BaseModel):
    name: str = Field(..., description="title of the element")
    description: str = Field(..., description="description of the contents of the element")
    asset: str = Field(None, description="asset associated with the element")
    prominence: str = Field(..., description="should be one of [high, medium, low]")
    instructions: str = Field(None, description="description of user instructions related to this element")
    group: int = Field(..., description="the id of the group to which this element belongs. Should be a single digit number.")

class ElementList(BaseModel):
    elements: List[GroupElement] = Field(..., description="list of the elements present in the poster. Do not include background image in this list.")
