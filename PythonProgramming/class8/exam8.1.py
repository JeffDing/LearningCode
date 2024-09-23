#获得用户的任何可能输入，将其中的英文字符进行打印输出，程序不出现错误。

ls=""
s=input()
for each in s:
    if(each>='a'and each<='z') or (each>='A' and each<='Z'):
        ls+=each
print(ls)