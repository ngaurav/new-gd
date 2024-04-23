import openai
import json

def askgpt(user, system=None, model='gpt-4-turbo', **kwargs):
    msgs = []
    if system: msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    c = openai.chat.completions.create(model=model, messages=msgs, **kwargs)
    return c.choices[0].message.content

def getjson(outline: str):
    if outline.startswith("```json"):
        outline = outline[8:-4]
    return json.loads(outline)