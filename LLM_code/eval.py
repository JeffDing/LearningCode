import torch.nn.functional as F
from torch import Tensor
from openmind import AutoTokenizer, AutoModel
import torch
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        help="Path to model",
        default="models/all_datasets_v3_mpnet-base",
    )
    args = parser.parse_args()
    return args

def evaluate_on_device(model_path, input_texts, device):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to(device)
    # Tokenize the input texts
    batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt').to(device)
    outputs = model(**batch_dict)
    embeddings =outputs.last_hidden_state[:,0]
    #(Optionally)normalizeembeddings
    embeddings =F.normalize(embeddings, p=2, dim=1)
    return embeddings

args = parse_args()
model_path = args.model_name_or_path
  
input_texts =[
"what is the capital of china?"
"how to implement quick sort in python?"
]
#Evaluate on CPU
cpu_embeddings =evaluate_on_device(model_path,input_texts,"cpu")

# print(f"CPU Embeddings:fcpu embeddings}")
# Evaluate on NPu if available
if torch.npu.is_available():
    npu_embeddings=evaluate_on_device(model_path, input_texts,"npu:0")
    
    # print(f"NPU Embeddings:fnpu embeddings}")
    #Move CPu embeddings to NPU
    cpu_embeddings_on_npu=cpu_embeddings.to("npu:0")

    # Calculate the cosine similarity between CPu and NPu embeddings
    
    cosine_similarity =F.cosine_similarity(cpu_embeddings_on_npu, npu_embeddings, dim=1)
    print(f"cosine similarity between CPU and NPU embeddings: {cosine_similarity}")
else:
    print("NPU is not available.")
