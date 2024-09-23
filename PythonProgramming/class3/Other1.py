num = input("请输入一个三位整数：")
if len(num)==3:
	#sum=eval(num[0])+eval(num[1])+eval(num[2])
	sum=eval(num[0]+num[1]+num[2])
	print("您输入的整数位的和为：{}".format(sum))
else:
	print("输入错误")