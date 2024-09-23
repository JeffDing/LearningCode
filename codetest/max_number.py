N=eval(input("请输入数字个数:"))
nums=[]
if N>0:
    for i in range(N):
    	a = eval(input("请输入第{}个数字:".format(i+1)))
    	nums.append(a)
    print("max={}".format(max(nums)))
if N<=0:
    print("ERROR")