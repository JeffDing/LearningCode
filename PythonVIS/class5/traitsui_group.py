from traits.api import HasTraits, Str, Int
from traitsui.api import View, Item, Group
from traitsui.menu import ModalButtons
 
class ModelManager(HasTraits):
    model_name = Str
    category = Str
    model_file = Str
    model_number = Int
    vertices = Int
 
view1 = View(
    Group(
        Item('model_name', label=u"模型名称"),
        Item('model_file', label=u"文件名"),
        Item('category', label=u"模型类型"),
        label = u'模型信息',
        show_border = True),
    Group(
        Item('model_number',label=u"模型数量"),
        Item('vertices',label=u"顶点数量"),
        label = u'统计数据',
        show_border = True),
    kind = 'modal',
    buttons = ModalButtons
)
 
model = ModelManager()
model.configure_traits(view=view1)