import math

m=eval(input("请输入数字:"))
nums=[]
for i in range(2,m):
	for j in range(2,int(math.sqrt(i)+1)):		
		if i%j ==0:
			break
	else:
		nums.append(i)
print(nums)