'''
20. 有效的括号
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。
'''

def isValid(s: str) -> bool:
    if len(s)<2 or len(s)%2!=0:
        if s=='':
            return True
        else:
            return False
    count = 0
    length = len(s)
    while(count<length/2):
        s = s.replace("{}","").replace("[]","").replace("()","")
        count+=1
    if len(s)>0:
        return False
    else:
        return True
print(isValid(s="()"))