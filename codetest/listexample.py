ls = []
n = input().split(",")
for i in n:
	ls.append(eval(i))
if 789 in ls:
	a = ls.index(789)
	print(a)
	ls.insert(a+1,"012")
	for m in ls:
		if m==789:
			ls.remove(789)
	print(ls)