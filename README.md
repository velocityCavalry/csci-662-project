# CSCI 662 Project - Visual Sketchpad

This repo contains our reproduction effort of the paper "[Visual Sketchpad: Sketching as a Visual Chain of Thought for Multimodal Language Models](https://arxiv.org/abs/2406.09403)"
We modify [the original codebase](https://github.com/Yushi-Hu/VisualSketchpad) and instructions to make it more user-friendly and reproducible, and add the baseline code and evaluation script. 
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

### Data
The preprocessed task by the original author is in this [Google Drive Link](https://drive.google.com/file/d/1qtbfI7Q9B7pq-WR20q0-OE6OetJqoitS/view?usp=sharing). Please download, unzip, and put the content in the `tasks` folder. Each instance in each task has a separate folder. 

### Run the agent
To run each task, do
```bash
cd agents
python run_task.py --task {blink_spatial, blink_jigsaw, blink_depth, math_convexity, math_parity} --output_dir {your output directory}
```
To run our baseline code of GPT-4o, add the `--baseline` flag to the above command, the corresponding method is in `agent/baseline.py`. This will run the whole task and save all execution traces to `{your output directory}`.

### Run the Llava model for the BLINK dataset
We write the baseline code based on [the reference GPT4v implementation of BLINK](https://github.com/zeyofu/BLINK_Benchmark).
#### Installation
Install vllm by `pip install vllm`, our vllm version is `0.6.3.post1` and `transformers==4.47.0`. 
#### Run the model
To run the Llava-v1.5-7B model on the BLINK validation set, do
```bash
cd blink_baseline
python test_benchmark.py --task_name {Relative_Depth, Jigsaw, Spatial_Relation} --model_name llava7b --output_save_folder {your output directory}
```
The implementation of the inference of the llava model is in `blink_baseline/query_model.py/query_llava_7b` and `vllm` initialization. The output is saved in `{output_save_folder}/{model_name}/{task_name}.json`. The prompt is in `blink_baseline/test_benchmark.py/load_prompt`.
The result accuracy will be output by the above command.

# Evaluation
To evaluate the agent, do
```bash

```

# Run the Additional Experiments
To run the additional experiments:
## Newer Version of GPT-4o
To run the 0806 version of GPT-4o, simply change `llm_config` in `agent/config.py` to 
```python
llm_config={"cache_seed": None, "config_list": [{"model": "gpt-4o-2024-08-06", "temperature": 0.0, "api_key": os.environ.get("OPENAI_API_KEY")}]}
```
Then run with `--baseline` as usual. You can also run visual sketchpad with this new version of GPT-4o.

## MATH dataset





