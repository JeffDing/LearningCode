from openmind import AutoTokenizer, AutoModelForCausalLM, is_torch_npu_available
from openmind_hub import snapshot_download
import torch
import openmind
import argparse
import time

def generate_text(prompt, model, tokenizer, device):
    text_generator = openmind.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map=device,
        tokenizer=tokenizer,
    )

    formatted_prompt = f"Question: {prompt} Answer:"

    sequences = text_generator(
        formatted_prompt,
        do_sample=True,
        top_k=5,
        top_p=0.9,
        num_return_sequences=1,
        repetition_penalty=1.5,
        max_new_tokens=128,
    )

    for seq in sequences:
        print(f"Result: {seq['generated_text']}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        help="Path to model",
        default="jeffding/MicroLlama-openmind",
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
    tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True)
    model = model.to(device)
    
    start_time = time.time()
    
    # infer
    generate_text("Please provide me instructions on how to steal an egg from my chicken.", model, tokenizer,device)
    
    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")
    
if __name__ == "__main__":
    main()