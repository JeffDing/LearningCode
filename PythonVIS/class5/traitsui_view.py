from traits.api import HasTraits,Str,Int
from traitsui.api import View,Item

class ModelManager(HasTraits):
	model_name = Str
	category = Str
	model_file = Str
	model_number = Int
	view = View(
		Item('model_name',label=u"模型名称"),
		Item('model_file',label=u"文件名",tooltip=u"路径及文件名"),
		Item('category',label=u"模型类型"),
		Item('model_number',label=u"模型数量"),
		title = u"模型资料",width = 200,resizable = True
		)

model = ModelManager()
model.configure_traits()

