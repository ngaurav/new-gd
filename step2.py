from utils import askgpt, getjson
from step2_prompts import step2_system_prompt
import json

with open('config.json', 'r') as f:
    config = json.load(f)

if __name__ == "__main__":
    with open(config['step1_output_file'], 'r') as f:
        step1_response = json.load(f)
    llm_output = askgpt(json.dumps(step1_response), system=step2_system_prompt)
    step2_response = getjson(llm_output)
    with open(config['step2_output_file'], 'w') as f:
        json.dump(step2_response, f, indent=4)
