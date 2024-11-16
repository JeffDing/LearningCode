from openmind import pipeline, AutoTokenizer, is_torch_npu_available
from openmind_hub import snapshot_download
import torch.nn.functional as F
from torch import Tensor
import openmind
import torch
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        help="Path to model",
        default="models/ruBert-base",
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    model_path = args.model_name_or_path

    if is_torch_npu_available():
        device = "npu:0"
    else:
        device = "cpu"
    
    start_time = time.time()
    
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    pipe = pipeline('fill-mask', model=model_path, torch_dtype=torch.bfloat16, device_map=device)
    MASK_TOKEN = tokenizer.mask_token
    result = pipe("Hello I'm a {} model.".format(MASK_TOKEN))
    print(result)
    
    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")
    
if __name__ == "__main__":
    main()