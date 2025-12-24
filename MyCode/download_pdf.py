import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_pdf(url, folder_path):
    """下载 PDF 文件并保存到指定文件夹"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # 从 URL 中提取文件名
        filename = os.path.basename(urlparse(url).path)
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
            
        file_path = os.path.join(folder_path, filename)
        
        # 保存文件
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        print(f"已下载: {filename}")
        return True
    except Exception as e:
        print(f"下载失败 {url}: {e}")
        return False

def get_all_pdfs(url, folder_path='pdf_files'):
    """获取网页中所有的 PDF 文件链接并下载"""
    try:
        # 创建保存 PDF 的文件夹
        os.makedirs(folder_path, exist_ok=True)
        
        # 获取网页内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有链接
        pdf_links = []
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if href.lower().endswith('.pdf'):
                absolute_url = urljoin(url, href)
                pdf_links.append(absolute_url)
        
        # 去重
        pdf_links = list(set(pdf_links))
        
        print(f"找到 {len(pdf_links)} 个 PDF 文件:")
        for pdf_url in pdf_links:
            print(pdf_url)
        
        # 下载所有 PDF
        for pdf_url in pdf_links:
            download_pdf(pdf_url, folder_path)
            
        print("所有 PDF 文件下载完成！")
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    # 使用示例
    target_url = input("请输入要爬取的网页URL: ").strip()
    folder_path = input("请输入文件夹名字:").strip()
    get_all_pdfs(target_url,folder_path)
