## Installing dependencies for vision experts

This doc contains how to install the vision specialist models locally and then run them as gradio servers.

```bash
cd vision_experts
```

### install Semantic-SAM for segmentation
```bash
pip install git+https://github.com/UX-Decoder/Semantic-SAM.git@package
python -m pip install 'git+https://github.com/MaureenZOU/detectron2-xyz.git'

cd simplified_som

# if you are using CUDA 11.X
export TORCH_CUDA_ARCH_LIST="3.5;5.0;6.0;6.1;7.0;7.5;8.0;8.6+PTX"
# if you are using CUDA 12.X
export TORCH_CUDA_ARCH_LIST="5.0;5.2;5.3;6.0;6.1;6.2;7.0;7.2;7.5;8.0;8.6;8.7;8.9;9.0+PTX"
# install components from Deformable-DETR
cd ops && sh make.sh && cd ..

# download checkpoint
wget https://github.com/UX-Decoder/Semantic-SAM/releases/download/checkpoint/swinl_only_sam_many2many.pth

cd ..
```

If you encounter a CUDA error like we do, check whether your `CUDA_HOME` is set correctly. If not, check using `which nvcc` and set `CUDA_HOME` to the directory where `nvcc` is located. If `nvcc` is unavailable, install the correct version of CUDA toolkit (that match your pytorch installation) by running
```bash
# install cuda toolkit for 12.4, for example
conda install nvidia/label/cuda-12.4.0::cuda-toolkit
```

### install GroundingDINO for detection
```bash
cd GroundingDINO
pip install -e .
mkdir weights && cd weights

# download checkpoint
wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth

cd ../..
```

### install DepthAnything
```bash
cd Depth-Anything
pip install -r requirements.txt 
cd ..
```

### set up latest gradio

```bash
pip install gradio==4.39.0 gradio_client==1.1.1
```
If you encounter a pip version error that says `semantic-sam` requires `gradio==3.42.0`, you can ignore such warning and use the latest version of gradio (4.39.0). 

## Launching Gradio servers for each vision expert

For each server, please open a new terminal, so that you can view server logs.
From the logs, you can also copy the server address.
Make sure you launched all of them before running the vision agent.
One server can serve multiple agents.

For SOM:
```bash
cd simplified_som/
python som_server.py 
```

For GroundingDINO
```bash
cd GroundingDINO/
python grounding_dino_server.py 
```

For Depth-Anything
```bash
cd Depth-Anything/
python depthanything_server.py 
```

## Using the servers

After launching each server, put the server address in `agent/config.py`.
