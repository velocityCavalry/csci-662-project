import argparse
import json
import os
import re


def eval_task(task_name, dir, eval_baseline=False):
    output_name = "baseline_output.json" if eval_baseline else "output.json"
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
            if eval_baseline
            else output[-1]["content"][-1]["text"]
        )
        pred_match = re.search(r"ANSWER: (.*)\. ", pred_text)

    if pred_match:
        pred = pred_match.group(1)
        return pred == answer

    raise ValueError("No answer found", answer, pred_text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, required=True) # "./agent/outputs"
    parser.add_argument("--eval_baseline", action="store_true")
    args = parser.parse_args()

    for task in os.listdir(args.output_dir):
        correct_count = 0
        total_count = 0
        task_name = task.split("_")[0]
        for entry in os.listdir(os.path.join(args.output_dir, task)):
            correct_count += eval_task(task_name, os.path.join(args.output_dir, task, entry),
                                       eval_baseline=args.eval_baseline)
            total_count += 1
        print(f"{task} accuracy: {correct_count / total_count}")


if __name__ == "__main__":
    main()