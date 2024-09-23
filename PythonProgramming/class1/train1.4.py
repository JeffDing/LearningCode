#TempConvert.py
TempStr = input("请输入带有符号的温度值：")
if TempStr[0] in ['F','f']:
    C = (eval(TempStr[1:])-32)/1.8
    print("转换后的温度是C{:.2f}".format(C))
elif TempStr[0] in ['C','c']:
    F = 1.8*eval(TempStr[1:])+32
    print("转换后的温度是:F{:.2f}".format(F))
else:
    print("输入格式错误")
