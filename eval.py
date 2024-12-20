import json
import os
import re

import requests


# dir = "./math_outputs"
dir = "./outputs_0513"
EVAL_BASELINE = False

API_KEY = "YOUR_API_KEY"


def gpt_parser(ground_truth, answer):
    prompt = """You will be given two paragraphs, one ground truth and one response. Your task is to determine whether the response is correct or not.
    
    Instructions:
    - Review the two paragraphs carefully, as the answer is embedded in the text.
    - Compare the response to the ground truth.
    - Respond with 'true' or 'false' on whether the response is correct.
    - Only compare the numerical answer, not the entire text.
    
    Rules:
    - No explanations or qualifiers allowed.
    
    Ground Truth:
    {}
    
    Response:
    {}
    
    Required format: One word, either "true" or "false", no explanation.
    Answer:
    """

    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt.format(ground_truth, answer)}],
    }

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    result = resp.json()["choices"][0]["message"]["content"]
    return result


def eval_task(task_name, dir):
    output_name = "baseline_output.json" if EVAL_BASELINE else "output.json"
    with open(os.path.join(dir, output_name), "r") as f:
        output = json.load(f)

    if task_name == "geometry":
        with open(os.path.join(dir, "ex.json"), "r") as f:
            task = json.load(f)
        ground_truth = task["solution"]
        if EVAL_BASELINE:
            answer = output["choices"][0]["message"]["content"]
        else:
            answer = output[-1]["content"][-1]["text"]

        judgement = gpt_parser(ground_truth, answer)
        if "true" not in judgement.lower():
            print(dir, judgement)
        return "true" in judgement.lower()

    ground_truth = "request" if task_name == "blink" else "example"
    with open(os.path.join(dir, f"{ground_truth}.json"), "r") as f:
        ground_truth = json.load(f)

    answer_key = "answer" if task_name == "blink" else "label"
    answer = ground_truth[answer_key]

    if task_name == "blink":
        if EVAL_BASELINE:
            pred_text = output["choices"][0]["message"]["content"]
        else:
            pred_text = output[-1]["content"][-1]["text"]
        pred_matches = re.findall(r"(\(.*?\))", pred_text)
    else:
        pred_text = (
            output["choices"][0]["message"]["content"]
            if EVAL_BASELINE
            else output[-1]["content"][-1]["text"]
        )
        pred_matches = re.findall(r"ANSWER: (.*)\. ", pred_text)

    if pred_matches:
        pred = pred_matches[-1]
        return pred == answer

    print(dir, "No answer found", answer, pred_text)
    return False


# for task in os.listdir(dir):
#     correct_count = 0
#     total_count = 0
#     task_name = task.split("_")[0]

task = "blink_depth"
correct_count = 0
total_count = 0
task_name = task.split("_")[0]
for entry in os.listdir(os.path.join(dir, task)):
    correct_count += eval_task(task_name, os.path.join(dir, task, entry))
    total_count += 1
print(f"{task} accuracy: {correct_count / total_count}")

# print(
#     gpt_parser(
#         "The first few prime numbers are: $2, 3, 5, 7, 11, 13, 17,\\ldots$.  Since the triangle is scalene, all the sides are different primes.\n\nIf one side is 2, then the other two sides must be odd.  Then the perimeter of the triangle would be even.  But the perimeter must also be greater than 2, so it cannot be prime.  This means that none of the sides can be 2.\n\nNow, suppose one side is 3.  Let the other two sides be $p$ and $q,$ where $p < q.$  Since all the sides are different,\n\\[3 < p < q.\\]Also, by the Triangle Inequality, $p + 3 > q,$ so\n\\[p > q - 3.\\]Since $p < q,$ the only possible values of $p$ are $q - 2$ and $q - 1.$\n\nSince $p$ is a prime greater than 3, $p$ is odd.  If $p = q - 1,$ then $q = p + 1$ is even, which means $q$ is not prime.  Therefore, $p = q - 2,$ or\n\\[q = p + 2.\\]As a number, $p$ must be of the form $3k,$ $3k + 1,$ or $3k + 2.$  Since $p$ is prime, $p$ cannot be of the form $3k.$  If $p = 3k + 1,$ then $q = p + 2 = 3k + 3 = 3(k + 1),$ which is not prime.  Therefore, $p = 3k + 2.$  Then $q = p + 2 = 3k + 4,$ and the perimeter of the triangle is\n\\[p + q + 3 = (3k + 2) + (3k + 4) + 3 = 6k + 9 = 3(2k + 3).\\]Since this is divisible by 3, the perimeter cannot be prime.  This tells us that none of the sides can be equal to 3 either.\n\nNote that $5 + 7 + 11 = 23$ is prime, so the smallest possible perimeter is $\\boxed{23}.$",
#         "# THOUGHT 2:\nThe smallest possible perimeter of a scalene triangle with side lengths that are prime numbers and whose perimeter is also a prime number has been found to be 23, with side lengths 5, 7, and 11. The diagram has been successfully generated to visualize the triangle.\n\n# ACTION 2:\nNo further action is needed as the problem has been solved.\n\nANSWER: The smallest possible perimeter of a scalene triangle with side lengths that are prime numbers and whose perimeter is also a prime number is 23, with side lengths 5, 7, and 11. TERMINATE",
#     )
# )
