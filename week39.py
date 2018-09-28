class ImmutableParent():

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def __setattr__(self, name, val):
        response = f'Attribute {name} can not be '
        if name in self.__dict__:
            response += 'changed'
        else:
            response += 'added'
        raise AttributeError(response)
        
    def __delattr__(self, name):
        raise AttributeError(f'Attribute {name} can not be deleted')
        
    def __repr__(self):
        return f'{vars(self)}'
        
        
class ImmutableMe(ImmutableParent):
    pass
    
    
