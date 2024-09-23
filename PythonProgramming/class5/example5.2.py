def f(n):
    if n==1 or n==2:
        return 1
    else:
        return (n-1)+(n-2)
a = eval(input("请输入数字："))
num = f(a)
print("结果为：{}".format(num))
