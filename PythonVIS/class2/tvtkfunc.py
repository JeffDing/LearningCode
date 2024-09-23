def ivtk_scene(actors):
	from tvtk.tools import ivtk
	#创建一个带Crust (Python Shell)的窗口
	win = ivtk.IVTKWithCrustAndBrowser()
	win.open()
	win.scene.add_actor(actors)

	#修正错误
	dialog = win.control.centralWidget().widget(0).widget(0)
	from pyface.qt import QtCore
	dialog.setWindowFlags(QtCore.Qt.WindowFlags(0x00000000))
	dialog.show()
	return win
	
def event_loop():	
	#开始界面消息循环
	from pyface.api import GUI
	gui = GUI()
	gui.start_event_loop()
