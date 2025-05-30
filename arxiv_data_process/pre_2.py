import json

input_path = "----"          # 上一步筛选后的数据
output_path = "----"  # 输出高质量数据

count = 0

with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
    for line in infile:
        try:
            record = json.loads(line)

            # 获取更新日期和摘要
            update_date = record.get("update_date", "")
            abstract = record.get("abstract", "")

            # 过滤条件，这里根据自己的模型参数修改
            if len(abstract) >= 300 and len(abstract)<=4096:
                if update_date and int(update_date[:4]) >= 2020:
                    outfile.write(json.dumps(record) + '\n')
                    count += 1

        except json.JSONDecodeError:
            continue  # 跳过格式错误的行

print(f"高质量筛选完成，共保留 {count} 条记录到 {output_path}")