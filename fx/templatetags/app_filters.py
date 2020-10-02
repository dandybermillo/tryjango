

from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='get_due_date_string')
def get_due_date_string(value):
    print(f"get_due_date_string{value}")
    month={1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"June",7:"Jul",8: "Aug",9:"Sept",10:"Oct", 11:"Nov",12:"Dec"}
    delta = date.today() - value 
    

    if delta.days == 0:
        return "Today"
    
    elif delta.days == 1:
        return "Yesterday"
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