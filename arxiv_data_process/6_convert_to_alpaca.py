import json
import os
import argparse


def convert_to_alpaca_format(input_file, output_file):
    """
    将 Swift 格式的数据转换为 Alpaca 格式

    输入格式:
    {
        "system": "你是个优秀的论文分类师",
        "conversation": [
            {
                "human": "Based on the title...",
                "assistant": "D"
            }
        ]
    }

    输出格式 (Alpaca):
    {
        "instruction": "根据论文的标题、作者和摘要，确定该论文的科学类别。",
        "input": "Based on the title...",
        "output": "D"
    }
    """
    print(f"转换数据: {input_file} -> {output_file}")

    converted_data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line.strip())

                # 检查数据结构
                if "system" not in data or "conversation" not in data:
                    print(f"警告: 数据缺少必要字段: {data}")
                    continue

                # 从 system 提取指令
                instruction = data.get("system", "")
                if not instruction:
                    instruction = "根据论文的标题、作者和摘要，确定该论文的科学类别。"

                # 处理对话
                for turn in data["conversation"]:
                    if "human" in turn and "assistant" in turn:
                        # 创建新的 Alpaca 格式数据
                        new_data = {
                            "instruction": instruction,
                            "input": turn["human"],
                            "output": turn["assistant"],
                        }
                        converted_data.append(new_data)

            except json.JSONDecodeError:
                print(f"警告: 无法解析JSON行: {line}")
            except Exception as e:
                print(f"处理行时发生错误: {str(e)}")

    # 写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        for item in converted_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"转换完成! 共转换 {len(converted_data)} 条数据")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="转换数据到Alpaca格式")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="输入文件路径 (swift_formatted_sft_train_data.jsonl)",
    )
    parser.add_argument("--output", type=str, required=True, help="输出文件路径")

    args = parser.parse_args()
    convert_to_alpaca_format(args.input, args.output)
