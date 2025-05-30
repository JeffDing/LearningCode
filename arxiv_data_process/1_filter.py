import json

# 要保留的类别关键词
target_categories = {
    "astro-ph", "cond-mat.mes-hall", "cond-mat.mtrl-sci",
    "cs.CL", "cs.CV", "cs.LG",
    "gr-qc", "hep-ph", "hep-th", "quant-ph"
}

input_path = "/root/dataset/arxiv-metadata-oai-snapshot.json"#原数据路径
output_path = "/root/dataset/arxiv.jsonl"  # 使用 JSON Lines 格式输出路径

count = 0

with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
    for line in infile:
        try:
            record = json.loads(line)
            record_cats = record.get("categories", "").split()
            if record_cats:
                last_cat = record_cats[-1]
                if last_cat in target_categories:
                    outfile.write(json.dumps(record) + '\n')
                    count += 1
        except json.JSONDecodeError:
            continue  # 忽略格式错误的行

print(f"筛选完成，共保存了 {count} 条记录到 {output_path}")