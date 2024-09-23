#工地搬砖问题：男的每人3块，女的每人2块，小孩2人一块，问有多少种办法
count = 0
for i in range(0,15):
	for j in range(0,23):
		k = 45-i-j
		x = int(k/2)
		y = 3*i+j*2+x
		if(y == 45):
			print("Man={},Woman={},Child={}".format(i,j,k))
			count=count+1
print("一共有{}个办法".format(count))