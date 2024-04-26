import openai
import json

def askgpt(user: str, system: str = None, model: str = 'gpt-4-turbo', **kwargs):
    msgs = []
    if system: msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    c = openai.chat.completions.create(model=model, messages=msgs, **kwargs)
    return c.choices[0].message.content

def askgptvision(user: str, img_url: str, system: str = None, model: str = 'gpt-4-turbo', **kwargs):
    msgs = []
    if system: msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": [
                {"type": "text", "text": user},
                {"type": "image_url", "image_url": {"url": img_url}},
            ]})
    c = openai.chat.completions.create(model=model, messages=msgs, response_format={"type": "json_object"}, **kwargs)
    return c.choices[0].message.content

def getjson(outline: str):
    if outline.startswith("```json"):
        outline = outline[8:-4]
    return json.loads(outline)