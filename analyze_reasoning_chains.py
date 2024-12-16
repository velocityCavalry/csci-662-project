import argparse
import os
import re
import json
from collections import defaultdict


def parse_chains(output_dir, task):
    task_directory = os.path.join(output_dir, task)
    tool2cnt = defaultdict(int)
    number2cnt = defaultdict(int)
    for subdirectory in os.listdir(task_directory):
        output_file_path = os.path.join(task_directory, subdirectory, "output.json")
        if os.path.exists(output_file_path):
            with open(output_file_path) as f:
                data = json.load(f)

                last_result = data[-1]['content']
                thought_number = int(last_result[0]['text'].split('THOUGHT ')[1].split(':')[0])
                number2cnt[thought_number] += 1

                tools_used = []
                for i in range(len(data)):
                    if data[i]['role'] == 'assistant':
                        content_text = data[i]['content'][0]['text']
                        match = re.search(r'the \b(\w+) tool\b', content_text)
                        if match:
                            tool_name = match.group(1)
                            tools_used.append(tool_name)
                            tool2cnt[tool_name] += 1
    print(number2cnt)
    print(tool2cnt)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--task", type=str, required=True)
    args = parser.parse_args()
    parse_chains(args.output_dir, args.task)


if __name__ == '__main__':
    main()
