from tvtkfunc import ivtk_scene,event_loop
from tvtk.api import tvtk

s = tvtk.CubeSource(x_length = 1.0,y_length = 2.0,z_length = 3.0)
m = tvtk.PolyDataMapper(input_connection = s.output_port)
a = tvtk.Actor(mapper = m)
win = ivtk_scene(a)
win.scene.isometric_view()
event_loop()