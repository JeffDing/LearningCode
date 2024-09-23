s = eval(input("请输入工资："))
if s < 5000:
	print("免税")
else:
	salary = s - 5000
	if (salary <= 3000):
		fee,num = 3,0
	elif(3000< salary <= 12000):
		fee,num = 10,210
	elif(12000< salary <= 25000):
		fee,num = 20,1410
	elif(25000< salary <= 35000):
		fee,num = 25,2260
	elif(35000< salary <= 55000):
		fee,num = 30,4410
	elif(55000< salary <= 80000):
		fee,num = 35,7160
	else:
		fee,num = 45,15160
	tax = salary * fee / 100 - num
	print("应缴税款{:.2f},实发工资{:.2f}元".format(tax,salary + 5000 - tax))