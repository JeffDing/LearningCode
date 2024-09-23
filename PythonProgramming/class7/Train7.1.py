#打印输出附件文件的有效行数，注意：空行不计算为有效行数。
f = open("latex.log")
count = 0
for line in f:
        line = line.strip('\n')
        if len(line) > 0:
            count += 1
        else:
            count += 0
print("共{}行".format(count))