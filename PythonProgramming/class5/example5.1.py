def rvs(s):
    if s=="":
        return s
    else:
        return rvs(s[1:])+s[0]
str = input("请输入一个字符串：")
print("反转后的结果为：{}".format(rvs(str)))
