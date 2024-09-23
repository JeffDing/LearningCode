from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
data_corpus = ['guru99 is the best size for online tutorials. I love to visit guru99 .']
vocabulary = vectorizer.fit(data_corpus)
X = vectorizer.transform(data_corpus)
print(X.toarray())
print(vocabulary.get_feature_names())
