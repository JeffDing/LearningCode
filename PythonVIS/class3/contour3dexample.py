import numpy
from mayavi import mlab

x,y,z = numpy.ogrid[-5:5:64j,-5:5:64j,-5:5:64j]
scalars = x*x+y*y+z*z
obj = mlab.contour3d(scalars,contours=8,transparent=True)
mlab.show()