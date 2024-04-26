from utils import askgpt, getjson
from step1_prompts import step1_user_prompt_1, step1_system_prompt, classifier_prompt
import json, os, shutil
from PIL import Image
from midjourney.automate_midjourney import call_midjourney

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
            el['type'] = 'text'
    output_folder = os.path.join(config['STEP1_OUTPUT_FOLDER'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    prompt = "Create a poster: " + out['prompt']
    call_midjourney(prompt, out['width'], out['height'])
    with open(config['MIDJOURNEY_OUTPUT_FILE']) as file:
        lines = [line.rstrip() for line in file]
        out['urls'] = lines
    for j, image_file in enumerate(os.listdir(config['MIDJOURNEY_OUTPUT_FOLDER'])):
        if image_file.endswith(".png"):
            src_file_path = os.path.join(config['MIDJOURNEY_OUTPUT_FOLDER'], image_file)
            dest_file_path = os.path.join(output_folder, f"{j}.png")
            shutil.copyfile(src_file_path, dest_file_path)
    return out

if __name__ == "__main__":
    llm_output = askgpt(step1_user_prompt_1, system=step1_system_prompt)
    step1_response_1 = step1_post_process(llm_output)
    with open(config['STEP1_OUTPUT_FILE'], 'w') as f:
        json.dump(step1_response_1, f, indent=4)
