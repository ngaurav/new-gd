import json
from step2_schema import Poster

step2_system_prompt = """
Your job is to place texts and assets (like logos) on a poster. The user will give you two things:
1. Poster Image: The background image of the poster of width <width> and height <height>
2. A list of elements to be placed on the Poster Image

For each element you have to specify some details which will be used to position them on the poster.
For every element you have to specify the position (X and Y co-ordinates) of the element in the poster.

Elements are of two types: Texts and Assets.
For assets, the aspect ratio should not be changed. The width and height must scale proportionately.
For text, you also need to specify the font_size and font_family. Pick one font_family from the following list:
["bree serif", "garamond", "jersey", "jacquard", "oswald", "merriweather", "shrikhand", "eczar", "charm", "rock salt", "dancing script", "pacifico", "caveat", "indie flower", "amatic sc", "kalam", "allura", "kaushan script", "aladin", "condiment"]

Respond with only valid JSON conforming to the following schema:
"""+json.dumps(Poster.model_json_schema(), indent=2)