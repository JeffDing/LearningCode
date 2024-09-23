#GovRptWordCloudV1.py
import jieba
import wordcloud
#from scipy.misc import imread
#from imageio import imread
from matplotlib.pyplot import imread

mask = imread("chinamap.jpg")
f = open("新时代中国特色社会主义.txt","r",encoding="utf-8")
t = f.read()
f.close()
ls = jieba.lcut(t)
txt = " ".join(ls)
w = wordcloud.WordCloud(width = 1000,height = 700, background_color = "white",mask = mask)
w.generate(txt)
w.to_file("GovRptV3.png")