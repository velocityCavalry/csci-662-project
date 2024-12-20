# CSCI 662 Project - Visual Sketchpad

This repo contains our reproduction effort of the paper "[Visual Sketchpad: Sketching as a Visual Chain of Thought for Multimodal Language Models](https://arxiv.org/abs/2406.09403)"
We modify [the original codebase](https://github.com/Yushi-Hu/VisualSketchpad) and instructions to make it more user-friendly and reproducible, and add the baseline code and evaluation script.

# Main Result

| Model                  | Setup / Task | Spatial     | Depth        | Jigsaw      | Math Parity  | Math Convexity |
| ---------------------- | ------------ | ----------- | ------------ | ----------- | ------------ | -------------- |
| **GPT-4o**             | Reported     | 76.9        | 75.0         | 62.0        | 86.5         | 92.6           |
| **Sketchpad + GPT-4o** | Reported     | 79.7 (+2.8) | 83.9 (+8.9)  | 70.0 (+8)   | 91.7 (+5.2)  | 93.8 (+1.3)    |
| ** Llava-v1.5-7B**     | Reported     | 61.5        | 52.4         | 11.3        | -            | -              |
| **GPT-4o**             | Observed     | 72.0        | 71.8         | 64.0        | 84.4         | 87.2           |
| **Sketchpad + GPT-4o** | Observed     | 81.1 (+9.1) | 83.9 (+12.1) | 70.7 (+6.7) | 94.7 (+10.3) | 94.9 (+7.7)    |
| ** Llava-v1.5-7B**     | Observed     | 59.4        | 58.0         | 52.7        | -            | -              |

The reproduction results and the reported results for each task in accuracy. The numbers in the parentheses are the improvement of sketchpad over the GPT-4o baseline. For the visualization, please see our report or run `python plot.py` to render the figure.

# Installation

Install the agent environment as follows:

```bash
conda create -n sketchpad python=3.9

pip install pyautogen==0.2.26
pip install 'pyautogen[jupyter-executor]'
pip install Pillow joblib matplotlib opencv-python numpy gradio gradio_client networkx scipy datasets
```

Set up your OpenAI API key in your environment, or in `agent/config.py` by edit the following:

```python
os.environ['OPENAI_API_KEY'] = '[YOUR OPENAI API KEY]'
```

Above is all it needs for math and geometry tasks.

### Installing vision experts for computer vision tasks

For computer vision tasks, you also need to install the vision experts.
In this code base, each vision expert is a gradio server. You can set them up in other servers, and access them through web link. This allows you to run sketchpad agents on your computer, while all vision models running on another GPU server.
Follow `vision_experts/installation.md` to install and launch all the vision experts.

After the server is launched, please edit the gradio servers link in `agent/config.py`. Change the server addresses to yours.

```python
SOM_ADDRESS = "[YOUR SOM SERVER ADDRESS]"
GROUNDING_DINO_ADDRESS = "[YOUR GroundingDINO SERVER ADDRESS]"
DEPTH_ANYTHING_ADDRESS = "[YOUR Depth-Anything SERVER ADDRESS]"
```

# Running the experiments

### 1. Data + Preprocessing

The preprocessed data by the original author is in this [Google Drive Link](https://drive.google.com/file/d/1qtbfI7Q9B7pq-WR20q0-OE6OetJqoitS/view?usp=sharing). Please download, unzip, and put the content in the `tasks` folder. Each instance in each task has a separate folder.

### 2. Run the agent

To run each task, do

```bash
cd agents
python run_task.py --task {blink_spatial, blink_jigsaw, blink_depth, math_convexity, math_parity} --output_dir {your output directory}
```

To run our baseline code of GPT-4o, add the `--baseline` flag to the above command, the corresponding method is in `agent/baseline.py`. This will run the whole task and save all execution traces to `{your output directory}`.

### 3. Run the Llava model for the BLINK dataset

We write the baseline code based on [the reference GPT4v implementation of BLINK](https://github.com/zeyofu/BLINK_Benchmark).

### 4. Run experiments on the new MATH dataset

```bash
cd agents
python run_task.py --task geometry_new --output_dir {your output directory}
```

To run the baseline code of GPT-4o, add the `--baseline` flag to the above command.

#### Installation

Install vllm by `pip install vllm`, our vllm version is `0.6.3.post1` and `transformers==4.47.0`. The pretrained Llava model can be obtained [here on huggingface](https://huggingface.co/llava-hf/llava-1.5-7b-hf).

#### Run the model

To run the Llava-v1.5-7B model on the BLINK validation set, do

```bash
cd blink_baseline
python test_benchmark.py --task_name {Relative_Depth, Jigsaw, Spatial_Relation} --model_name llava7b --output_save_folder {your output directory}
```

The implementation of the inference of the llava model is in `blink_baseline/query_model.py/query_llava_7b` and `vllm` initialization. The output is saved in `{output_save_folder}/{model_name}/{task_name}.json`. The prompt is in `blink_baseline/test_benchmark.py/load_prompt`.
The result accuracy will be output by the above command.

# Evaluation

To evaluate the output and calculate the accuracy of each task, do

```bash
python eval.py --output_dir {the output directory you passed in run_task.py}
```

To evaluate baseline, pass in `--eval_baseline`.

# Run the Additional Experiments

To run the additional experiments:

## Newer Version of GPT-4o

To run the 0806 version of GPT-4o, simply change `llm_config` in `agent/config.py` to

```python
llm_config={"cache_seed": None, "config_list": [{"model": "gpt-4o-2024-08-06", "temperature": 0.0, "api_key": os.environ.get("OPENAI_API_KEY")}]}
```

Then run with `--baseline` as usual. You can also run visual sketchpad with this new version of GPT-4o.

## MATH dataset

## Analysis of reasoning chains

To run the analysis of reasoning chains length for BLINK datasets, do

```bash
cd agent
python analyze_reasoning_chains.py --task {blink_spatial, blink_jigsaw, blink_depth} --output_dir {the output directory you passed in run_task.py}
```

This will read the output files and output the reasoning chain length, and the tool use distribution for the specific task.
