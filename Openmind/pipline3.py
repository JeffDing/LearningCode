from openmind import AutoModelForCausalLM, AutoTokenizer, pipeline , is_torch_npu_available
from openmind_hub import snapshot_download
import torch.nn.functional as F
from torch import Tensor
import openmind
import torch
import argparse
import time

# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        help="Path to model",
        default="jeffding/AlephBERT-openmind",
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
        
    # Load model from HuggingFace Hub
    model = AutoModelForCausalLM.from_pretrained(model_path,
                                             device_map=device,
                                             trust_remote_code=False,
                                             revision="main")

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
    
    start_time = time.time()
    prompt = "Tell me about AI"
    prompt_template=f'''<s>[INST] {prompt} [/INST]
    '''

    print("\n\n*** Generate:")

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
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
        repetition_penalty=1.1
    )

    print(pipe(prompt_template)[0]['generated_text'])
    
    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")
    
if __name__ == "__main__":
    main()