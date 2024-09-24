from openmind import pipeline, is_torch_npu_available
from openmind import AutoTokenizer, AutoModelForCausalLM
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
        default="models/Cerebras-GPT-590M",
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
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).to(device)
    
    start_time = time.time()
    text = "Generative AI is "
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer,device=device)
    generated_text = pipe(text, max_length=50, do_sample=False, no_repeat_ngram_size=2)[0]
    print(generated_text['generated_text'])
    
    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")
    
if __name__ == "__main__":
    main()