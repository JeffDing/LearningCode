import matplotlib.pyplot as plt 
import matplotlib as mpl

mpl.rcParams['font.family']='Microsoft YaHei'
mpl.rcParams['font.size']='12'
plt.plot([3,1,4,5,2])
plt.ylabel("纵轴（值）")
plt.savefig('test2',dpi=600)
plt.show()