import numpy as np 
import matplotlib.pyplot as plt 

np.random.seed(0)
mu,sigma = 100,20 #均质和标准差
a = np.random.normal(mu,sigma,size=100)

plt.hist(a,40,density=1,histtype='stepfilled',facecolor='b',alpha=0.74)
plt.title('Histogram')

plt.show()