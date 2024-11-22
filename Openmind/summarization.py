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
       default="models/mt5_summarize_japanese",
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
        
    seq2seq = pipeline("summarization", model=model_path,device_map=device)
    
    start_time = time.time()
    sample_text = "サッカーのワールドカップカタール大会、世界ランキング24位でグループEに属する日本は、23日の1次リーグ初戦において、世界11位で過去4回の優勝を誇るドイツと対戦しました。試合は前半、ドイツの一方的なペースではじまりましたが、後半、日本の森保監督は攻撃的な選手を積極的に動員して流れを変えました。結局、日本は前半に1点を奪われましたが、途中出場の堂安律選手と浅野拓磨選手が後半にゴールを決め、2対1で逆転勝ちしました。ゲームの流れをつかんだ森保采配が功を奏しました。"
    result = seq2seq(sample_text)
    print(result)

    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")

if __name__ == "__main__":
   main()