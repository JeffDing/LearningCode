import json
import random

input_file = "---------"   # 20000条原始数据文件路径
output_file = "----------"

# 类别对应选项映射
label_map = {
    "astro-ph": "A",
    "cond-mat.mes-hall": "B",
    "cond-mat.mtrl-sci": "C",
    "cs.CL": "D",
    "cs.CV": "E",
    "cs.LG": "F",
    "gr-qc": "G",
    "hep-ph": "H",
    "hep-th": "I",
    "quant-ph": "J"
}

options_text = (
    "\n\nA. astro-ph\nB. cond-mat.mes-hall\nC. cond-mat.mtrl-sci\nD. cs.CL\n"
    "E. cs.CV\nF. cs.LG\nG. gr-qc\nH. hep-ph\nI. hep-th\nJ. quant-ph"
)

# 读取所有数据
with open(input_file, 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]

# 随机抽样1000条
random.seed(42)
sampled = random.sample(data, 1000)

with open(output_file, 'w', encoding='utf-8') as f_out:
    count = 0
    for item in sampled:
        # 多类别时取最后一个类别（通常以空格分割）
        categories_str = item.get("categories", "").strip()
        if not categories_str:
            continue
        last_category = categories_str.split()[-1]

        if last_category not in label_map:
            continue

        title = item.get("title", "").replace("\n", " ").strip()
        authors = item.get("authors", "").replace("\n", " ").strip()
        abstract = item.get("abstract", "").replace("\n", " ").strip()
        if not title or not authors or not abstract:
            continue

        human_text = (
            f"Based on the title '{title}', authors '{authors}', and abstract '{abstract}', "
            f"please determine the scientific category of this paper.{options_text}"
        )

        finetune_sample = {
            "system": "你是个优秀的论文分类师",
            "conversation": [
                {
                    "human": human_text,
                    "assistant": label_map[last_category]
                }
            ]
        }

        f_out.write(json.dumps(finetune_sample, ensure_ascii=False) + "\n")
        count += 1

print(f"转换完成，共生成{count}条微调数据，保存到 {output_file}")