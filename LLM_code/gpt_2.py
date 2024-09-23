import torch
from openmind import AutoTokenizer, AutoModelForCausalLM, is_torch_npu_available
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        help="Path to model",
        default="jeffding/internlm2_5-7b-openmind",
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
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    # Set `torch_dtype=torch.float16` to load model in float16, otherwise it will be loaded as float32 and might cause OOM Error.
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, trust_remote_code=True).to(device)
    model = model.eval()
    inputs = tokenizer(["简单介绍一下上海这座城市"], return_tensors="pt")
    for k,v in inputs.items():
        inputs[k] = v.to(device)
    gen_kwargs = {"max_length": 1000, "top_p": 0.8, "temperature": 0.8, "do_sample": True, "repetition_penalty": 1.0}
    output = model.generate(**inputs, **gen_kwargs)
    output = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
    print(output)
    end_time = time.time()
    print(f"硬件环境：{device}推理执行时间：{end_time - start_time}秒")

if __name__ == "__main__":
    main()
