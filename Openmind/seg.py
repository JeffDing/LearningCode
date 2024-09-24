from openmind import AutoTokenizer, AutoModel, is_torch_npu_available
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
        default="jeffding/all-MiniLM-L6-v1-openmind",
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
    tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to(device)
    
    start_time = time.time()
    sentences = ['如何更换花呗绑定银行卡', 'How to replace the Huabei bundled bank card']
    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt').to(device)

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    # Perform pooling. In this case, mean pooling.
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    print("Sentence embeddings:")
    print(sentence_embeddings)
    
    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")
    
if __name__ == "__main__":
    main()