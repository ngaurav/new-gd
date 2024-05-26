import shutil
from utils import askgpt, getjson
from step2_prompts import step2_system_prompt
import json, os
import subprocess

with open('config.json', 'r') as f:
    config = json.load(f)

if __name__ == "__main__":
    with open(config['STEP1_OUTPUT_FILE'], 'r') as f:
        step1_response = json.load(f)
    output_folder = os.path.join(config['STEP2_OUTPUT_FOLDER'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(config['STEP3_OUTPUT_FOLDER']):
        os.makedirs(config['STEP3_OUTPUT_FOLDER'])
    i = 0
    for url in step1_response['urls']:
        fpath = os.path.join(config['STEP0_OUTPUT_FOLDER'],f"{config['STEP0_OUTPUT_PREFIX']}{i}.json")
        with open(fpath, 'r') as f:
            step1_response = json.load(f)
        system_prompt = step2_system_prompt.replace(r"<width>", str(step1_response['width'])).replace(r"<height>", str(step1_response['height']))
        llm_output = askgpt(json.dumps(step1_response['elements']), system=system_prompt)
        step2_response = getjson(llm_output)
        step2_response['poster_image'] = {
            'x': 0,
            'y': 0,
            "width": step1_response['width'],
            "height": step1_response['height'],
            "url": url
        }
        with open(config['STEP2_OUTPUT_FILE'], 'w') as f:
            json.dump(step2_response, f, indent=4)
        filepath = os.path.join(config['STEP2_OUTPUT_FOLDER'],f"{i}.json")
        with open(filepath, 'w') as f:
            json.dump(step2_response, f, indent=4)
        subprocess.call(['bash', './run_step3.sh'])
        dest_file_path = os.path.join(config['STEP3_OUTPUT_FOLDER'],f"{i}.png")
        shutil.copyfile(config['STEP3_OUTPUT_FILE'], dest_file_path)
        i = i + 1
