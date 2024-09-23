'''
190.颠倒二进制位
颠倒给定的 32 位无符号整数的二进制位。
示例：
输入: 00000010100101000001111010011100
输出: 00111001011110000010100101000000
'''
def reverseBits(n: int) -> int:
    temp = bin(n)[2:]
    count = 32-len(temp)
    if count > 0:
        for i in range(0,count):
            temp = '0' + temp
    return int(temp[::-1],2)
print(reverseBits(n=eval(input("请输入32位无符号整数的二进制:"))))