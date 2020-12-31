

from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='get_due_date_string')
def get_due_date_string(value):
   # print(f"get_due_date_string{value}")
    month={1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"June",7:"Jul",8: "Aug",9:"Sept",10:"Oct", 11:"Nov",12:"Dec"}
    delta = date.today() - value 
    

    if delta.days == 0:
        return "Today"
    
    elif delta.days == 1:
        return "1 day ago"
    elif delta.days > 1 and  delta.days < 8:
        return "%s %s ago" % (abs(delta.days),
            ("day" if abs(delta.days) == 1 else "days"))
    else:
        today  = date.today()
        
        if value.year == today.year:
            return  f"{month[value.month]} {value.day}"
        else:
            value

        return  value
    # elif delta.days > 1:
    #     return "In %s days" % delta.days
@register.filter(name='convert_option')
def convert_option(value):
  
   TX_PAYMENT,TX_LOAN_PAYMENT,TX_VENTURE,TX_TRANSACTION,TX_DEPOSIT,TX_WITHRAWAL,TX_GROCERY,TX_SERVICES=(0,1,2,3,4,5,6,7)
   cat ={TX_TRANSACTION:"REGULAR TRANSACTION",TX_PAYMENT:"PAYMENT",TX_VENTURE:"VENTURE",TX_DEPOSIT:"DEPOSIT",TX_WITHRAWAL:'WITHRAWAL',TX_GROCERY:'GROCERY',TX_SERVICES:'SERVICES',TX_LOAN_PAYMENT:"LOAN PAYMENT"}
   print(f"cat 1: { cat.get(1)}")
   print(f"cat 2: { cat.get(2)}")
   print(f"cat 5: { cat.get(5)}")
   print(f"TX_DEPOSIT: { cat.get(TX_DEPOSIT)}")
   print(f"value : {value}")
   return  cat.get(value)