from traits.api import Delegate,HasTraits,Instance,Int,Str

class Parent(HasTraits):
	#初始化
	last_name = str('Zhang')

class Child(HasTraits):
	age = Int
	#验证
	father = Instance(Parent)
	#代理
	last_name = Delegate('father')
	#监听
	def _age_changed(self,old,new):
		print('Age change from %s to %s' % (old,new))

p = Parent()
c = Child()
c.father = p
print(c.last_name)
c.age = 4
c.print_traits()
c.get()
c.set(age=8)