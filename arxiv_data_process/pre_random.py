import json
import random

input_path = "----------"
output_path = "----------"
sample_size = 20000  # 你可以改成 10000 等其他数字

# 先将所有数据加载到内存中（30万条可以接受）
with open(input_path, 'r') as infile:
    data = [json.loads(line) for line in infile]

print(f"原始数据量：{len(data)} 条")
random.seed(42) #随机数种子，可以自己随便调
# 随机抽样
sampled_data = random.sample(data, sample_size)

# 保存结果
with open(output_path, 'w') as outfile:
    for record in sampled_data:
        outfile.write(json.dumps(record) + '\n')

print(f"已随机抽取 {sample_size} 条数据保存到 {output_path}")
