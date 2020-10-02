
from .models import MemberModel,WalletModel,TransferModel
from .models import TransferModel
from .baseTable import  base
from .mytable import Class_Table


class myTable(Class_Table):
    def __init__(self, **kwargs ):
        self.data =kwargs.get("data")
        self.filter_field_value = kwargs.get("filter_field_value", self.Options.filter_field_value)
        self.total_rows = kwargs.get("total_rows", self.Options.total_rows)
        self.user_prefered_nos_rows =  kwargs.get("user_prefered_nos_rows", self.Options.user_prefered_nos_rows)
        self.model =  kwargs.get("model", self.Options.model)
        self.filter_field =  kwargs.get("filter_field", self.Options.filter_field)
        self.code_name =  kwargs.get("code_name", self.Options.code_name)
        self.filter_dict=  kwargs.get("filter_dict", {})
        #.template_name = "products/member/templates/transfer_receivers_table.html"
    class Options:   
        model = 'Wallet'
        user_prefered_nos_rows =5
        total_rows =10
        rows_option_list =[3,5,10,20,30,50,100]
        filter_field_value = None
        filter_field = 'member_id'
        code_name=""
       
        
    def get_nav_settings(self):
        return {"total_records":self.total_rows,"rows_per_page": self.user_prefered_nos_rows,"rows_option_list":self.Options.rows_option_list,"filter_field_value":self.filter_field_value,"filter_field":self.filter_field}
    
    def get_model(self):
       return self.model

class TransferReceiver_cls(myTable):
    def __init__(self, **kwargs ):
        super().__init__(**kwargs)

    def setData(self,start,total_rows_to_display,distinct):
         self.user_prefered_nos_rows = total_rows_to_display
         if (distinct):
            self.data = TransferModel.objects.select_related('receiver').order_by('receiver_id').distinct('receiver_id').filter( **self.filter_dict )[start:total_rows_to_display]
            self.total_rows = TransferModel.objects.select_related('receiver').distinct('receiver_id').filter( **self.filter_dict ).count()
         else:
            self.data = TransferModel.objects.select_related('receiver').order_by('-id').filter( **self.filter_dict )[start:total_rows_to_display]
            self.total_rows = TransferModel.objects.select_related('receiver').order_by('id').filter( **self.filter_dict ).count()
class SearchMember(myTable):   # being used by search_settings at context_processor.py
    def __init__(self, **kwargs ):
        super().__init__(**kwargs)

     

         



 