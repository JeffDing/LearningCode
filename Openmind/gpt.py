from openmind import AutoTokenizer, AutoModelForCausalLM, is_torch_npu_available
from openmind_hub import snapshot_download
import torch.nn.functional as F
from torch import Tensor
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        help="Path to model",
        default="jeffding/TinyLLama-v0-openmind",
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
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
    model = model.to(device)
    start_time = time.time()
    
    prompt = "Give me a short introduction to large language model."
    inputs = tokenizer(prompt, return_tensors="pt", return_token_type_ids=False).to(device)
    out = model.generate(**inputs, max_new_tokens=80).ravel()
    out = tokenizer.decode(out)
    print(out)
    
    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")
    
if __name__ == "__main__":
    main()