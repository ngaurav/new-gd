from utils import askgpt, getjson
from step1_prompts import step1_system_prompt
import json, os, shutil
from os import listdir
from os.path import isfile, join
from PIL import Image
from midjourney.automate_midjourney import call_midjourney

with open('config.json', 'r') as f:
    config = json.load(f)

if __name__ == "__main__":
    output_folder = os.path.join(config['STEP2_INPUT_FOLDER'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    mypath = config['STEP1_INPUT_FOLDER']
    onlyfiles = [f for f in listdir(mypath) if (f.endswith('.json') and isfile(join(mypath, f)))]
    for file in onlyfiles:
        with open(join(mypath, file), 'r') as f:
            step1_input = json.load(f)
        retry = 0
        while retry < 3:
            llm_output = askgpt(json.dumps(step1_input['elements'], indent=2), system=step1_system_prompt)
            out = getjson(llm_output)
            if out == False:
                retry = retry + 1
            else:
                retry = 3
        with open(join(output_folder, file), 'w') as f:
            json.dump(out, f, indent=4)
