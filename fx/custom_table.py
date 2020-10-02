from django.utils.safestring import mark_safe
from .base import Field_column

class TableOptions(object):
    def __init__(self, options=None):
        print(">>> option table > options:",options)
       # print("dir options:",dir(options.__dict__))
        self.model = getattr(options, 'model', None)
        
        
        # id attribute of <table> tag
        
class my_metaClass(type):
    
    def __new__(meta, classname, bases, attrs):
        #print ('Name            Type                 Value')
        #print ('-------------   ------------------   ---------------------------')
        options = TableOptions(attrs.get('Meta', None))
        attrs['options'] = options
        #print(f"dir(options): {dir(attrs['options'])}")
         
        columns = []
        
        for attr_name, attr in attrs.items():
            print(f"attr_name:{attr_name}, attr: {attr}")
            if isinstance(attr, ()): #todo remove SequenceColumn
                columns.extend(attr)
            elif isinstance(attr, Field_column  ):
                columns.append(attr)
         
       # attrs['column']=column
        return type.__new__(meta, classname, bases, attrs)
    
class Class_Table(metaclass = my_metaClass):
    def __init__( self, queryset=None,user_prefered_nos_rows = 10):
        super().__init__()
        self.queryset =queryset
        


     

 