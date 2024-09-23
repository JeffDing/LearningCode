from traits.api import HasTraits, Int, Range, Property, property_depends_on
from traitsui.api import View, Item, RangeEditor
 
class RangeDemo(HasTraits):
    a = Range(1, 10)
    b = Range(1, 10)
    c = Property(Int)
    view = View(
        Item('a'),
        Item('b'),
        '_',
        Item('c',editor=RangeEditor(low = 1, high = 20, mode = 'slider')),
        Item('c'),
        width = 0.3
    )
 
    @property_depends_on('a,b', settable = True)
    def _get_c(self):
        print("computing")
        return (self.a + self.b)
 
ran = RangeDemo()
ran.edit_traits()