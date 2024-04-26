import json
from step1_schema import Outline

step1_system_prompt= """
You are a mathematically skilled poster designer. The user will give you the requirements for creating a poster.
Your job is to create an outline of a poster in the json format.

A poster outline has the following important info:
1. The dimensions (width and height) of the poster. It should always be in pixels.
2. The theme of the poster which describes the purpose of the poster and the overall visual style of the poster.
3. The color scheme to be used in the poster. If the user has not provided any details, then you have to suggest this.
4. The font theme which will match the vibe of the poster. Posters can have different vibes like Modern, Retro, Professional, Handwritten, Abstract, Vintage, Calligraphic, etc.

Additionally, the poster outline will also contain a list of elements.
Each of the elements will have a name and a description.
The name of the element will suggest the purpose: like title, subtitle, venue, date, time, CTA, foreground image, background image, logo, etc.
The elements are usually of two types: Image and Text.
For the Text elements, the description of the element will contain the exact content of the text.
For the Image elements, the description of the element will contain the detailed textual description of the visuals in the image.
Some elements can have an asset (file) associated with it. The user will provide a list of assets which can be attached to an element.
The user can also provide specific design instructions for individual elements. You need to capture this as the style of the element.

HERE ARE YOUR CONSTRAINTS:
1. DO NOT ADD ANY ELEMENT WHICH USER HAS NOT MENTIONED.
2. DO NOT MERGE MULTIPLE ELEMENTS INTO ONE ELEMENT. CREATE SEPARATE ELEMENTS.
2. DO NOT CREATE SEPARATE ELEMENTS JUST FOR AN ASSET. FIND THE RIGHT TEXT ELEMENT TO WHICH THE ASSET CAN BE ATTACHED.

Respond with only valid JSON conforming to the following schema:
"""+json.dumps(Outline.model_json_schema(), indent=2)

step1_user_prompt_1 = """
Design a poster for a Salsa Social Event for Instagram. The event is titled Mucho Mambo.
It is happening on Thursday 9PM to 12 PM At Buffalo Wild Wings, Indiranagar.
The event is organised by Palladium Dance Company.
Please use a Golden starry theme for the background and in the foreground use a real photograph of a couple doing salsa.

You can use the assets:
mucho_mambo_logo.png
palladium_dance_company_logo.png
buffalo_wild_wings_logo.png
"""

classifier_prompt = """
The user will give a json description of an element within a poster. You need to identify if the element is describing an image or a text.
If it is an image, reply "image", else reply "text"."""