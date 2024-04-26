from utils import askgpt, getjson
from step2_prompts2 import step2_system_prompt
import json

with open('config.json', 'r') as f:
    config = json.load(f)

if __name__ == "__main__":
    with open(config['STEP1_OUTPUT_FILE'], 'r') as f:
        step1_response = json.load(f)
    llm_output = askgpt(json.dumps(step1_response), system=step2_system_prompt)
    step2_response = getjson(llm_output)
    with open(config['STEP2_OUTPUT_FILE'], 'w') as f:
        json.dump(step2_response, f, indent=4)
