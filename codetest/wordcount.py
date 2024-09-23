import re

def wordcount(text):
    # 使用正则表达式去除标点符号
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    # 将所有字母转换为小写
    cleaned_text = cleaned_text.lower()
    # 分割字符串为单词列表
    words = cleaned_text.split()
    # 创建字典统计单词出现的次数
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

# 测试函数
text = """
Got this panda plush toy for my daughter's birthday,
who loves it and takes it everywhere. It's soft and
super cute, and its face has a friendly look. It's
a bit small for what I paid though. I think there
might be other options that are bigger for the
same price. It arrived a day earlier than expected,
so I got to play with it myself before I gave it
to her.
"""

print(wordcount(text))