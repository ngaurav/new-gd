import json, os

with open('config.json', 'r') as f:
    config = json.load(f)

if __name__ == "__main__":
    with open(config['STEP1_OUTPUT_FILE'], 'r') as f:
        step1_response = json.load(f)
    output_folder = os.path.join(config['STEP0_OUTPUT_FOLDER'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    title_placement_x = ['center', 'center', 'center', 'center']
    title_placement_y = ['top', 'slightly above center', 'center', 'slightly below center']
    subtitle_placement_x = ['center', 'center', 'center', 'center']
    subtitle_placement_y = ['below title', 'below title', 'below title', 'below title']
    other_placement_x = ['left', 'right', 'left', 'right']
    other_placement_y = ['bottom', 'bottom', 'top', 'top']
    for i in range(4):
        output_file = os.path.join(config['STEP0_OUTPUT_FOLDER'],f"step1_output{i}.json")
        count = 0
        for element in step1_response['elements']:
            if element['prominence'] == 'high':
                count += 1
                element['tag'] = 'title'
                element['placement_x'] = title_placement_x[i]
                element['placement_y'] = title_placement_y[i]
        if count <=1:
            for element in step1_response['elements']:
                if element['prominence'] == 'medium' and element['type'] == 'text':
                    element['tag'] = 'subtitle'
                    element['placement_x'] = subtitle_placement_x[i]
                    element['placement_y'] = subtitle_placement_y[i]
        j = 0
        for element in step1_response['elements']:
            if not 'placement_x' in element:
                element['placement_x'] = other_placement_x[j]
                element['placement_y'] = other_placement_y[j]
                j = j + 1
            if 'placement' in element:
                del element['placement']
            if 'style' in element:
                del element['style']
        with open(output_file, 'w') as f:
            json.dump(step1_response, f, indent=4)
    