from utils import askgpt, getjson
from step1_prompts import step1_user_prompt_1, step1_system_prompt, classifier_prompt
import json
from PIL import Image

with open('config.json', 'r') as f:
    config = json.load(f)

def step1_post_process(outline: str):
    out = getjson(outline)
    for el in out['elements']:
        if 'asset' in el.keys() and el['asset']:
            img = Image.open(config['INPUT_FOLDER']+'/'+el['asset'])
            el['type'] = "asset"
            el['height'] = img.height
            el['width'] = img.width
            el['aspect_ratio'] = str(round(img.width/img.height, 2))
        else:
            el['type'] = askgpt(json.dumps(el), system=classifier_prompt, model='gpt-4-turbo')
    return out

if __name__ == "__main__":
    llm_output = askgpt(step1_user_prompt_1, system=step1_system_prompt)
    step1_response_1 = step1_post_process(llm_output)
    with open(config['STEP1_OUTPUT_FILE'], 'w') as f:
        json.dump(step1_response_1, f, indent=4)
