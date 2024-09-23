import pandas as pd
import matplotlib.pyplot as plt 

hprice = pd.Series([3.04,22.93,12.75,22.6,12.33], index=['2008','2009','2010','2011','2012'])
m2 = pd.Series([8.18,18.38,9.13,7.82,6.69], index=['2008','2009','2010','2011','2012'])
print(hprice.corr(m2))


plt.plot(hprice,color='red')
plt.plot(m2,color='blue')
plt.show()
