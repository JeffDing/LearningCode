#DayDayUpQ3
dayup = 1.0
dayfactory = 0.01
for i in range(365):
    if i%7 in[6,0]:
        dayup = dayup*(1-dayfactory)
    else:
        dayup = dayup*(1+dayfactory)
print("工作日的力量：{:.2f}".format(dayup))