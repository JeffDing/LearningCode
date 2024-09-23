"""
演示TraitsUI的各种编辑器
"""
 
import os
from datetime import time
from traits.api import *
from traitsui.api import *
 
class EditorDemoItem(HasTraits):
    """界面右半部分,对于选中的某个Trait属性,使用4种样式创建属性编辑器"""
    code = Code()
    view = View(
        Group(
            # 使用simple编辑器,可尽量减少界面占用空间,width属性可指定编辑器宽度,负数表示强制设置宽度
            Item("item", style="simple", label="simple", width=-300),
            "_",  # 下划线字符串表示创建分隔线
            # 使用custom编辑器,可尽量呈现更多内容 #
            # TODO: Trait,Enum,Range三个函数无法用于custom编辑器,要运行这三个函数需要将其注释
            Item("item", style="custom", label="custom"),
            "_",
            # 使用text编辑器,只呈现文本内容
            Item("item", style="text", label="text"),
            "_",
            # 使用readonly编辑器,呈现只读文本
            Item("item", style="readonly", label="readonly"),
        ),
    )
 
 
class EditorDemo(HasTraits):
    """创建主界面"""
    codes = List(Str)  # 创建List界面,用来展示各种Trait属性的字符串
    selected_item = Instance(EditorDemoItem)  # 初始化selected_item界面,用来存储被选项的编辑界面
    selected_code = Str  # 初始化selected_code变量,用来存储被选项名称
    view = View(
        # 使用HSplite水平分隔两个界面
        HSplit(
            # 界面左半部分,用来创建各种Trait属性的源程序列表
            Item("codes", style="custom", show_label=False,
                 # 将editor属性设置为ListStrEditor(列表选择框控件),并更新selected_code变量
                 editor=ListStrEditor(editable=False, selected="selected_code")),
            # 界面右半部分
            Item("selected_item", style="custom", show_label=False),
        ),
        resizable=True,
        width=800,
        height=400,
        title=u"各种编辑器演示"
    )
 
    def _selected_code_changed(self):
        """当selected_code变量改变时触发,更新selected_item界面"""
        item = EditorDemoItem(code=self.selected_code)
        # 使用eval对selected_code字符串进行求值,并将值存储到item中
        item.add_trait("item", eval(str(self.selected_code)))
        self.selected_item = item
 
 
class Employee(HasTraits):
    """创建Employee类,该类为包含四个属性的界面"""
    name = Unicode(label=u"姓名")
    department = Unicode(label=u"部门")
    salary = Int(label=u"薪水")
    bonus = Int(label=u"奖金")
    view = View("name", "department", "salary", "bonus")
 
 
if __name__ == '__main__':
    employee = Employee()
    demo_list = [u"低通", u"高通", u"带通", u"带阻"]
    trait_defines = """
        Array(dtype="int32", shape=(3,3)) #{1}fadsfa
        Bool(True)
        Button("Click me")
        List(editor=CheckListEditor(values=demo_list))
        Code("print('hello world')")
        Color("red")
        RGBColor("red")
        Trait(*demo_list) #无法用于custom编辑器
        Directory(os.getcwd())
        Enum(*demo_list) #无法用于custom编辑器
        File()
        Font()
        HTML('<b><font color="red" size="40">hello world</font></b>')
        List(Str, demo_list)
        Range(1, 10, 5) #无法用于custom编辑器
        List(editor=SetEditor(values=demo_list))
        List(demo_list, editor=ListStrEditor())
        Str("hello")
        Password("hello")
        Str("Hello", editor=TitleEditor())
        Tuple(Color("red"), Range(1,4), Str("hello"))
        Instance(EditorDemoItem, employee)    
        Instance(EditorDemoItem, employee, editor=ValueEditor())
        Instance(time, time(), editor=TimeEditor())
    """
    demo = EditorDemo()
    # 一般写法
    trait_list = []
    for s in trait_defines.split('\n'):  # 按行分割字符串
        if s.split('#')[0].strip():  # 判断s中是否存在可执行函数
            trait_list.append(s.split('#')[0])  # 去掉注释
    demo.codes = trait_list
    # 简洁写法
    # demo.codes = [s.split("#")[0] for s in trait_defines.split("\n") if s.split('#')[0].strip()]
    demo.configure_traits()