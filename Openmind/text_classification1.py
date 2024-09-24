from openmind import AutoTokenizer, AutoModelForSequenceClassification, is_torch_npu_available
import torch

import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        help="Path to model",
        default="models/distilroberta-finetuned-financial-news-sentiment-analysis",
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
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, trust_remote_code=True).to(device)
                                              
    start_time = time.time()

    # 文本数据
    text = "Hello, my dog is cute."

    # 将文本编码为模型所需的格式
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)

    # 确保模型处于评估模式
    model.eval()

    # 使用torch.no_grad()进行推理，以避免计算梯度
    with torch.no_grad():
        # 进行推理
        outputs = model(**inputs)

    # 获取logits
    logits = outputs.logits

    # 将logits转换为预测类别的ID
    predicted_class_id = logits.argmax(-1).item()

    # 如果你有类别标签与ID的映射，你可以将预测的ID转换为实际的类别标签
    # 例如：
    # class_labels = ['negative', 'positive']
    # predicted_label = class_labels[predicted_class_id]
    # print(f"Predicted label: {predicted_label}")

    print(f"Predicted class ID: {predicted_class_id}")
    
    id2label = model.config.id2label[predicted_class_id]
    print(f"id2label:{id2label}")
                                        
    end_time = time.time()
    print(f"硬件环境：{device},推理执行时间：{end_time - start_time}秒")

if __name__ == "__main__":
    main()