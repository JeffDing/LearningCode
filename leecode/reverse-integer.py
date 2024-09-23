'''
7. 整数反转
给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
示例：
输入: 123
输出: 321
def reverse(x: int) -> int:
    a = str(x)
    y = list(a)
    y.reverse()
    if y[-1] == "-":
        y.remove('-')
        y.insert(0, '-')
    if y[0] == 0:
        y.remove('0')
    y2 = ''.join(y)
    z = int(str(y2))
    if z < (-2**31) or z > (2**31-1):
        z = 0
    return z
print(reverse(eval(input("请输入一个32位有符号整数："))))