import torch
import argparse
from openmind import pipeline, is_torch_npu_available
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Eval the model")
    parser.add_argument(
       "--model_name_or_path",
       type=str,
       help="path or model",
       default="jeffding/multilingual-MiniLMv2-L6-mnli-xnli-openmind",
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

    classifier = pipeline("zero-shot-classification", model=model_path,device_map=device)

    sequence_to_classify = "Angela Merkel ist eine Politikerin in Deutschland und Vorsitzende der CDU"
    candidate_labels = ["politics", "economy", "entertainment", "environment"]
    output = classifier(sequence_to_classify, candidate_labels, multi_label=False)
    print(output)

    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")

if __name__ == "__main__":
   main()