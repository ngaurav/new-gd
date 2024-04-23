import json
import os
import shutil
from midjourney.automate_midjourney import call_midjourney

with open('config.json', 'r') as f:
    config = json.load(f)

if __name__ == "__main__":
    with open(config['step2_output_file'], 'r') as f:
        step2_response = json.load(f)
    if len(step2_response['images']) > 0:
        i = 0
        for image in step2_response['images']:
            call_midjourney(image['prompt'], image['width'], image['height'])
            if not os.path.exists(config['step3_output_folder']):
                os.makedirs(config['step3_output_folder'])
            output_folder = os.path.join(config['step3_output_folder'], f"{i}")
            with open(config['midjourney_output_file']) as file:
                lines = [line.rstrip() for line in file]
                image['urls'] = lines
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            for j, image_file in enumerate(os.listdir(config['midjourney_output_folder'])):
                if image_file.endswith(".png"):
                    src_file_path = os.path.join(config['midjourney_output_folder'], image_file)
                    dest_file_path = os.path.join(output_folder, f"{j}.png")
                    shutil.copyfile(src_file_path, dest_file_path)
            i = i + 1
    with open(config['step3_output_file'], 'w') as f:
        json.dump(step2_response, f, indent=4)