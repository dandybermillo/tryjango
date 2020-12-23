from django.contrib.auth.decorators import login_required

from .forms import ContactModelForm

from fx.models import WalletModel,MemberModel
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MemberForm  
from django.contrib import messages
from .views import get_user_preference
from .tables import myTable
from django.http import JsonResponse



def services(request):
         context ={'message':" Services offered"}
         return render(request, "fx/users/services.html", context) 
def contact(request):
         context ={'message':" Contact Us"}
         return render(request, "fx/users/contact.html", context) 
def join(request):
         print("--------------------->")
         form = ContactModelForm()
        
         if request.is_ajax and request.method == "POST":
                form = ContactModelForm(request.POST)
                print(request.POST)
                if form.is_valid():
                    form.save()
                    return JsonResponse({
                        'message': 'success'
                    })
         return render(request, "fx/users/join.html", {'form':form}) 
def about(request):
         context ={'message':"About Us"}
         return render(request, "fx/users/about_us.html", context) 
     
def user_dashboard(request,id=0):
    
    member_info  = get_member_info(request) 
    if  id > 0 and id != member_info.id:
         print(" id and request id   is not same.")
         context ={'message':" Sorry. This  page is for authorized user only. Thank you."}
         return render(request, "fx/messages/pagenotfound.html", context) 
 
    
     
   # if member_info.id != request.user.id:  #for unauthorized user
    #    return None #todo add page not found template 
    #member_info= Client.objects.get(id = id) #todo add exception
    
    class obj:
        pass
    table =obj()
    table.cards=[]
      
     
    table.cards.append({"name":"ewallet","card_name":"E-Wallet","id":id})
    # table.cards.append({"name":"store","card_name":"store","id":1})
    # table.cards.append({"name":"Cash On Hand","card_name":"COH","id":0})
    table.template_name = "fx/users/templates/card_template.html"
     
    context={
      "table":table,
      "member_info":member_info,
      "State":{"dashboard":"active"}
    }   
    
    return render(request, "fx/users/dashboard.html", context)


