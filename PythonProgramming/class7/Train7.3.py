#统计附件文件中与其他任何其他行都不同的行的数量，即独特行的数量。
f = open("latex.log")
ls = f.readlines()
s = set(ls)
for i in s:
    ls.remove(i)
t = set(ls)
print("共{}独特行".format(len(s)-len(t)))