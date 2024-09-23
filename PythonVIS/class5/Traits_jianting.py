from traits.api import HasTraits, Str, Int
 
class Child ( HasTraits ):          
    name = Str
    age = Int
    doing = Str
     
    def __str__(self):
        return "%s<%x>" % (self.name, id(self))
    # 静态监听age属性的变化
    def _age_changed ( self, old, new ):
        print ("%s.age changed: form %s to %s" % (self, old, new))
    # 静态监听任何Trait属性的变化
    def _anytrait_changed(self, name, old, new):
        print ("anytrait changed: %s.%s from %s to %s" % (self, name, old, new))
 
def log_trait_changed(obj, name, old, new):
    print ("log: %s.%s changed from %s to %s" % (obj, name, old, new))
 
z = Child(name = "ZhangSan", age=4)
l = Child(name = "LiSi", age=1)
# 动态监听doing属性的变化
z.on_trait_change(log_trait_changed, name="doing")

z.age =5
z.doing = "playing"

l.doing = "sleeping"