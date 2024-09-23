count=0
def hanoi(n,src,dst,mid):
    global count
    if n == 1:
        print("{}号圆盘:{}->{}".format(1,src,dst))
        count += 1
    else:
        hanoi(n-1,src,mid,dst)
        print("{}号圆盘:{}->{}".format(n,src,dst))
        count+=1
        hanoi(n-1,mid,dst,src)
h = eval(input("请输入圆盘数量："))
hanoi(h,"A","C","B")
print("一共搬运了{}次".format(count))