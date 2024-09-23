from random import*
seed(123)
Points = eval(input()) 
hits = 0.0 
for i in range(1,Points+1):
    x,y = random(),random()
    dist = pow(x**2+y**2,0.5) 
    if dist<=1.0:
        hits+=1
pi = 4*(hits/Points)
print("{:.6f}".format(pi))