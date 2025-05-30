import json

input_path = "/root/dataset/arxiv_random.jsonl"#刚刚随机抽样的数据
output_path = "/root/dataset/arxiv_dataset.jsonl"

count = 0
skipped = 0

with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
    for line in infile:
        try:
            record = json.loads(line)

            paper_id = record.get("id")
            title = record.get("title", "").replace("\n", " ").strip()
            submitter = record.get("submitter")
            authors = record.get("authors", "").replace("\n", " ").strip()
            categories = record.get("categories", "").split()
            abstract = record.get("abstract", "").strip()

            # 必要字段缺失，跳过
            if not all([paper_id, title, submitter, authors, categories, abstract]):
                skipped += 1
                continue

            category = categories[-1]
            journal = record.get("journal-ref", "No journal information available.")
            doi = record.get("doi", "No DOI information available.")
            license_url = record.get("license", "No license information available.")

            versions = record.get("versions", [])
            if not versions or "created" not in versions[-1]:
                skipped += 1
                continue
            version_str = versions[-1].get("version", "unknown")
            update_date = versions[-1]["created"]

            content = f"""This is a paper with ID {paper_id}, titled "{title}", submitted by {submitter}. The authors are {authors}.
The paper belongs to the {category} category and is published in {journal}. The latest version is {version_str}, created on {update_date}. DOI: {doi}. License: {license_url}.

Abstract:
{abstract}
"""

            result = {
                "messages": [
                    {
                        "role": "assistant",
                        "content": content
                    }
                ]
            }

            outfile.write(json.dumps(result) + "\n")
            count += 1

        except json.JSONDecodeError:
            skipped += 1
            continue

print(f"转换完成，共保存 {count} 条数据到 {output_path}，跳过 {skipped} 条不完整数据")
