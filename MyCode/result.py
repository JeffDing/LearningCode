N=eval(input("请输入学生个数:"))
#N = 10
nums=[]
for i in range(N):
	a = eval(input("请输入第{}个学生成绩:".format(i+1)))
	if a >=0 and a<=100:
		if a < 60:
			continue
		else:
			nums.append(a)
	else:
		print("输入有误，请重新输入")
		break
print("人数={},平均分={}".format(len(nums),sum(nums)/len(nums)))