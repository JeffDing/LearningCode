x = eval(input("请输入X："))
y = eval(input("请输入Y："))
if (x == y):
	print("两数相同")
elif(x > y):
	print("较大数字为:{}".format(x))
else:
	print("较大数字为:{}".format(y))