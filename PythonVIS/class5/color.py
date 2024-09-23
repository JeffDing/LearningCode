from traits.api import HasTraits,Color
class Circle(HasTraits):
	color = Color

c = Circle()
c.color = 'red'
print(c.color.getRgb())
c.configure_traits()