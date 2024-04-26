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
            el['aspect_ratio'] = str(round(img.width/img.height, 2))
        else:
            el['type'] = 'text'
    output_folder = os.path.join(config['STEP1_OUTPUT_FOLDER'])
    # TODO: Remove temporary hack
    out['urls'] = [
        "https://cdn.discordapp.com/attachments/1224586563510468619/1233344295852048446/gd_superagi_98661_Create_a_poster_Golden_starry_theme_backgroun_231ee637-294b-4df1-8379-cf854125208a.png?ex=662cc0e2&is=662b6f62&hm=041109bf390b224d8c8633d83e555f4a0c1e82202ff45fc7b123c045b669d3b0&",
        "https://cdn.discordapp.com/attachments/1224586563510468619/1233344308917309520/gd_superagi_98661_Create_a_poster_Golden_starry_theme_backgroun_edc0dd12-f6d0-46e1-a874-2c172b288444.png?ex=662cc0e5&is=662b6f65&hm=18b50c10666768098757dee1d5368eb53b18c7bdbf6185bb4fdcf2b16c39894e&",
        "https://cdn.discordapp.com/attachments/1224586563510468619/1233344322485751878/gd_superagi_98661_Create_a_poster_Golden_starry_theme_backgroun_eda48be6-d73e-4e09-bd9a-72fc1c446fa7.png?ex=662cc0e8&is=662b6f68&hm=7078b5be642cbfab0fbb579edd5f80391af9562596220c110496bf442a668e23&",
        "https://cdn.discordapp.com/attachments/1224586563510468619/1233344338281500695/gd_superagi_98661_Create_a_poster_Golden_starry_theme_backgroun_f86f91d1-7fb5-46c5-aaf9-ef2a84750282.png?ex=662cc0ec&is=662b6f6c&hm=2aeffe5a5f5af0d10a407c2fe7ebee749342a7e16768557b5ef45f5d1221a17c&"
    ]
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
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
    llm_output = askgpt(step1_user_prompt_1, system=step1_system_prompt)
    step1_response_1 = step1_post_process(llm_output)
    with open(config['STEP1_OUTPUT_FILE'], 'w') as f:
        json.dump(step1_response_1, f, indent=4)
