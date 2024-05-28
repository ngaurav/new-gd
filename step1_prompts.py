import json
from step1_schema import ElementList

step1_system_prompt= """
The user will give you a list of elements to be present in a Poster Image.
Your job is to group similar elements together.
For every element you have to specify a group id. Similar elements will have the same group id.

HERE ARE YOUR CONSTRAINTS:
1. DO NOT CREATE MORE THAN THREE GROUPS. TRY TO CREATE MINIMAL GROUPS.
2. EACH GROUP CAN HAVE A MAXIMUM OF FOUR ELEMENTS.
3. TRY TO PLACE SEMANTICALLY CONNECTED ELEMENTS IN THE SAME GROUP.

Respond with only valid JSON conforming to the following schema:
"""+json.dumps(ElementList.model_json_schema(), indent=2)
