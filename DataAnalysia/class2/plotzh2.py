import matplotlib.pyplot as plt 
import matplotlib as mpl
import numpy as np 

mpl.rcParams['font.family']='Microsoft YaHei'
mpl.rcParams['font.size']='20'

a = np.arange(0.0,5.0,0.02)

plt.xlabel("横轴：时间")
plt.ylabel("纵轴：振幅")
plt.plot(a,np.cos(2*np.pi*a),'r--')
plt.show()