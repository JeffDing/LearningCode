import numpy as np 
from mayavi import mlab

#建立数据
n_mer,n_long = 6,11
dphi = np.pi / 1000.0
phi = np.arange(0.0,2*np.pi+0.5*dphi,dphi)
mu =  phi * n_mer
x = np.cos(mu) *  (1+np.cos(n_long*mu/n_mer)*0.5)
y = np.sin(mu) *  (1+np.cos(n_long*mu/n_mer)*0.5)
z = np.sin(n_long*mu/n_mer)*0.5

#对数据进行可视化
l = mlab.plot3d(x,y,z,np.sin(mu),tube_radius=0.025,colormap='Spectral')
mlab.show()