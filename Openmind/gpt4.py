from openmind import AutoModelForCausalLM, AutoTokenizer, pipeline, is_torch_npu_available
from openmind_hub import snapshot_download
import torch

import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        help="Path to model",
        default="models/Phi-3-mini-128k-instruct",
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

    # 加载分词器和模型
    model = AutoModelForCausalLM.from_pretrained( 
        model_path,  
        device_map=device,  
        torch_dtype="auto",  
        trust_remote_code=True,  
    ) 

    tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True) 
                                              
    start_time = time.time()

    torch.random.manual_seed(0) 
    

    messages = [ 
        {"role": "system", "content": "You are a helpful AI assistant."}, 
        {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"}, 
        {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."}, 
        {"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"}, 
    ] 

    pipe = pipeline( 
        "text-generation", 
        model=model, 
        tokenizer=tokenizer,
    ) 

    generation_args = { 
        "max_new_tokens": 500, 
        "return_full_text": False, 
        "temperature": 0.0, 
        "do_sample": False, 
    } 

    output = pipe(messages, **generation_args) 
    print(output[0]['generated_text']) 
                                        
    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")

if __name__ == "__main__":
    main()
