from openmind import AutoTokenizer, AutoModelForCausalLM, pipeline, is_torch_npu_available
from openmind_hub import snapshot_download
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
        default="models/mega-ar-525m-v0.07-ultraTBfw",
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
        
    
    model = AutoModelForCausalLM.from_pretrained(model_path,
                                             device_map=device,
                                             trust_remote_code=False,
                                             revision="main").to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True,trust_remote_code=False)
    
    start_time = time.time()
    
    prompt = "Write a story about llamas"
    system_message = "You are a story writing assistant"
    prompt_template=f'''[INST] {prompt} [/INST]
    '''

    print("\n\n*** Generate:")

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.to(device)
    output = model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=512)
    print(tokenizer.decode(output[0]))

    # Inference can also be done using transformers' pipeline

    print("*** Pipeline:")
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        top_k=40,
        repetition_penalty=1.1,
        device=device
    )

    print(pipe(prompt_template)[0]['generated_text'])
    
    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")
    
if __name__ == "__main__":
    main()
