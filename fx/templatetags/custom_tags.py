from django import template
from django.utils.safestring import mark_safe
from fx.models import TransferModel
from fx.views import get_running_finance_balance,get_cash_on_hand_balance
from fx.views import abbrNum
from django.db.models import Sum
from django.apps import apps



register = template.Library()

from django.contrib.auth.models import User
@register.inclusion_tag('fx/results.html')
def show_results(value,fields,xtra):
     # obj = User.objects.values_list('username', flat=True)
      return {'model': value,'fields':fields,'xtra':xtra}



@register.simple_tag
def getattribute(value,col_name):
     val = getattr(value,col_name)
     return  val 

@register.simple_tag
def getbalance(member_id,include_transactions =False,model="wallet"):
   
      model_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel"}
      model =model_list.get(model.lower())
      print(f"....getbalance:model:{model}")
      #get_cash_on_hand_balance():
    # qs_deposit = Wallet.objects.filter(transaction_type ='D').aggregate(total_deposit=Sum('credit'))
    # qs_withdrawal = Wallet.objects.filter(transaction_type ='W').aggregate(total_withdrawal=Sum('debit'))
    # cash_on_hand_balance = qs_deposit['total_deposit']  - qs_withdrawal['total_withdrawal'] 
    # return {'cash_on_hand_balance':cash_on_hand_balance,'cash_in':qs_deposit['total_deposit'],'cash_out':qs_withdrawal['total_withdrawal'] }
     
      transaction={}
      transaction_short={}
      print(f"@ getbalance member_id:{member_id}, model:{model}")
      if  member_id == 0:
         cash_on_hand = get_cash_on_hand_balance()
         print(f"cash_on_hand:{cash_on_hand}")
         cash_on_hand_balance =cash_on_hand['cash_on_hand_balance']
         print(f"cash_on_hand_balance:{cash_on_hand_balance}")
         cashTransfer = TransferModel.objects.filter(status ='W').aggregate(total_cashTransfer=Sum('amount'))
         if not cash_on_hand['cash_in']:
            cash_on_hand['cash_in'] =0
         if not cashTransfer['total_cashTransfer']:
            cashTransfer['total_cashTransfer'] =0
         print(f"@ getbalance cash_on_hand['cash_in']:{cash_on_hand['cash_in']}, ['total_cashTransfer']:{ cashTransfer['total_cashTransfer']}")

         cash_on_hand['cash_in'] =cash_on_hand['cash_in'] + cashTransfer['total_cashTransfer']
         #cash_on_hand['cash_out'] = cash_on_hand['cash_out'] 
         cash_on_hand_balance = cash_on_hand_balance + cashTransfer['total_cashTransfer']

         transaction["cash_in"] = round(cash_on_hand['cash_in'],4)
         transaction["cash_out"] =round(cash_on_hand['cash_out'],4)
         transaction_short["cash_in"] = abbrNum(cash_on_hand['cash_in'],2)
         transaction_short["cash_out"] = abbrNum(cash_on_hand['cash_out'],2)
         cash_on_hand_balance = abbrNum(cash_on_hand_balance,2)
         # if cash_on_hand_balance > 0:
             
         # print(f">>>>> cash_on_hand_balance:{cash_on_hand_balance}")  
         running_balances ={'balance':cash_on_hand_balance,'transaction':transaction,'transaction_short':transaction_short}

         return running_balances

      
      
      try:
         # if model == "Wallet":
         #    filter_field ="member_id"
         #    filter_field_value= member_id 
         # else: #Cc,Saving,payment
         filter_field ="member_id"
         filter_field_value = member_id
         model_running_balance = get_running_finance_balance(model.replace('Model','').lower(),filter_field, filter_field_value)["running_balance"]
        # print(f"model:{model} @ getbalance,model_running_balance:{model_running_balance}")
         model_running_balance =round(model_running_balance,4)
         balance_long = model_running_balance
         model_running_balance = model_running_balance
         
         balance_long = model_running_balance

         model_running_balance= abbrNum(model_running_balance,2) 
      except Exception as e:
            print (f"erorr:{e}, {type(e)}") #todo modify
            model_running_balance =0
         #wallet_running_balance= abbrNum(wallet_running_balance,2) 
      #saving_running_balance = abbrNum(saving_running_balance,2)
      
      if include_transactions:
            filter_dict = {filter_field: filter_field_value}
            Model = apps.get_model('fx', model)
            qs_deposit = Model.objects.filter( **filter_dict, transaction_type ='D').aggregate(total_deposit=Sum('credit'))
            qs_withdrawal = Model.objects.filter( **filter_dict,transaction_type ='W').aggregate(total_withdrawal=Sum('debit'))
            
            if not qs_deposit['total_deposit']:
               qs_deposit['total_deposit'] =0
            else:
                qs_deposit['total_deposit'] =round( qs_deposit['total_deposit'],4)
            if not qs_withdrawal['total_withdrawal']:
                qs_withdrawal['total_withdrawal'] =0
            else:
               qs_withdrawal['total_withdrawal'] = round(qs_withdrawal['total_withdrawal'])
            transaction["cash_in"] = qs_deposit['total_deposit']
            transaction["cash_out"] =qs_withdrawal['total_withdrawal']

            transaction_short["cash_in"] = abbrNum(qs_deposit['total_deposit'],2)
            transaction_short["cash_out"] = abbrNum(qs_withdrawal['total_withdrawal'],2)
            


      print(f" transaction: {transaction}")
      running_balances ={'balance':model_running_balance,'balance_long':balance_long,'transaction':transaction,'transaction_short':transaction_short}
 
      return running_balances
  

 