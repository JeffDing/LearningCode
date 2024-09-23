#获得用户输入的一个整数N，输出N中所出现不同数字的和。
n = input("请输入一个整数N：")
ss = set(n)
s = 0
for i in ss:
    s += eval(i)
print(s)