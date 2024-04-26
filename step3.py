import json
import os
import shutil
from midjourney.automate_midjourney import call_midjourney

with open('config.json', 'r') as f:
    config = json.load(f)

if __name__ == "__main__":
    with open(config['STEP2_OUTPUT_FILE'], 'r') as f:
        step2_response = json.load(f)
    output_folder = os.path.join(config['STEP3_OUTPUT_FOLDER'])
    image = step2_response['poster_image']
    prompt = "Create a poster: " + image['prompt']
    call_midjourney(prompt, image['width'], image['height'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with open(config['MIDJOURNEY_OUTPUT_FILE']) as file:
        lines = [line.rstrip() for line in file]
        image['urls'] = lines
    for j, image_file in enumerate(os.listdir(config['MIDJOURNEY_OUTPUT_FOLDER'])):
        if image_file.endswith(".png"):
            src_file_path = os.path.join(config['MIDJOURNEY_OUTPUT_FOLDER'], image_file)
            dest_file_path = os.path.join(output_folder, f"{j}.png")
            shutil.copyfile(src_file_path, dest_file_path)
    with open(config['STEP3_OUTPUT_FILE'], 'w') as f:
        json.dump(step2_response, f, indent=4)