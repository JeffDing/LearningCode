from traits.api import HasTraits, Button, Int
from traitsui.api import View
 
class ButtonEditor(HasTraits):
    # 定义一个Button trait:
    my_button = Button('Click Me')
    counter = Int
    # 当按钮点击后，处理当按钮被点击后，触发的事件
    def _my_button_fired(self):
        self.counter += 1
    # 创建视图
    traits_view = View(
        'my_button',
        'counter',
        title     = 'ButtonEditor',
        buttons   = [ 'OK' ],
        resizable = True)
 
button = ButtonEditor()
button.configure_traits()