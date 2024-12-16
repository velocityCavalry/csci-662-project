import json
import os
import shutil
from openai import OpenAI
from utils import custom_encoder
from prompt import MathPrompt
from config import llm_config


def run_baseline(task_input, output_dir, task_type="vision", task_name=None):
    assert task_type in ["vision", "math", "geo"]

    # create a directory for the task
    task_input = task_input.rstrip("/")
    task_directory = os.path.join(output_dir, os.path.basename(task_input))

    # copy the task input to the output directory
    os.makedirs(output_dir, exist_ok=True)
    shutil.copytree(task_input, task_directory, dirs_exist_ok=True)

    if task_type == "vision":
        raise NotImplementedError
    elif task_type == "math":
        query = json.load(open(os.path.join(task_input, "example.json")))
        images = []
        prompt_generator = MathPrompt(task_name, baseline=True)
    elif task_type == "geo":
        raise NotImplementedError

    client = OpenAI(api_key=llm_config["config_list"][0]["api_key"])
    model_ver = llm_config["config_list"][0]["model"]
    resp = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_generator.initial_prompt(query, len(images)),
            }
        ],
        model=model_ver,
        temperature=llm_config["config_list"][0]["temperature"],
    )

    resp_json = json.loads(resp.model_dump_json())
    with open(os.path.join(task_directory, "baseline_output.json"), "w") as f:
        json.dump(resp_json, f, indent=4, default=custom_encoder)
