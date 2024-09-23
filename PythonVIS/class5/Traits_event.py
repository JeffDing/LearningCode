from traits.api import HasTraits, Str, Int, Event, on_trait_change
 
class Child (HasTraits):          
    name = Str("ZhangSan")
    age = Int(4)
    Infoupdated = Event
    # 对_Info_changed()方法进行修饰
    @on_trait_change("name,age")
    def _Info_changed (self):
        self.Infoupdated = True
    # Inforupdated事件处理方法
    def _Infoupdated_fired(self):
        self.reprint()
    def reprint(self):
        print ("reprint information %s , %s" % (self.name, self.age))

child = Child()
child.name="LiSi"
child.age = 1
child.name="liSi"
child.Infoupdated=0