import numpy
from mayavi import mlab

#建立数据
s = numpy.random.random((10,10))
print(s)

#对数据进行可视化
img = mlab.imshow(s,colormap='gist_earth')
mlab.show()