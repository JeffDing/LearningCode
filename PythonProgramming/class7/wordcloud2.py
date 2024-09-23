import wordcloud
txt = "Life is short,You need Python"
w = wordcloud.WordCloud(background_color= "white")
w.generate(txt)
w.to_file("pywcloud.png")