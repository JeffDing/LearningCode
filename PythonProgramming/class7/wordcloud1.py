import wordcloud
c = wordcloud.WordCloud()
c.generate("WordCloud by Python")
c.to_file("pywordcloud.png")