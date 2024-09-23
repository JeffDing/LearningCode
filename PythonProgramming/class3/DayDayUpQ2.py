#DayDayUpQ2
dayfactor1 = 0.005
dayup1 = pow(1+dayfactor1,365)
daydown1 = pow(1-dayfactor1,365)
print("千分之5的向上：{:.2f},向下：{:.2f}".format(dayup1,daydown1))

dayfactor2 = 0.01
dayup2 = pow(1+dayfactor2,365)
daydown2 = pow(1-dayfactor2,365)
print("百分之1的向上：{:.2f},向下：{:.2f}".format(dayup2,daydown2))