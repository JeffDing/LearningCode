def f(n):
	n = str(n)
	sum = 0
	for i in n:
		sum += int(i)**2
	return sum

k,a,b = [int(i) for i in input("请输入三个数字，需要满足 a, b,k,k>=1, a,b<=10**10, a<=n :").split(",")]

count = 0

for i in range(a,b+1):
	if k*f(i) == i:
		count += 1
print (count)