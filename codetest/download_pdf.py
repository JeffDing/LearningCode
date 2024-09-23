import requests
import os

from bs4 import BeautifulSoup

from urllib.parse import urljoin

url = "https://www.fia.com/documents/championships/fia-formula-one-world-championship-14/season/season-2023-2042"  # 目标网站的URL
save_path = "pdf_files_2023"  # 下载PDF文件的保存路径

response = requests.get(url)  # 获取网页内容
soup = BeautifulSoup(response.text, "html.parser")  # 解析HTML

# 查找包含PDF文件链接的元素
pdf_links = soup.find_all("a", href=lambda href: href and href.endswith(".pdf"))

# 如果保存路径不存在，则创建它
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 下载并保存PDF文件
for link in pdf_links:
    pdf_url_source = link.get("href")
    pdf_name =  pdf_url_source.split("/")[-1]
    pdf_path = os.path.join(save_path, pdf_name)
    website_root = "https://www.fia.com/"
    pdf_url = urljoin(website_root,pdf_url_source)

    if not os.path.exists(pdf_path):  # 如果文件不存在
        response = requests.get(pdf_url)
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"已下载文件: {pdf_name}")
    else:
        print(f"文件已存在: {pdf_name}")
