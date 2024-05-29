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

#step2_to_step3
import json
import os
from typing import Dict, List
import os
import json
import shutil

def generate_grid(num_groups: int) -> List[Dict[str, int]]:
    """
    Generate a grid configuration based on the number of groups.

    Args:
        num_groups (int): The number of groups to generate the grid for.

    Returns:
        list: A list of dictionaries representing the grid configuration.

    Raises:
        ValueError: If the number of groups is not supported.
    """
    if num_groups == 1:
        return [{"cols": 2, "rows": 1}, {"cols": 1, "rows": 1}]
    elif num_groups == 2:
        return [{"cols": 2, "rows": 2}]
    elif num_groups == 3:
        return [{"cols": 3, "rows": 3}]
    else:
        raise ValueError("Unsupported number of groups")

def group_elements(elements: List[Dict]) -> Dict[int, List[Dict]]:
    """
    Group elements based on their 'group' key.

    Args:
        elements (list): A list of dictionaries representing the elements.

    Returns:
        dict: A dictionary where the keys are group IDs, and the values are lists of elements belonging to that group.
    """
    grouped_elements: Dict[int, List[Dict]] = {}
    for element in elements:
        group_id = element.get('group', 1)  # Use 1 as the default group
        grouped_elements.setdefault(group_id, []).append(element)
    return grouped_elements

def process_input(input_file: str, output_file: str) -> None:
    """
    Process the input JSON file and generate the output JSON file.

    Args:
        input_file (str): The path to the input JSON file.
        output_file (str): The path to the output JSON file.
    """
    with open(input_file, 'r') as f:
        data = json.load(f)
    elements = data.pop('elements', [])  # Remove and get 'elements' from data
    grouped_elements = group_elements(elements)
    num_groups = len(grouped_elements)
    grid = generate_grid(num_groups)
    
    # Construct output data by preserving all original properties
    output_data = data.copy()  # Copy all remaining data
    output_data['grid'] = grid
    output_data['groups'] = [{'elements': grouped_elements[group_id]} for group_id in sorted(grouped_elements)]

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

def process_all_json_files(input_directory1: str, input_directory2: str, output_directory: str) -> None:
    """
    Process all JSON files in the input directories and generate output files in the output directory.

    Args:
        input_directory1 (str): The path to the first input directory.
        input_directory2 (str): The path to the second input directory.
        output_directory (str): The path to the output directory.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for input_dir in [input_directory1, input_directory2]:
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.json'):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(output_directory, file)
                    process_input(input_file, output_file)

def copy_properties_except_elements(input_file: str, output_file: str) -> None:
    """
    Copy properties from the input file to the output file, excluding the 'elements' property.

    Args:
        input_file (str): The path to the input JSON file.
        output_file (str): The path to the output JSON file.
    """
    with open(input_file, 'r') as f:
        data = json.load(f)
        # Remove 'elements' property if it exists
        data.pop('elements', None)

    with open(output_file, 'r') as f:
        output_data = json.load(f)

    # Create a new dictionary with properties from input file first
    new_output_data = data.copy()
    new_output_data.update(output_data)

    with open(output_file, 'w') as f:
        json.dump(new_output_data, f, indent=2)

def split_grid_configurations(output_directory):
    """
    Splits JSON files with multiple grid configurations into separate files.

    Args:
        output_directory (str): The path to the output directory containing the JSON files.
    """
    for filename in os.listdir(output_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(output_directory, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)

            grids = data.get('grid', [])
            if len(grids) > 1:
                base_filename, ext = os.path.splitext(filename)
                original_data = data.copy()
                for i, grid in enumerate(grids[1:], start=1):
                    new_data = original_data.copy()
                    new_data['grid'] = [grid]
                    new_filename = f"{base_filename}_{i}{ext}"
                    new_file_path = os.path.join(output_directory, new_filename)
                    with open(new_file_path, 'w') as f:
                        json.dump(new_data, f, indent=2)

                # Remove additional grid configurations from the original file
                data['grid'] = [grids[0]]
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)


def remove_txt_from_filename(output_directory):
    """
    Removes the ".txt" substring from filenames in the output directory.

    Args:
        output_directory (str): The path to the output directory containing the files.
    """
    for filename in os.listdir(output_directory):
        if '.txt' in filename:
            src = os.path.join(output_directory, filename)
            dst = os.path.join(output_directory, filename.replace('.txt', ''))
            os.rename(src, dst)

if __name__ == "__main__":
    input_directory1 = 'step1_input'
    input_directory2 = 'step2_input'
    output_directory = 'step3_input'

    process_all_json_files(input_directory1, input_directory2, output_directory)

    for file in os.listdir(input_directory1):
        if file.endswith('.json'):
            input_file = os.path.join(input_directory1, file)
            output_file = os.path.join(output_directory, file)
            copy_properties_except_elements(input_file, output_file)

    split_grid_configurations(output_directory)
    remove_txt_from_filename(output_directory)
    
#step3_to_step4
import os
import copy
import json

def assign_groups_to_grids(groups, grid):
    assigned_groups_list = []

    for grid_config in grid:
        num_groups = len(groups)
        cols, rows = grid_config["cols"], grid_config["rows"]
        assigned_groups = []

        if num_groups == 1:
            if cols == 2 and rows == 1:
                group = copy.deepcopy(groups[0])
                group["col"] = 0
                group["row"] = 0
                assigned_groups.append([group])
            else:
                group = copy.deepcopy(groups[0])
                group["col"] = 0
                group["row"] = 0
                assigned_groups.append([group])

        elif num_groups == 2:
            if cols == 2 and rows == 2:
                # Configuration 1: Different rows
                conf1 = copy.deepcopy(groups)
                conf1[0]["col"] = 0
                conf1[0]["row"] = 0
                conf1[1]["col"] = 0
                conf1[1]["row"] = 1
                assigned_groups.append(conf1)

                # Configuration 2: Same row
                conf2 = copy.deepcopy(groups)
                conf2[0]["col"] = 1
                conf2[0]["row"] = 0
                conf2[1]["col"] = 1
                conf2[1]["row"] = 1
                assigned_groups.append(conf2)


        elif num_groups == 3:
            conf1 = copy.deepcopy(groups)
            conf1[0]["col"] = 0
            conf1[0]["row"] = 0
            conf1[1]["col"] = 0
            conf1[1]["row"] = 1
            conf1[2]["col"] = 0
            conf1[2]["row"] = 2
            assigned_groups.append(conf1)

        assigned_groups_list.extend(assigned_groups)

    return assigned_groups_list

def process_json(input_file, output_dir):
    with open(input_file, 'r') as f:
        data = json.load(f)

    grid = data.get("grid")
    groups = data.get("groups", [])

    assigned_groups = assign_groups_to_grids(groups, grid)

    for i, group_config in enumerate(assigned_groups):
        data["groups"] = group_config
        output_file = os.path.join(output_dir, f"{os.path.basename(input_file).split('.')[0]}_{i}.json")
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)

def process_all_json_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_file = os.path.join(input_dir, filename)
            process_json(input_file, output_dir)

if __name__ == "__main__":
    input_directory = 'step3_input'
    output_directory = 'step4_input'
    process_all_json_files(input_directory, output_directory)