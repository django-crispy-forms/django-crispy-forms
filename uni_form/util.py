class BaseInput(object):
    """
        An base Input class to reduce the amount of code in the Input classes.
    """

    def __init__(self,name,value):
        self.name = name
        self.value = value
        
    def __call__(self):

        return '%s=%s|%s' % (self.input_type, self.name, self.value)
        
class Toggle(object):
    """
        A container for holder toggled items such as fields and buttons.   
    """
    
    fields = []
    
    