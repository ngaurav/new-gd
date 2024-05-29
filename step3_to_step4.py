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