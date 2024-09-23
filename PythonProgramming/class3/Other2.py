N = eval(input("请输入一个N："))
daydayup = pow((1.0+N/1000),365)
daydaydn = pow((1.0-N/1000),365)
print("每天努力的能力：{:.2f}，每天放任的能力：{:.2f},能力间的比值：{}".format(daydayup,daydaydn,str(int(daydayup//daydaydn)))) 