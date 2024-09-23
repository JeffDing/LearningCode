import matplotlib.pyplot as plt 
import numpy as np 

a = np.arange(10)
plt.plot(a,a*1.5,'go-',a,a*2.5,'rx',a,a*3.5,'*',a,a*4.5,'b-.',)
plt.show()