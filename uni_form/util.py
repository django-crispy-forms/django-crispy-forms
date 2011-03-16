class BaseInput(object):
    """
    A base Input class to reduce the amount of code in the Input classes.
    """
    
    def __init__(self,name,value):
        self.name = name
        self.value = value
        
