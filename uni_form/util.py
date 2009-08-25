class BaseInput(object):
    """
        An base Input class to reduce the amount of code in the Input classes.
    """
    
    def __init__(self,name,value):
        self.name = name
        self.value = value
        

class Toggle(object):
    """
        A container for holder toggled items such as fields and buttons.
    """
    
    fields = []
    
    