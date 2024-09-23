from tvtk.api import tvtk
from tvtk.tools import ivtk
from pyface.api import GUI

s = tvtk.CubeSource(x_length = 1.0,y_length = 2.0,z_length = 3.0)
m = tvtk.PolyDataMapper(input_connection = s.output_port)
a = tvtk.Actor(mapper = m)

#创建一个带Crust (Python Shell)的窗口
gui = GUI()
win = ivtk.IVTKWithCrustAndBrowser()
win.open()
win.scene.add_actor(a)

#开始界面消息循环
gui.start_event_loop()