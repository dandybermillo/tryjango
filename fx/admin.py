from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .models import PersonalLoanModel,WalletModel,MemberModel,VentureModel,VentureWalletModel
from .models import Tmp_UsernameModel,Tmp_PasswordModel,IdRepositoryModel
from .models import TransferModel,UserPreferenceModel,WalletModel,TradingModel
from .models import CcModel,VentureCcModel,SavingModel,PaymentModel,PendingLoanModel,NoteModel,Change_Table,ProfileModel
from .models import LoanSummaryModel,tmpVariables,dayTransactionModel,JoinModel,MessageModel,LoadModel,RepairModel,MechanicModel,ConstructionModel,DeliveryModel,LivePostModel
import decimal, csv
from django.db.models import Count
#.model is a realative import bcoz models and admin are in 
#  same dir
# Register your models here. 
#from django.contrib.admin.actions import delete_selected as delete_selected_
admin.site.site_header ="Fair Exchange Admin"

class MemberAdmin(admin.ModelAdmin):

    list_per_page=5
    list_display = ['id','member_id','member','address','telephone','active','birthday']
    list_display_links =['member']
    search_fields = ['firstname']
    def member(self,obj):

        return '{} {} {} {}'.format(obj.gender,obj.firstname,obj.middlename,obj.lastname)
class ProfileModelAdmin(admin.ModelAdmin):

    list_display = ['id','firstname','middlename','lastname','source_id','address','telephone','active','birthday']
   
    
class WalletAdmin(admin.ModelAdmin):
    list_display = ['id','date_entered','debit','credit','description','transaction_type','category','source_id'
]
    def Delete_selected(self, request, queryset):
        for obj in queryset:
             obj.delete()
    Delete_selected.short_description = "Delete selected objects"

class UserAdmin(admin.ModelAdmin):
        list_display =["id","username","password","last_login","is_staff","is_active","is_Superuser" ]
        
     #return  Client.first_name
class MoneyReserveAdmin(admin.ModelAdmin):
    list_per_page=5
    list_display = ['id','amount']
       
    def get_queryset(self, request):
        return super(MoneyReserveAdmin, self).get_queryset(request).annotate(
            amount_count=Count('amount'))
            #,
            #books_sum_price=Sum('books__price'))

class CcAdmin(admin.ModelAdmin):
    list_display = ['id','date_entered','debit','credit','description','transaction_type','category','source_id'
]
class VentureCcAdmin(admin.ModelAdmin):
    list_display = ['id','date_entered','debit','credit','description','transaction_type','category','source_id'
]
class SavingAdmin(admin.ModelAdmin):
    list_display = ['id','date_entered','debit','credit','description','transaction_type','category','source_id'
]
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','date_entered','debit','credit','transaction_type','category','source_id'
]

class LoanAdmin(admin.ModelAdmin):
    list_display = ['id','date_entered','source_type','source_id','cc_id','saving_id','cc_loan','saving','percent','flag','note_id'
]
class PendingLoanAdmin(admin.ModelAdmin):
    list_display = ['id',"loan_id",'source_type','source_id','cc_loan','saving','percent'
]
class NoteAdmin(admin.ModelAdmin):
    list_display = ["source_id",'note','category'
]

class VentureAdmin(admin.ModelAdmin):
    list_display = ['id','seller','customer','transaction_type','date_entered','source_type','amount','seller_source_id','customer_source_id','cc','category','percent','flag']
class TradingModelAdmin(admin.ModelAdmin):
    list_display = ['id','seller','customer','transaction_type','date_entered','source_type','amount','seller_source_id','customer_source_id','cc','percent','flag']

class IdRepositoryModelAdmin(admin.ModelAdmin):
    list_display = ['code','counter']
class VentureWalletModelAdmin(admin.ModelAdmin):
    list_display = ['id','date_entered','debit','credit','description','transaction_type','category','source_id'
]
class Change_TableAdmin(admin.ModelAdmin):
    list_display = ['id','change','venture_id','destination_acct_code',"destination_acct_code"
]
 
class LoanSummaryModelAdmin(admin.ModelAdmin):
    list_display = ['id','member_id','percent','max_loan',"date_entered"
]
    

class tmpVariablesModelAdmin(admin.ModelAdmin):
    list_display = ['id','max_loan'
]
    
class dayTransactionModelAdmin(admin.ModelAdmin):
    list_display = ['id','account_code','category','customer','in_charge','date_entered','source_type','amount','source_id'
]
class JoinModelAdmin(admin.ModelAdmin):
    list_display = ['name','birthday','phone','address','email'
]
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['name','email','message'
]

class LoadModelAdmin(admin.ModelAdmin):
    list_display = ['name','phone','carrier','amount'
]  
class RepairModelAdmin(admin.ModelAdmin):
    list_display = ['name','phone','description','email'
] 
class MechanicModelAdmin(admin.ModelAdmin):
    list_display = ['name','phone','description','email','category'
]
class ConstructionModelAdmin(admin.ModelAdmin):
    list_display = ['name','phone','category','message','email'
]
class DeliveryModelAdmin(admin.ModelAdmin):
    list_display = ['name','phone','address','recepient_address','recepient','recepient_phone','message'
]    

class LivePostModelAdmin(admin.ModelAdmin):
    list_display = ['status','remarks','category','customer','in_charge','active'
]  
    

admin.site.register(ProfileModel,ProfileModelAdmin)  

admin.site.register(LivePostModel,LivePostModelAdmin)  
admin.site.register(DeliveryModel,DeliveryModelAdmin)  
admin.site.register(ConstructionModel,ConstructionModelAdmin)  
admin.site.register(RepairModel,RepairModelAdmin)

admin.site.register(MechanicModel,MechanicModelAdmin)

admin.site.register(LoadModel,LoadModelAdmin)

admin.site.register(MessageModel,MessageModelAdmin)

admin.site.register(JoinModel,JoinModelAdmin)

admin.site.register(dayTransactionModel,dayTransactionModelAdmin)
admin.site.register(tmpVariables,tmpVariablesModelAdmin)
admin.site.register(LoanSummaryModel,LoanSummaryModelAdmin)

admin.site.register(VentureWalletModel,VentureWalletModelAdmin)
admin.site.register(TradingModel,TradingModelAdmin)


admin.site.register(VentureModel,VentureAdmin)
admin.site.register(MemberModel,MemberAdmin)
admin.site.register(Tmp_UsernameModel)
admin.site.register(Tmp_PasswordModel)
admin.site.register(TransferModel)
admin.site.register(UserPreferenceModel)
admin.site.register(WalletModel,WalletAdmin)

admin.site.register(VentureCcModel,VentureCcAdmin)
admin.site.register(CcModel,CcAdmin)
admin.site.register(SavingModel,SavingAdmin)
admin.site.register(PersonalLoanModel,LoanAdmin)
admin.site.register(PaymentModel,PaymentAdmin)
admin.site.register(PendingLoanModel,PendingLoanAdmin)
admin.site.register(NoteModel,NoteAdmin)
admin.site.register(IdRepositoryModel,IdRepositoryModelAdmin)
admin.site.register(Change_Table,Change_TableAdmin)












 

   