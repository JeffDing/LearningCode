from jina import DocumentArray, Document  # 导包

# DocumentArray 相当于一个 list，用于存放 Document
da = DocumentArray([Document(text='hello world'), 
                    Document(text='goodbye world'),
                    Document(text='hello goodbye')])

vocab = da.get_vocabulary()  # 输出：{'hello': 2, 'world': 3, 'goodbye': 4}

print(vocab)

# 转为ndarray
for d in da:
    d.convert_text_to_tensor(vocab, max_length=10)  # 转为tensor向量，max_length为向量最大值，可不设置
    print(d.tensor)

# ndarray
for d in da:
    d.convert_tensor_to_text(vocab)
    print(d.text)

