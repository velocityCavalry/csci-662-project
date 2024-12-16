import json
import os
import re


# dir = "./math_outputs"
dir = "./agent/outputs"
EVAL_BASELINE = False


def eval_task(task_name, dir):
    output_name = "baseline_output.json" if EVAL_BASELINE else "output.json"
    with open(os.path.join(dir, output_name), "r") as f:
        output = json.load(f)

    ground_truth = "request" if task_name == "blink" else "example"
    with open(os.path.join(dir, f"{ground_truth}.json"), "r") as f:
        ground_truth = json.load(f)

    answer_key = "answer" if task_name == "blink" else "label"
    answer = ground_truth[answer_key]

    if task_name == "blink":
        pred_text = output[-1]["content"][-1]["text"]
        pred_match = re.search(r"(\(.*?\))", pred_text)
    else:
        pred_text = (
            output["choices"][0]["message"]["content"]
            if EVAL_BASELINE
            else output[-1]["content"][-1]["text"]
        )
        pred_match = re.search(r"ANSWER: (.*)\. ", pred_text)

    if pred_match:
        pred = pred_match.group(1)
        return pred == answer

    raise ValueError("No answer found", answer, pred_text)


for task in os.listdir(dir):
    correct_count = 0
    total_count = 0
    task_name = task.split("_")[0]
    for entry in os.listdir(os.path.join(dir, task)):
        correct_count += eval_task(task_name, os.path.join(dir, task, entry))
        total_count += 1
    print(f"{task} accuracy: {correct_count / total_count}")
