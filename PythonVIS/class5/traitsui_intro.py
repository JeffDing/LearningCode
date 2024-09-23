from traits.api import HasTraits, Str, Int
 
class ModelManager(HasTraits):
    model_name = Str
    category = Str
    model_file = Str
    model_number = Int
 
model = ModelManager()
model.configure_traits()