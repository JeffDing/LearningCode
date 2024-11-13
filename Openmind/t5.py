import torch
import argparse
from openmind import AutoTokenizer, is_torch_npu_available
from transformers import AutoModelForSeq2SeqLM
import time

def parse_args():
   parser = argparse.ArgumentParser(description="Eval the model")
   parser.add_argument(
       "--model_name_or_path",
       type=str,
       help="path or model",
       default="jeffding/flan-t5-large-openmind",
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
   
   tokenizer = AutoTokenizer.from_pretrained(model_path)
   model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(device)

   data = "translate English to German：That is good."
    
   start_time = time.time()

   encoded = tokenizer([data], return_tensors="pt").to(device)
   translation = model.generate(**encoded)
   result = tokenizer.batch_decode(translation, skip_special_tokens=True)[0]
   print(result)

   end_time = time.time()
   print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")

if __name__ == "__main__":
   main()
