import matplotlib.pyplot as plt 
import matplotlib as mpl
import numpy as np 

a = np.arange(0.0,5.0,0.02)

plt.xlabel("横轴：时间",fontproperties="Microsoft Yahei",fontsize=20)
plt.ylabel("纵轴：振幅",fontproperties="Microsoft Yahei",fontsize=20)
plt.plot(a,np.cos(2*np.pi*a),'r--')
plt.show()