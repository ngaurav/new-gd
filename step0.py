from utils import askgpt, getjson
from step0_prompts import step0_system_prompt
import json, os, shutil
from os import listdir
from os.path import isfile, join
from PIL import Image
from midjourney.automate_midjourney import call_midjourney

with open('config.json', 'r') as f:
    config = json.load(f)

def step0_post_process(outline: str):
    for el in out['elements']:
        if 'asset' in el.keys() and el['asset']:
            img = Image.open(config['INPUT_FOLDER']+'/'+el['asset'])
            el['type'] = "asset"
            el['aspect_ratio'] = str(round(img.width/img.height, 2))
        else:
            el['type'] = 'text'
    output_folder = os.path.join(config['STEP0_OUTPUT_FOLDER'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # prompt = "Create a poster: " + out['prompt']
    # call_midjourney(prompt, out['width'], out['height'])
    # with open(config['MIDJOURNEY_OUTPUT_FILE']) as file:
    #     lines = [line.rstrip() for line in file]
    #     out['urls'] = lines
    # for j, image_file in enumerate(os.listdir(config['MIDJOURNEY_OUTPUT_FOLDER'])):
    #     if image_file.endswith(".png"):
    #         src_file_path = os.path.join(config['MIDJOURNEY_OUTPUT_FOLDER'], image_file)
    #         dest_file_path = os.path.join(output_folder, f"{j}.png")
    #         shutil.copyfile(src_file_path, dest_file_path)
    return out

if __name__ == "__main__":
    output_folder = os.path.join(config['STEP1_INPUT_FOLDER'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    mypath = config['STEP0_INPUT_FOLDER']
    onlyfiles = [f for f in listdir(mypath) if (f.endswith('.txt') and isfile(join(mypath, f)))]
    for file in onlyfiles:
        with open(join(mypath, file), 'r') as f:
            step0_input = f.read()
        retry = 0
        while retry < 3:
            llm_output = askgpt(step0_input, system=step0_system_prompt)
            out = getjson(llm_output)
            if out == False:
                retry = retry + 1
            else:
                retry = 3
        step0_response = step0_post_process(out)
        with open(join(output_folder, file + ".json"), 'w') as f:
            json.dump(step0_response, f, indent=4)
