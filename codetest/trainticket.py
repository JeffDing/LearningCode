a = input()

if(1<= eval(a[0:-1]) <= 17):
	if(a[-1] in ['A','a'] or a[-1] in ['F','f']):
		print("窗口")
	elif(a[-1] in ['C','c'] or a[-1] in ['D','d']):
		print("过道")
	elif(a[-1] in ['E','e']):
		print("中间")
	else:
		print("输入错误")
else:
	print("ERROR")