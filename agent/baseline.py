import base64
import json
import os
import shutil
from openai import OpenAI
import openai
from utils import custom_encoder
from prompt import GeoPrompt, MathPrompt
from config import llm_config


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def run_baseline(task_input, output_dir, task_type="vision", task_name=None):
    print("Running baseline model")
    assert task_type in ["vision", "math", "geo"]

    # create a directory for the task
    task_input = task_input.rstrip("/")
    task_directory = os.path.join(output_dir, os.path.basename(task_input))

    # copy the task input to the output directory
    os.makedirs(output_dir, exist_ok=True)
    shutil.copytree(task_input, task_directory, dirs_exist_ok=True)

    if task_type == "vision":
        task_metadata = json.load(open(os.path.join(task_input, "request.json")))
        query = task_metadata["query"]
        images = task_metadata["images"]

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": query + "\nRule: Give the shortest answer possible.",
                    },
                ]
                + [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(image)}"
                        },
                    }
                    for image in images
                ],
            }
        ]

    elif task_type == "math":
        query = json.load(open(os.path.join(task_input, "example.json")))
        images = []
        prompt_generator = MathPrompt(task_name, baseline=True)
        messages = [
            {
                "role": "user",
                "content": prompt_generator.initial_prompt(query, len(images)),
            }
        ]
    elif task_type == "geo":
        query = json.load(open(os.path.join(task_input, "ex.json")))
        images = []
        prompt_generator = GeoPrompt(baseline=True)
        messages = [
            {
                "role": "user",
                "content": prompt_generator.initial_prompt(query, len(images)),
            }
        ]
        print(messages)

    client = OpenAI(api_key=llm_config["config_list"][0]["api_key"])
    model_ver = llm_config["config_list"][0]["model"]
    print(model_ver)
    resp = client.chat.completions.create(
        messages=messages,
        model=model_ver,
        temperature=llm_config["config_list"][0]["temperature"],
    )

    resp_json = json.loads(resp.model_dump_json())
    with open(os.path.join(task_directory, "baseline_output.json"), "w") as f:
        json.dump(resp_json, f, indent=4, default=custom_encoder)
