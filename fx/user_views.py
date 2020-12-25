from django.contrib.auth.decorators import login_required

from .forms import SignUpModelForm,MessageForm,LoadForm

from fx.models import WalletModel,MemberModel,MessageModel
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MemberForm  
from django.contrib import messages
from .views import get_user_preference
from .tables import myTable
from django.http import JsonResponse



def services(request):
      
         print("--------------------->contact")
         form_load = LoadForm()
         print(f" is ajax: {request.is_ajax}")
         if request.is_ajax and request.method == "POST":
                print("pass if;;")
              
                try: 
                     form_load = LoadForm(request.POST)
                except   Exception as e:
                        print(f"e: {e}")
                print(f" re: {request.POST}")
                if form_load.is_valid():
                    try: 
                         form_load.save()
                    except   Exception as e:
                        print(f"e: {e}")
                    return JsonResponse({
                        'message': 'success'
                    })

                else:
                     print("not valid")  
                     #print(f"errors: {form_message.errors['foo']}")
                     print(f"form:{form_load}")
                     error_list =""
                     for field, errors in form_load.errors.items():
                        print(f"Field: {field} Errors: {errors}")
                        error_list =errors
                     return JsonResponse({
                        'message': error_list
                    })
         else:
              print("else:")
              print(request.POST)  
         print("Exit")                
         return render(request, "fx/users/services.html",{'form_load':form_load}) 
def contact(request):
         print("--------------------->contact")
         form_message = MessageForm()
         print(f" is ajax: {request.is_ajax}")
         if request.is_ajax and request.method == "POST":
                print("pass if;;")
              
                try: 
                     form_message = MessageForm(request.POST)
                except   Exception as e:
                        print(f"e: {e}")
                print(f" re: {request.POST}")
                if form_message.is_valid():
                    try: 
                         form_message.save()
                    except   Exception as e:
                        print(f"e: {e}")
                    return JsonResponse({
                        'message': 'success'
                    })

                else:
                     print("not valid")  
                     #print(f"errors: {form_message.errors['foo']}")
                     print(f"form:{form_message}")
                     error_list =""
                     for field, errors in form_message.errors.items():
                        print(f"Field: {field} Errors: {errors}")
                        error_list =errors
                     return JsonResponse({
                        'message': error_list
                    })
         else:
              print("else:")
              print(request.POST)  
         print("Exit")                
         return render(request, "fx/users/contact.html",{'form_message':form_message}) 
def join(request):
         print(f"---------------------> user{ request.user}")
         form = SignUpModelForm()
        
         if request.is_ajax and request.method == "POST":
                form = SignUpModelForm(request.POST)
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


