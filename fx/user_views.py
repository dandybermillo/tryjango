from django.contrib.auth.decorators import login_required


from fx.models import WalletModel,MemberModel
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MemberForm  
from django.contrib import messages
from .views import get_user_preference
from .tables import myTable

def get_member_info(req):
    try:
       member_info  = MemberModel.objects.get(user_id =req.user.id) 
    except  MemberModel.DoesNotExist:
               print(f" id:{req.user.id}  @user_dashboard----------------")
               context ={'message':" Sorry. This user does not exist. Thank you."}
               return render(req, "fx/messages/pagenotfound.html", context) 
    return member_info

@login_required(login_url='/login/')
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


 
@login_required(login_url='/login/')
def user_finance(request,id):
        # if (id == 0):
        #     id  = Client.objects.get(user_id =request.user.id).id
        
        member_info  = get_member_info(request) 
        print(f"id:{id}, member_info.id: {member_info.id}")
        if  id != member_info.id:
            print(" id and request id is not same.")
            context ={'message':" Sorry. This  page is for authorized user only. Thank you."}
            return render(request, "fx/messages/pagenotfound.html", context) 
 
          
      
 
        #member_info= Client.objects.get(id = id) #todo add exception
         #todo if the id is the same as user.authenticated o
       # return redirect('/update_user_details/',client.id)
        user_prefered_nos_rows = get_user_preference(member_info.id)
        wallet_detail =Wallet.objects.raw('''select "fx_wallet"."id","fx_wallet"."transaction_type","fx_wallet"."description","fx_wallet"."credit","fx_wallet"."debit", sum("fx_wallet"."credit") over (order by "fx_wallet"."id" ) - sum("fx_wallet"."debit") over (order by "fx_wallet"."id")  as balance from "fx_wallet" where "fx_wallet"."walletTransaction_id" = {}  order by "fx_wallet"."id" desc   limit {}'''.format(memberTrans.id,user_prefered_nos_rows))
        total_rows = Wallet.objects.filter(member_id =member_info.id).count()
       
       
        table = myTable(data=wallet_detail,filter_field_value= member_info.id,total_rows=total_rows,user_prefered_nos_rows=user_prefered_nos_rows,model= 'Wallet')
        table.member_id =member_info.id
        table.template_name = "fx/users/templates/table.html"
        context={
             "member_info":member_info,
             "table":table,
             'State':{"account":"active"}
         }
        return render( request,"fx/users/user_finance.html",context)

@login_required(login_url='/login/')
def update_user_info(request, id=id):  # display and update
            member_info  = get_member_info(request) 
            print(f"id:{id}, member_info.id: {member_info.id}")
            if  id != member_info.id:
                print(" id and request id   is not same.")
                context ={'message':" Sorry. This  page is for authorized user only. Thank you."}
                return render(request, "fx/messages/pagenotfound.html", context)
            
            if request.method == "GET":
                    # member_info = get_object_or_404(Client, id=id)
                    form = MemberForm(instance=member_info)
                    context = {
                        'form': form,
                        'member_info': member_info,
                        'State':{"profile":"active"}
                    }
                    return render(request, "fx/users/update_user_info.html", context)
            else:     
                        # try:
                        #     member_info = Client.objects.get(id=id)
                     
                       
                        memberForm = MemberForm(request.POST , instance=member_info)
                        
                        if memberForm.is_valid():
                            updated_Member= memberForm.save()
                            context = {
                                    
                                    'form': memberForm,
                                    'no_save_button':True,
                                    'member_info': member_info,
                                    'State':{"profile":"active"}
                                     
                                 }
                            messages.success(request, 'Your personal infomation has been successfully updated!') 
                            return render(request, "fx/users/update_user_info.html", context)          
                        else:  #invalid form  for existing record
                             context = {
                                     'form':memberForm,  #tsomething wrong here
                                     'member_info':member_info,
                                     'State':{"account":"active" }
                                     
                                    
                                 }
                        return render(request, "fx/users/update_user_info.html", context)

                            
 