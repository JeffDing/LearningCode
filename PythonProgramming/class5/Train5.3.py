#计算任意个输入数字的乘积
def cmul(*a):
    sig = 1
    for i in a:
        sig = sig*i
    return sig
print(eval("cmul({})".format(input("输入任意个数字："))))