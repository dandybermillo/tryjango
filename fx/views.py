#1 Transfer_check_balance
#2 update_transfer_status
#3 wallet_new_transaction
#4 create_update_member_wallet

from django.views.decorators.csrf import csrf_exempt


import ast, base64
from datetime import date,datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.views.defaults import page_not_found

from django.shortcuts import render, get_object_or_404, redirect, Http404
from .forms import MemberForm,UserLoginForm,PersonalLoanForm,PaymentForm,VentureForm,TradeForm
from fx.models import MemberModel,Tmp_UsernameModel,Tmp_PasswordModel,VentureModel,IdRepositoryModel 
from fx.models import PersonalLoanModel,CcModel,SavingModel,PaymentModel,PendingLoanModel,NoteModel,VentureWalletModel,VentureCcModel,TradingModel
from fx.models import MechanicModel,LoanSummaryModel,tmpVariables,dayTransactionModel,JoinModel,MessageModel,LivePostModel,ProfileModel,RepairModel,DeliveryModel,ConstructionModel,LoadModel
from fx.models import Change_Table,ProductModel,ProductSold,CustomerNoteModel,CreditLineModel
from .forms import WalletForm,SavingForm

from fx.models import WalletModel,CodeGeneratorModel,UserPreferenceModel
from datetime import  date
from datetime import datetime, timedelta 
from django.contrib.auth.decorators import login_required
import random
from django.views.generic import ListView
from .tables import TransferReceiver_cls,SearchMember
from django.db.models import Q,F,Sum
from django.contrib.messages import constants as messages
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import template
from django.core.validators import EmailValidator, ValidationError
from django.core.exceptions import ObjectDoesNotExist

from django import forms
from .models import TransferModel
from django.http import JsonResponse
from django.core import serializers
from django import template

from django.template.defaultfilters import stringfilter
import json
from django.apps import apps
from .tables import myTable
from django.contrib.auth.models import  Group

from datetime import timedelta
#test
from django.views.generic import View
from time import time
#end test
from django.core import serializers

#error logging
import logging,traceback
# logger = logging.getLogger(__name__)
logger = logging.getLogger("django")
#error logging end

#register = template.Library()
walk_in_id = 4
minimum_deposit = 0
maximum_deposit =10000
limits ={"minimum_deposit":minimum_deposit,"maximum_deposit": maximum_deposit}
#source_model_list= {"venture":"VentureModel","trading":"TradingModel"}


model_list= {"venture":"VentureModel","trade":"TradingModel"}
Model_data_list ={"live":"LivePostModel","profile":"ProfileModel","message":"MessageModel","join":"JoinModel","mobile":"LoadModel","repair":"RepairModel","mechanic":"MechanicModel","delivery":"DeliveryModel","construction":"ConstructionModel"}
model_list_change= {"WALLET ACCT":"WalletModel","SAVING ACCT":"SavingModel"}




CREATE,UPDATE,DELETE =(0,1,2)
TX_PAYMENT,TX_LOAN_PAYMENT,TX_VENTURE,TX_TRANSACTION,TX_DEPOSIT,TX_WITHRAWAL,TX_GROCERY,TX_SERVICES=(0,1,2,3,4,5,6,7)

NEW_RECORD, EDIT_RECORD, DELETE_RECORD =(0,1,2)
SOURCE_TRADING,SOURCE_VENTURE,SOURCE_REGULAR =(1,2,3)
NO_ACCOUNT,ACCOUNT_SAVINGS,ACCOUNT_WALLET,ACCOUNT_CC,ACCOUNT_VENTURE,ACCOUNT_PAYMENT =(0,1,2,3,4,5)
CAT_REG_TRANSACTION,CAT_TRANSFER,CAT_GROCERY,CAT_LOAN,CAT_VENTURE,CAT_TRADE =(0,1,2,5,6,7)
source_funds_cc= {SOURCE_VENTURE:"VentureCcModel",SOURCE_TRADING:"CcModel",SOURCE_REGULAR:"CcModel"}
source_funds_pm= {SOURCE_VENTURE:"VentureWalletModel",SOURCE_TRADING:"WalletModel",SOURCE_REGULAR:"WalletModel"}
#21
TRANS_PAYMENT,TRANS_VENTURE,TRANSACTION=(0,1,2)

@login_required(login_url='/login/')
def user_login_success(request,id):
      #  return render(request, 'fx/users/user_page.html', {'posts':"posts"})  
        print(f"--- user id: {id}")
        user_id =id
        member_id=""
        try:
                qs = MemberModel.objects.get(user_id = user_id)
                
                
                
                
                id = qs.id
                member_id = qs.member_id
                print(f"id: {id}--- member id: {member_id}")
                print(" successfull!")
        except Exception as e: 
                #todo
                print(f"LoginView e: {e} ")
        print(f" id : {id}")
        
        try:
              member_qs = ProfileModel.objects.get(source_id = id)
             
              member_qs.id  = id
              member_qs.member_id =member_id
              print(f"passs try,member_qs.id:{id} ")
        except Exception as e:
              print("no data yet at profileModel")
              print(f"user_login_success: {e} ")
              try:
                 member_qs = MemberModel.objects.get(id = id)
              except Exception as e:
                   print(f"user_login_success: {e}")
        
        tx = dayTransactionModel.objects.filter(date_entered__lte=datetime.today(), date_entered__gt=datetime.today()-timedelta(days=30), customer =id).order_by("-pk") #.values('createdate').annotate(count=Count('id'))
       
        
        
        #employees = Employee.objects.all().values('id','name','company__name')
        APPROVED = 2
        live = LivePostModel.objects.all().values("status","remarks","customer__member_id").filter(customer_id = id,code =APPROVED)
        pwd=""
        try:
                    pwd = Tmp_PasswordModel.objects.get(member_id = id).pwd.strip()
                    print(f"------------:{pwd} , len: {len(pwd)}")
                    pwd = base64.b64decode(pwd)
                    print(f"second------------{pwd} , len: {len(pwd)}")
                    pwd =pwd.decode("utf-8")
                    print (f"...retrieve.pwd from Tmp_PasswordModel : {pwd}")
        except Exception as e:
                    print (f"decode pass at login success: {e}, {type(e)}")
                    
        print(f"----qrcode : {create_qrcode_code(member_qs.member_id,pwd)}")
        # print(f"member_qs. member_id: {member_qs.member_id}")
        member_qs.qrcode = create_qrcode_code(member_qs.member_id,pwd)
        decosde = decode( member_qs.qrcode)
        print(f"----- decosde: {decosde}")
        print(f"------------- qrcode create:{member_qs.qrcode }")
        context ={'message':" Welcome to Fair Exchange!",
                  "member":member_qs,
                  "tx":tx,
                  'live':live,
                  'asset_liabities':get_all_balances(id)}
        return render(request, "fx/users/main/member_index.html",context)  
        
  

    # return HttpResponse(f"<h1 >Login success. logged in username: { request.user.username }</h1>")
def livePost(request,id,code):
   # print("livePost")
   # live_code = request.GET.get("live_code", -1).strip()
    #live_code =int(live_code)
   # print(f" live_code: {code}, {type(code) }")

    try:
                    # live = LivePostModel.objects.all().values("status","remarks","customer__member_id").filter(customer_id = id,active =True)
                #print(id)
                APPROVED = 2
                if id == 0: # 1 means ready 
                        fields = {"code":APPROVED}
                else:
                        fields = {"code":APPROVED,'customer_id':id}
                if code > 0:
                    fields['category']=code
                #print(f"id: {id} fields: {fields}")
                qs = LivePostModel.objects.all().values("status","remarks","customer__member_id","category").filter( **fields)
                
                data=[]
                for row in qs:
                    # row ={"id":row["customer__member_id"],"status":row.status,"remarks":qs.remarks}
                    #  print(f"row:{row}")
                    data.append(row) 
                return JsonResponse({"live":data},status =200) 
    except Exception as e:

       print(f"ERROR,LivePost: e:{e}")
       return JsonResponse({"live":{}},status =400) 
def livePost_services(request):
   # print("live services")
      #    MOBILE,COMPUTER_REPAIR,MECHANIC,CONSTRUCTION,DELIVERY =(1,2,3,4,5)
    walk_in =4

    try:
                    # live = LivePostModel.objects.all().values("status","remarks","customer__member_id").filter(customer_id = id,active =True)
                #print(id)
                
                data=[]
               #         tx = dayTransactionModel.objects.filter(date_entered__lte=datetime.today(), date_entered__gt=datetime.today()-timedelta(days=7), customer =id).order_by("-pk")   #.values('createdate').annotate(count=Count('id'))
                filter_fields = { }
                qs = RepairModel.objects.all().values("source_id","served","name","source__id","source__member_id","source__gender","source__firstname","source__lastname","source__telephone","phone","description").filter( served = False,date_entered__lte=datetime.today(),date_entered__gt=datetime.today()-timedelta(days=2))
                 
               
                for row in qs:
                    row["category"] = 2
                    print(f"------id: {row['source__id']}")
                    if row['source__id'] == walk_in :
                        del row["source__firstname"]
                        del row["source__lastname"]
                        del row["source__gender"]
                        del row["source__telephone"]
                     
                    # row ={"id":row["customer__member_id"],"status":row.status,"remarks":qs.remarks}
                    
                    data.append(row)
                qs = DeliveryModel.objects.all().values("source_id","served","name","source__id","source__member_id","source__gender","source__firstname","source__lastname","source__telephone","phone","message").filter(  served = False,date_entered__lte=datetime.today(),date_entered__gt=datetime.today()-timedelta(days=2))
                
                
                for row in qs:
                    row["category"] = 5
                    if row['source__id'] == walk_in :
                        del row["source__firstname"]
                        del row["source__lastname"]
                        del row["source__gender"]
                        del row["source__telephone"]
                    # row ={"id":row["customer__member_id"],"status":row.status,"remarks":qs.remarks}
                    
                    data.append(row) 
                qs = ConstructionModel.objects.all().values("source_id","served","name","source__id","source__member_id","source__gender","source__firstname","source__lastname","source__telephone","phone","message").filter(  served = False,date_entered__lte=datetime.today(),date_entered__gt=datetime.today()-timedelta(days=2))
                for row in qs:
                    row["category"] = 4
                    # row ={"id":row["customer__member_id"],"status":row.status,"remarks":qs.remarks}
                    if row['source__id'] == walk_in :
                        del row["source__firstname"]
                        del row["source__lastname"]
                        del row["source__gender"]
                        del row["source__telephone"]
                    data.append(row) 
                
                qs = MechanicModel.objects.all().values("source_id","served","name","source__id","source__member_id","source__gender","source__firstname","source__lastname","source__telephone","phone","description").filter(  served = False,date_entered__lte=datetime.today(),date_entered__gt=datetime.today()-timedelta(days=2))
                for row in qs:
                    row["category"] = 3
                    # row ={"id":row["customer__member_id"],"status":row.status,"remarks":qs.remarks}
                    if row['source__id'] == walk_in :
                        del row["source__firstname"]
                        del row["source__lastname"]
                        del row["source__gender"]
                        del row["source__telephone"]
                    data.append(row) 

                qs = LoadModel.objects.all().values("source_id","served","name","source__id","source__member_id","source__gender","source__firstname","source__lastname","source__telephone","phone","description").filter(  served = False,date_entered__lte=datetime.today(),date_entered__gt=datetime.today()-timedelta(days=2))
                    
                for row in qs:
                    row["category"] = 1
                    
                    # row ={"id":row["customer__member_id"],"status":row.status,"remarks":qs.remarks}
                   # print(f"row:{row}")
                    if row['source__id'] == walk_in :
                        del row["source__firstname"]
                        del row["source__lastname"]
                        del row["source__gender"]
                        del row["source__telephone"]
                    data.append(row) 
                
                
                 
            
            
            
                return JsonResponse({"live":data},status =200) 
    except Exception as e:

       print(f"ERROR,LivePost: e:{e}")
       return JsonResponse({"live":{}},status =400) 
def worker_task(request,id):
    print(f"id:: {id}")
    try:
 
                qs = LivePostModel.objects.all().values("in_charge","status","remarks","customer__member_id","customer__gender","customer__lastname","customer__firstname",).filter( in_charge = id)
                
                data=[]
                for row in qs:
                    # row ={"id":row["customer__member_id"],"status":row.status,"remarks":qs.remarks}
                    #  print(f"row:{row}")
                    data.append(row) 
                return JsonResponse({"worker_task":data},status =200) 
    except Exception as e:

       print(f"ERROR,LivePost: e:{e}")
       return JsonResponse({"live":{}},status =400) 
class LoginView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        print (f"--password:  {password}")
        print(f" user: {username}")

        if username == "" or password=="":
            return JsonResponse({"type": "error", "message": "Please input both username & password"})

        user = authenticate(username= username, password=password)
        
        print(f"user: {user}")
        print(f"user id: {user.id}")
        if user is not None:
            
            login(request, user)
            # try:
            #     id = MemberModel.objects.get(user_id = user.id).id
            #     print(f"--- id: {id}")
            #     print(" successfull!")
            # except Exception as e: 
            #     #todo
            #     print(f"LoginView e: {e} ")
            return JsonResponse({"type":'success', "message":"Login Success","id":user.id})
        else:
            print(" access denied!")
            return JsonResponse({"type": "error", "message": "Invalid Credentials"})#test

        

    
    
       
class Process_Data_View(View):
    def post(self, request, *args, **kwargs):
        print("processing data!")
        lists =["customer__member_id","id","source_id","gender","firstname","lastname","middlename","name","address","phone","telephone","message","description","email","birthday","amount","carrier","amount","recepient_phone","recepient","recepient_address","remarks","status","member_id"]
        #request.post: <QueryDict: {'csrfmiddlewaretoken': ['e6zJhjN1iSYstCJmxrZ9kHM4VeEWB6SVlCFIQpPHA0stQEcWWPyd6sPeAtfuFMtP'], 'code': ['delivery'], 'name': ['da'], 'phone': ['232323232323'], 'email': ['dandybermillo@yahoo.com'], 'address': ['pili'], 'recepient': ['dad rec'], 'recepient_phone': ['232323232323'], 'recepient_address': ['asdfsf'], 'message': ['hi there']}>
        filter_fields ={}
        id=0 # use id instead of source_id or vice versa
        for key, value in request.POST.items():
                if key in lists:
                     filter_fields[key] = value
                print('Key: %s' % (key) ) 
                # print(f'Key: {key}') in Python >= 3.7
                print('Value %s' % (value) )
                # print(f'Value: {value}') in Python >= 3.7
        print(f"filter fields: {filter_fields}")
        
        # print("process data....")
        # name = request.POST.get('name')
        # phone = request.POST.get('phone')
        # email = request.POST.get('email')
        # message = request.POST.get('message')
        # address = request.POST.get('address')
        print(f"request.post: {request.POST}")
        code = request.POST.get('code').strip()
        
        source_id = request.POST.get('source_id',"0").strip()
        source_id = int(source_id)
        
        #just added
        id =  request.POST.get('id',"0").strip()
        id = int(id)
        # if source_id == 0:
        #      id =  request.POST.get('id',"0").strip()
        #      id = int(id)
        #      source_id = id
        
       # if code=- "live"
       # source_id = int(source_id)
        del filter_fields["id"]
        print(f"filter fields: {filter_fields}")
       
         
         
        model_name =Model_data_list.get(code) 
        
        Model = apps.get_model('fx', model_name)
       
        print(f"id= {id} code :{code}, source_id: {source_id} ,type: {type(source_id)} , modelname: {model_name}")
        
        # if source_id  < 0:
        #      return JsonResponse({"type":'error', "message":"source_id  < 0"})
             
        if id <= 0:  
            
                    try:
                        print("ADDING...........")
                            #create_update_cc("CREATE",amount,customer_id,0,"GROCERY")
                        process_data = Model( **filter_fields) #name=name,phone=phone,email=email,birthday =birthday,address = address)
                        process_data.save() 
                        print("success writing")
                        return JsonResponse({"type":'success', "message":"Your data has been saved!"})
                    except Exception as e:
                        print(f"@ exception e:{e}")
                        logger.warning(f"Process_Data_View(View): exception e:{e}")
                        return JsonResponse({"type": "error", "message": "unable to save this data"})#test
        
        else:
            
                    try:
                          print("UPDATING...........")
                          if id > 0:
                              update_qs = Model.objects.filter(id = id).update( **filter_fields)
                          else:
                              update_qs = Model.objects.filter(source_id = source_id).update( **filter_fields) 
                          print(f" update_qs: {update_qs}")
                          if update_qs <=0:
                                    try:
                                        print(f" add instead of editing..... atttention")
                                        process_data = Model( **filter_fields) #name=name,phone=phone,email=email,birthday =birthday,address = address)
                                        process_data.save() 
                                        print("success writing 2")
                                        return JsonResponse({"type":'success', "message":"Your data has been saved  for approval!"})
                                    except Exception as e:
                                        print(f"@ exception e:{e}")
                                        logger.warning(f"Process_Data_View(View): 'update_qs <=0', try: e:{e}")
                                        return JsonResponse({"type": "error", "message": "unable to save this data"})#test
                          else:
                              return JsonResponse({"type":'success', "message":"Your data has been updated  for approval!"})
                              
                                
                    except  Exception as e:
                            print(f"Process Data: e: {e}")
                            logger.warning(f"Process_Data_View(View): 'update_qs = Model.objects.filter', try: e:{e}")

                            #todo log here
                 

    
class MobileView(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        select = request.POST.get('select')
        
        
        print(f"select :{select}")

        print(f"request.POST :{request.POST}")

       
        return JsonResponse({"type":'success', "message":"Your data has been saved!"})
        # else:
        #     print(" access denied!")
        #     return JsonResponse({"type": "error", "message": "Invalid Credentials"})#test

def create_post(request):
  #  posts = Post.objects.all()
    response_data = {}
    print(f"create_post: {create_post}")

    if request.POST.get('action') == 'post':
        try: 
            title = request.POST.get('title')
            description = request.POST.get('description')

            response_data['title'] = title
            response_data['description'] = description
        except Exception as e:
             print(f" Errror: {e}")

        # Post.objects.create(
        #     title = title,
        #     description = description,
        #     )
        return JsonResponse(response_data)

    return render(request, 'fx/venture/test.html', {'posts':"posts"})     

class AjaxHandlerView(View):
 
   def get(self,request):
       
      text =  request.GET.get('button_text')
      if request.is_ajax():
             t = time()
             return JsonResponse({'seconds':t}, status =200)
      return render(request,'fx/venture/test.html')
   def post(self,request):
     
      if  request.is_ajax() and request.method == "POST": 
            card_text = request.POST.get('text')
            print(f"code: {request.POST.get('code')}")
            result = f"I have : {card_text}"
            return JsonResponse({'data':result}, status =200)
      else:
           return JsonResponse({'data':'none'}, status =400)


#end test 


def parseint(string,lenght=10): #10 has no meaning
    result = '0'
    ctr = 0
    for x in string:
        if x.isdigit():
           result+=x
           ctr = ctr + 1
        else:
            return int(result)
        if ctr >= lenght:
               return int(result)
    return int(result)
def decode(qr_code):
    #rint(f"len:{len('da1010-0')}")
    #qr_code ="8da1010-09652"
    qr_code=qr_code.replace("x","-")
    print("-------------@ decode.....qr_code: "+qr_code )
    logger.info(f" decode #1: {qr_code}") #1
    
    x = parseint(qr_code,2)
    if x > 9:
        lent = 2
    else:
        lent = 1
        
    part_un = qr_code[lent+2:lent+6]
    part_pwd = qr_code[lent+x:]

    print(f"-----x:{x}, lent:{lent}, part_un:{part_un}, part_pwd:{part_pwd}") 
    logger.info(f"#2-----x:{x}, lent:{lent}, part_un:{part_un}, part_pwd:{part_pwd}") #2
    
    #get pass
    #print(f"------ username:   {qr_code[lent:x+lent]}")
    customer_id = qr_code[lent:x+lent]
    save_pwd = get_temp_pass(customer_id)
    print(f"save type: {type(save_pwd)}")
    #save_pwd =3590
    #save_pwd =pwd.decode("utf-8")
    print(f"save pwd: {save_pwd} , customer_id: {customer_id}")
    logger.info(f"#4 save pwd: {save_pwd} , customer_id: {customer_id}") #4
   # save_pwd = "1010"
    print("xxxxx")
    pwd = parseint(reverse(save_pwd))
    subtrahend = parseint(part_un) + pwd
    #print(f"subtrahend:{subtrahend}, pwd:{pwd}")
    pwd = parseint(part_pwd) - subtrahend
    pwd = reverse(str(pwd))
    if len(pwd) <= 3:
        pwd =pwd+"0"
    print("password:"+ pwd)
    print("username:"+qr_code[lent:x+lent])
    logger.info(f"#5 username {qr_code[lent:x+lent]} , password : {pwd}") #5
    return {"username":qr_code[lent:x+lent],"password":pwd}
def reverse(s): 
    str = "" 
    for i in s: 
        str = i + str
    return str


  #  return {"username":qr_code[lent:x+lent],"password":pwd}


def create_qrcode_code(username,save_pwd):
   # username ="da1212-01"
    print(f"at create_qrcode_code: {username}, pwd: {save_pwd} ")
    part_un = username[2:6].strip()
    lent = str(len(username)).strip()
    print(f"encode, lent:{lent}, partun:{part_un}")
   # save_pwd = "1359"
    pwd =parseint( reverse(save_pwd))
    part_username = parseint(part_un)
    subtrahend = part_username + pwd
    pwd =  pwd + subtrahend
    
    print(f"{lent},{username},{pwd}")
    username = username.replace("-","x")
    code =f"{lent}{username}{pwd}"
    print(f"--- code:{code}")
   # print("decoding")
   # decoded = decode(code)
   # decoded = decode("9da1212-0121210")

    return code   #.replace("-",":")
    #return f"username:{decoded['username']} ,pass:{decoded['password']}"
    
    
    
    
    
    
    
    
    

def get_temp_pass(username):
    try:   
             
            print(f"username:>{username}")
           
            message ="xusername"  #invalid username
          
            member_qs = MemberModel.objects.get(member_id=username)
            print(f"member_qs.id:{member_qs.id}")
            pwd = Tmp_PasswordModel.objects.get(member_id = member_qs.id).pwd
            pwd = base64.b64decode(pwd)
            pwd =pwd.decode("utf-8")
            print(f"at get_temp_pass,pwd: {pwd} ,username:{username}")
            logger.info(f"at get_temp_pass,pwd: {pwd} ,username:{username}")
            
            return pwd
    except Exception as e:
            print (f"def get_temp_pass: {e}, {type(e)}")
            return "" 
    
def check_user(request):
    member_id = request.POST.get("member_id", "").strip().upper()
    password = request.POST.get("password", "").strip()
    print("ajax_check_user_url.... reached")
    print(f"member_id:{member_id} , password:{password}")
    if  request.method == "POST":
            if member_id and password:
                        try:
                            user = MemberModel.objects.get(member_id = member_id).user
                            username=user.username
                            print("user name:",user.username)
                        except  Exception as e:
                            print (f"{e}, {type(e)}")
                        user = authenticate(username=username, password=password)
                        print(f"....self.user:{user}, username:{username}")
                        if user is None:
                            try:
                                # User.objects.get(username__exact=username)
                                user = User.objects.get(username__exact=username)
                                res= user.check_password(password)
                                print(f"....password:{password} , check: {res}")
                                if not user.check_password(password):
                                    print( 'Incorrect password' )
                                if not user.is_active:
                                    print('This user is not active')
                            except ObjectDoesNotExist:
                                   print('This user does not exist')
       
                               
    else:
        context = {
        'post_data':True,
    }
    return render(request, 'fx/venture/login.html', context)

                 
         
def get_product_details(request):
    print("--def get customer details")
    logger.info("--def get customer details")
    item_id = request.GET.get("item_id", "").strip().upper()
    print(f"product id: {item_id}")
    
    try:
        
         product_info_qs = ProductModel.objects.get(product_id  =item_id)  
         product_info ={"title":product_info_qs.title,"price":product_info_qs.price,"cm":product_info_qs.cm}
         print ("success readin prod detail")
         return JsonResponse({"data":"Success","product_info":product_info}, status = 200)
        
    except Exception as e:
        print(f"unable to retrieve product details: e: {e}")
        logger.warning(f"unable to retrieve product details: e: {e}")
        return JsonResponse({"data":""}, status = 200)
        
   
   
    # if from_code == "qrcode":
    #    # qrpassword = request.GET.get("qrpassword", "").strip()
    #     qrcode = customer_id.replace(":","-")
    #     qrcode = decode(qrcode)
       

    #         member_info = {"member_id":member_qs.member_id.upper(),"name":member_qs.name,"id": member_qs.id}
    #         print(f"member_info:{member_info}")
    #         #cm_balance = get_running_finance_balance("cc","member_id",member_qs.id)["running_balance"]
    #         balances =get_all_balances(member_qs.id)
    #         return JsonResponse({"data":"Success","member_info":member_info,"balances":balances}, status = 200)
    #   except Exception as e:
    #         print (f"get customer detail error: {e}, {type(e)}")
    #         logger.warning(f"{e}, {type(e)}")
    #         return JsonResponse({"message":message}, status = 200)    
    return JsonResponse({}, status = 400)



def get_customer_details_bypass(request):
    #-#
    print("--def get customer details bypass")
    logger.info("--def get customer details")
    customer_id = request.GET.get("member_id", "").strip().lower()
    
   
    # member_id_pk = request.GET.get("member_id_pk", "").strip().lower()
    # print(f"member_id_pk id: {member_id_pk} -----------------")

   
    if request.is_ajax and request.method == "GET":
      Message=""
      try:   
            message ="This user does not exist!"  #invalid username
            print(f"---customer_id:{customer_id}")
            print("------->>>>>")
            #customer_id = customer_id.upper()
            member_qs = MemberModel.objects.get(member_id=customer_id) 
            member_info = {"member_id":member_qs.member_id.upper(),"name":member_qs.name,"id": member_qs.id}
            print(f"member_info:{member_info}")
            #cm_balance = get_running_finance_balance("cc","member_id",member_qs.id)["running_balance"]
            balances =get_all_balances(member_qs.id)
            print(f"---pk:{member_qs.id}")
            notes= []
            
            try:
                notes_qs = CustomerNoteModel.objects.filter(date_entered__lte=datetime.today(), date_entered__gt=datetime.today()-timedelta(days=30),   member_id =member_qs.id).order_by("pk")[:100]
                
                for row in notes_qs:
                    row ={"id":row.id,"note":row.note,"date_entered":row.date_entered}
                    notes.append(row)
            except Exception as e:
                print(f"Retrieving customer note error: {e}")
            if member_qs.id !=   walk_in_id:
                     product_codes = ProductSold.objects.all().values("item__product_id","item__title","member").distinct('item__product_id').filter( member = member_qs.id)
            codes=[]
            for row in product_codes:
                if row["item__product_id"] != 1 and row['item__title'] !="none":
                    codes.append(row["item__product_id"])
                    print(f"id : {row['item__product_id']} title: {row['item__title']}, member: {row['member']}")
            
           
            
            
            return JsonResponse({"data":"Success","member_info":member_info,"balances":balances,'notes':notes,'product_codes':codes}, status = 200)
      except Exception as e:
            print (f"get customer detail bypass error: {e}, {type(e)}")
            logger.warning(f"get customer detail bypass error:  {e}, {type(e)}")
            return JsonResponse({"message":message}, status = 200)    
    return JsonResponse({}, status = 400)

def get_customer_details(request):
    print("--def get customer details")
    logger.info("--def get customer details")
    customer_id = request.GET.get("customer_id", "").strip().lower()
    from_code = request.GET.get("from", "manual").strip()
    qrpassword=""
    #qr_code = request.GET.get("qr_code", "").strip()

    if from_code == "qrcode":
       # qrpassword = request.GET.get("qrpassword", "").strip()
        qrcode = customer_id.replace(":","-")
        qrcode = decode(qrcode)
       

        qrpassword = qrcode["password"]
        customer_id =qrcode['username'] #qrcode['username']
        customer_id =customer_id.replace("x","-")
        # print("-------")
        print(f",,----username:{qrcode['username']}, pwd: {qrcode['password']}")
        logger.info(f" ,,----username:{qrcode['username']}, pwd: {qrcode['password']} ")
    else:
        password = request.GET.get("password", "").strip()
    if request.is_ajax and request.method == "GET":
      Message=""
      try:   
            message ="This user does not exist!"  #invalid username
            print(f"---customer_id:{customer_id}")
            print("------->>>>>")
            #customer_id = customer_id.upper()
            member_qs = MemberModel.objects.get(member_id=customer_id) 
            print(f"------id:{member_qs.id}")
            if from_code == "qrcode":
                    message ="Incorrect password!"  #invalid password
                    pwd = Tmp_PasswordModel.objects.get(member_id = member_qs.id).pwd
                    pwd = base64.b64decode(pwd)
                    pwd = pwd.decode("utf-8")
                    logger.info(f"pwd: {pwd}, qrpassword: {qrpassword}")
                    logger.info(f"pwd: {parseint(pwd)}, qrpassword: {parseint(qrpassword)}")
                    print (f"pwd: {pwd}, qrpassword: {qrpassword}")
                    print (f"pwd: {parseint(pwd)}, qrpassword: {parseint(qrpassword)}")
                    if  parseint(pwd) != parseint(qrpassword):
                         print (f"pwd not matched")
                         logger.warning(f"pwd not matched at parseint(pwd) != parseint(qrpassword)")
                        
                         return JsonResponse({"message":message}, status = 200)  
            else:
                    member_id = customer_id  # request.POST.get("customer_id", "").strip().upper()
                    logger.info(f"else of from_code == 'qrcode': member_id :{member_id}")
                    # print (f"member_id:{member_id}, password: {password}")
                    if member_id and password:
                            
                            try:
                                user = MemberModel.objects.get(member_id = member_id).user
                                username = user.username
                                print("user name:",user.username)
                            except  Exception as e:
                                print (f" here: {e}, {type(e)}")
                                logger.info(f"if member_id and password: {e}, {type(e)} : This user does not exist")
                                return JsonResponse({"message":'This user does not exist'}, status = 200) 
                            user = authenticate(username=username, password=password)
                            print(f"....self.user:{user}, username:{username}")
                            if user is None:
                                    try:
                                        # User.objects.get(username__exact=username)
                                            user = User.objects.get(username__exact=username)
                                            res= user.check_password(password)
                                            print(f"....password:{password} , check: {res}")
                                            if not user.check_password(password):
                                                logger.info("if user is None: Incorrect password")
                                                return JsonResponse({"message":'Incorrect password'}, status = 200)
                                            if not user.is_active:
                                                logger.info("if user is None: This user is not active")
                                                return JsonResponse({"message":'This user is not active'}, status = 200) 
                                                
                                    except Exception as e:
                                        logger.warning(f"if user is None:: {e}, {type(e)}")
                                        return JsonResponse({"message":'This user does not exist'}, status = 200) 

                    else:
                         logger.info("Sorry. We are unable to indentify this username")
                         return JsonResponse({"message":'Sorry. We are unable to indentify this username'}, status = 200) 
                 


                   # password = request.GET.get("password", "").strip()
                    #x = check_user(customer_id,password)
                    #print(f"---get_user:{x}")
                    
           
           
           
                

            member_info = {"member_id":member_qs.member_id.upper(),"name":member_qs.name,"id": member_qs.id}
            print(f"member_info:{member_info}")
            #cm_balance = get_running_finance_balance("cc","member_id",member_qs.id)["running_balance"]
            balances =get_all_balances(member_qs.id)
            return JsonResponse({"data":"Success","member_info":member_info,"balances":balances}, status = 200)
      except Exception as e:
            print (f"get customer detail error: {e}, {type(e)}")
            logger.warning(f"{e}, {type(e)}")
            return JsonResponse({"message":message}, status = 200)    
    return JsonResponse({}, status = 400)

 
      #return render(request, "/templates/fx/messages/pagenotfound.html", context) 
# def handler_404(request, exception):
#    return page_not_found(request, exception, template_name="404.html")
def get_member_info(id,code):
     print("--- at get_member_info")
     member_info = ""
     try:
            member_info =  MemberModel.objects.get(id = id) 
             
             
            print(f"..member_info:{member_info}")
            if member_info != "":
                    return member_info
          
     except Exception as e:
            #return render(request, '404.html', status=404)
            #return HttpResponseNotFound("Page not found....")
           # messages.error("", f"Message: Sorry. This record  can't be deleted this time.")

            raise Http404("Sorry. User id does not exist!")
            print(f"code:{code}, @exception, id: None , e:{e}")
             
           # return redirect(f'unsuccess/page_not_found/{message}/')

def cc_manager_create(source_id,description,transaction_type,debit,credit,member,category,date_enterd,source_fund,code):
        model_name =  source_funds_cc.get(source_fund)
        Model = apps.get_model('fx', model_name)
        try:
                #create_update_cc("CREATE",amount,customer_id,0,"GROCERY")
            create_cc_qs = Model(source_id=source_id,description = description ,transaction_type =transaction_type, debit =debit,credit =credit,member_id =member,category = category,date_entered = date.today())
            create_cc_qs.save() 
            id=create_cc_qs.id
            print(f"code:{code}, id:{id}")
            return id
        except Exception as e:
            print(f"code:{code},@ exception, id: None , e:{e}")
            
            return -1
def cc_manager_delete(source_id,source_fund,code):
        model_name =  source_funds_cc.get(source_fund)
        Model = apps.get_model('fx', model_name)
        try:
                deleteModel=Model.objects.get(id = source_id).delete()
                return True
        except Exception as e:
                print(f"code:{code},@ exception, Success:False, e:{e}")
                return False
def cc_manager_update(source_id,debit,credit,source_fund,code):
        model_name =  source_funds_cc.get(source_fund)
        Model = apps.get_model('fx', model_name)
        try:
                update_cc_qs = Model.objects.filter(id = source_id).update(debit = debit,credit =credit)
                if update_cc_qs <=0:
                    print(f"code:{code}, Success:False")
                    return False
                else:
                    print(f"code:{code}, Success:True")
                    return True
        except Exception as e:
                print(f"code:{code},@ exception, Success:False ,e:{e}")
                return -1
 
def delete_model_object(id,object_model,code):
    Model = apps.get_model('fx', object_model)
    try:
            Model.objects.get(id = id).delete()
            print(f"code:{code} Successs:True")
            return True
    except Exception as e:
            print(f"code:{code} Successs:False, e:{e}")
            return  False

def delete_venture(request,member_id,venture_id,request_action ):
    request_action =request_action.strip().lower()
    model_name =model_list.get(request_action) 
    Model = apps.get_model('fx', model_name)
    venture_qs = Model.objects.get(id = venture_id )
    customer_info = get_member_info(venture_qs.customer_id,"#delete venture. 0") #delete venture. 0
    Success = True
    if  request_action == "venture":
            customer_source_fund = SOURCE_REGULAR
            seller_dest_fund =SOURCE_VENTURE
    elif request_action == "trade":
            customer_source_fund = SOURCE_REGULAR
            seller_dest_fund =SOURCE_REGULAR
             
# Physical Money
    if venture_qs.source_type == "W":                        #delete_venture 1
            Success = account_manager_delete(venture_qs.customer_source_id,customer_source_fund,"#delete_venture 1")
            if Success == False:
               logger.warning(f">>> Unable to delete pthysical money payment of member_id: {member_id}, venture_id :{venture_id}, customer_source_fund:{customer_source_fund}")
    print(f"=================success 1: {Success}")
           
# Virtual Money  
    if Success and venture_qs.customer_cc_id:                    #delete_venture 3
                    Success = cc_manager_delete(venture_qs.customer_cc_id,customer_source_fund ,"#delete_venture 3") 
                    if Success == False:
                        logger.warning(f"Unable to delete cc payment of member_id: {member_id}, venture_id :{venture_id}")
    print(f"=================success 2: {Success}")
                   
# notes:    
    if Success:
        note_id = venture_qs.note_id
        if note_id > 0:
                response= create_or_update_venture_note(note_id,"",2)
    if Success:                                                  #middle-delete_venture(def)
              Success = delete_model_object(venture_id,model_name,"middle-delete_venture(def)")
         
    if Success:
            messages.success(request, f"Message: {customer_info.name}'s payment  has been successfully deleted.")
            return redirect(f'/pos/{member_id}/{0}/')
    else:
            member_info = get_member_info(member_id,"#delete_venture @else. 1") #delete_venture @else. 1
            if  request_action == "venture":
                  ventureForm = VentureForm( instance=venture_qs) # instance=saving bcoz editing process, none when new record
            else:
                  ventureForm = TradeForm( instance=venture_qs)
            #customer = venture_qs.customer_id
            ventureForm.request_action = request_action
            ventureForm.id= venture_qs.id
            ventureForm.totalCost = venture_qs.amount + venture_qs.cc

            asset_balance={}
            cc_balance = get_running_finance_balance("cc","member_id",venture_qs.customer_id)["running_balance"]
            if maximum_deposit < cc_balance: 
                cc_balance = maximum_deposit
            asset_balance ={"cc_balance":cc_balance}
            context = {
                    'post_data':True,
                    'asset_balance':asset_balance,
                    'venture': ventureForm,  
                    'limits':limits,
                    'member_info':member_info,
                    'customer_info':customer_info,
                    }
            messages.error(request, f"Message: Sorry. This record  can't be deleted this time.")
            return render(request, 'fx/venture/pos.html', context)
def account_manager_delete(source_id,sourceFund,code):
            model_name =source_funds_pm.get(sourceFund) 
            Model = apps.get_model('fx', model_name)
            try:
                    delete_wallet_res = Model.objects.get(id = source_id).delete()  #todo id = source_id
                    print(f"code:{code}, Success:True")
                    return True
            except Exception as e:
                    print(f"code:{code}, @Exception, Success:False") 
                    print(f"..account manager delete_wallet_res: {e}")
                    return False
            return True
def account_manager_create(customer,sourceFund,source_id,description,category,transaction_type,date_entered,debit,credit,code):
     #  return_id = account_manager_create(customer, venture_id,"Grocery",2,'W', date.today(),amount,0)
            model_name =source_funds_pm.get(sourceFund) 
            Model = apps.get_model('fx', model_name)
            try:
                create_wallet_qs = Model(member_id = customer,source_id =source_id, description=description,category = category, transaction_type=transaction_type,date_entered =date_entered,debit =debit,credit =credit) #todo id = source_id
                create_wallet_qs.save()
                id = create_wallet_qs.id
                print(f"code:{code}, id:{id}")
                return create_wallet_qs.id
            except Exception as e:
                    print(f"code:{code},@Exception id:None")
                    print(f"..account manager create_wallet_qs: {e}")
                    return -1

def account_manager_update(source_id,debit,credit,sourceFund,code):
            try:
                model_name =source_funds_pm.get(sourceFund) 
                Model = apps.get_model('fx', model_name)
                update_wallet_result = Model.objects.filter(id = source_id).update( debit = debit,credit =credit)
                
                if update_wallet_result > 0:
                    print(f"code:{code}, Success:True")
                    return True
                else:
                    print(f"code:{code}, Success:False")
                    return False
            except Exception as e:
                    print(f"code:{code}, @Exception Success:False")
                    print(f"..account manager update_wallet_result: {e}")
                    return False


#333
def create_or_update_venture_note(code, source_id,note,category=2):
        #-1 : no-action, 0:edit,1: create
        print(f"--------- code: {code},source_id:{source_id}, category: {category},note: {note}")
        if code == DELETE_RECORD:
                try:
                    delete_note_qs = NoteModel.objects.get(id = source_id ).delete()
                    print("delete create_or_update_venture_note")
                    return {"Success":True, 'result': delete_note_qs}
                except Exception as e:
                    logger.warning("unable to delete note at Def create_or_update_venture_note ")
                    return {"Success":False}

        else:
            if code == EDIT_RECORD and source_id > 0:    
                try:  
                    result = NoteModel.objects.filter(id = source_id).update(note=note)
                    print("-- success editing note at create_or_update_venture_note")
                    return {"Success":True,"result": result}
                except Exception as e:
                    print (f"result notes {e}, {type(e)}")
                    logger.warning(f"result notes {e}, {type(e)} at Def create_or_update_venture_note ")
                    return {"Success":False}
            else:  
                
                print("-- success adding note at create_or_update_venture_note")       
                try:
                    note_qs = NoteModel(source_id = source_id ,category=category ,note = note  )
                    note_qs.save() 
                    return {"Success":True,"result": note_qs.id} 
                except Exception as e:
                    logger.warning(f"Unable to save notes at Def create_or_update_venture_note ")
                    print (f"result notes {e}, {type(e)}")
                    return {"Success":False}

def create_update_venture_result(request,member_id,venture_id,msg,request_action):

        
        model_name = model_list.get(request_action) 
        Model = apps.get_model('fx', model_name)
        member_info = get_member_info(member_id,"#create_update_venture_result. 1") #create_update_venture_result. 1
        venture_qs= get_object_or_404(Model, id=venture_id)
        if request_action == "trade":
            ventureForm = TradeForm( instance=venture_qs)
            if venture_qs.role_type == "S": #B-buyer, default
                  customer = venture_qs.seller_id
            else:
                  customer = venture_qs.customer_id
        else:
             ventureForm = VentureForm( instance=venture_qs)
             customer = venture_qs.customer_id
        customer_info = get_member_info(customer,"#create_update_venture_result. 2") #create_update_venture_result. 2
        print(f"member_id:{customer_info.member_id}, firstname:{customer_info.firstname}")
        
        
        ventureForm.request_action = request_action
        ventureForm.id= venture_qs.id
        ventureForm.totalCost = venture_qs.total_cost #venture_qs.amount + venture_qs.cc
        
        if venture_qs.note_id > 0: #note has been provided
                    try:
                        ventureForm.note = NoteModel.objects.get(id=venture_qs.note_id).note #todo: handler
                    except Exception as e:
                        print(f"loan app note: {e}")
        else:     
                        ventureForm.note =""
        print(f"====venture_qs.note_id: {venture_qs.note_id},, ventureForm.note: {ventureForm.note}  ")
        
        # get change intry
        ventureForm.change_destination =""
        try:
             change_table_qs = Change_Table.objects.get(venture_id= venture_id)
             ventureForm.change = change_table_qs.change
             ventureForm.tender =  venture_qs.amount + change_table_qs.change
             ventureForm.destination_acct_code =change_table_qs.destination_acct_code
             
             print(f"ventureForm.tender:{ventureForm.tender}")
        except Exception as e:
                ventureForm.change =""
                ventureForm.tender =""
                ventureForm.destination_acct_code=""
                print(f"create_update_venture_result:change_table: {e}")
        
                

        context = { 
                'post_data':True,
                   #id = member_id
                'venture': ventureForm,   
                'member_info':member_info,
                'customer_info':customer_info,
            }
         
        messages.success(request, msg)
        return render(request, 'fx/venture/pos.html', context)

 # date_time_str = '19/09/01 01:55:19'
    # date_time_obj = datetime.strptime(date_time_str, '%y/%m/%d %H:%M:%S')

    # print ("The type of the date is now",  type(date_time_obj))
    # print ("The date is", date_time_obj)
    # bod = date.today()


    # gender_list={"M":"1","F":"0"}
    # gender ="F"
    # firstname ="dandy".upper().strip()
    # part1= firstname[0:2]
    # bod = date.today()
    # part2 = bod.strftime("%m%d")

    

    # customer_id = part1 + part2 + "-" + gender_list.get(gender)
    # try:
    #     idRepository_qs = IdRepositoryModel.objects.get(code = customer_id)
    #     counter = idRepository_qs.counter + 1
    #     idRepository_qs.counter =F('counter')+1
    #     idRepository_qs.save()
            
    # except  IdRepositoryModel.DoesNotExist:
    #     idRepository_res =  IdRepositoryModel(code = customer_id,counter =1 )
    #     idRepository_res.save()
    #     counter = 1

    # customer_id =customer_id + f"{counter}"
    # print(f".......part1: {part1}{ bod} part2: {part2}")
    # print(f"customer_id: {customer_id}")

    # return



#todo. cuv
def add_change_transaction(code, wallet_id,venture_id,amount):
    print(f"add_change_transaction: wallet_id:{wallet_id}, venture_id:{venture_id}, amount:{amount}")
    if code == 0:
            try:  
                    change = Change_Table(wallet_id = wallet_id, date_entered=date.today(),venture_id=venture_id ,tender=amount )
                    change.save() 
                    return {"Success":True,"id":change.id}
                    
            except Exception as e:
                    
                    print (f"add_change_transaction:error result:{e}, {type(e)}")
                    return {"Success":False}
    else:
        
        if amount == 0:
            #
            try:  

                    change = Change_Table.objects.get(venture_id=venture_id  )
                    wallet_id = change.wallet_id
                    print(f"amount == 0,wallet_id:{wallet_id}") 
                    delete_change = Change_Table.objects.get(venture_id = venture_id).delete()
                    try:
                           delete_wallet_change = WalletModel.objects.get(id = wallet_id).delete() 
                    except Exception as e:
                           print (f"add_change_transaction:delete change fr. wallet:{e}, {type(e)}")
                      
                    
            except Exception as e:
                    
                    print (f"add_change_transaction:delete change:{e}, {type(e)}")
                    return {"Success":False}
             
        print("code > 0")
        pass
    

def add_regular_transaction(code, target_table ,member,description ="Change Deposit",transaction_type="D",credit=0,debit=0,source_id=0,category = 0):
            #code : 0 -new, 1 -edit
            #credit - change_amount
            print(f"-------------------add_regular_transaction ------------- code: {code}, credit:{credit}, venture_id:{source_id}, target_table:{target_table},change_amount: {credit}")
            if code > 0: # edit existing record
                    old_destination_acct_code =""
                    try:    
                        change = Change_Table.objects.get(venture_id=source_id)
                        destination_acct_id = change.destination_acct_id
                        old_destination_acct_code = change.destination_acct_code
                        old_amount = change.change
                        print(f"old_destination_acct_code:{old_destination_acct_code}, change:{old_amount}")
                    except Exception as e:
                                print (f"add_regular_transaction:not found,code > 0:{e}, {type(e)}")
                                if credit <=0:
                                        return {"Success":False}
                                else:
                                    code = 0
                    
                    if credit <=0 and code > 0:
                            if old_destination_acct_code == "W":
                                target_table = "WALLET ACCT"
                            elif old_destination_acct_code == "S":
                                target_table = "SAVING ACCT"
                            print(f"xtarget_table:{target_table}")
            else: # new record
                    code = 0
           
            #update_wallet_result = Model.objects.filter(id = source_id).update( debit = debit,credit =credit)
            # if code > 0:
            #         try:
                        
            #             change = Change_Table.objects.get(venture_id=source_id)
            #             destination_acct_id = change.destination_acct_id
            #         except Exception as e:
            #                 print (f"add_regular_transaction:not found:{e}, {type(e)}")
            #                 code = 0
            print(">>")
            destination_acct_code = ""
            if target_table == "WALLET ACCT":
                          destination_acct_code ="W"
            elif target_table == "SAVING ACCT":
                          destination_acct_code ="S"    
            else:
                  target_table =""      
                  print("target_table is empty---------------")
            print(">>>")     
            if target_table != "":
                    model_name = model_list_change.get(target_table) 
                    Model = apps.get_model('fx', model_name)
                    
                  
             
            print(">>>>")                         
            if code > 0:  # edit existing record
                    
                    # change = Change_Table.objects.get(venture_id=source_id)
                    # destination_acct_id = change.destination_acct_id
                    # old_destination_acct_code = change.destination_acct_code
                    print(f" old_destination_acct_code:{old_destination_acct_code} = change.destination_acct_code:{destination_acct_code}")
                     
                    if credit > 0 and destination_acct_code != old_destination_acct_code:
                                print("------ credit > 0 and destination_acct_code != old_destination_acct_code:passed")
                                try: 
                                        if  old_destination_acct_code == "W":
                                            delete_walletModel = WalletModel.objects.get(id = destination_acct_id).delete() 
                                        elif old_destination_acct_code == "S":
                                            delete_savingModel = SavingModel.objects.get(id = destination_acct_id).delete() 
                                        print("---dldldl")
                                except Exception as e:
                                            print (f"destination_acct != old_destination_acct:delete rec:{e}, {type(e)}")
                                            return {"Success":False}
                                try: 
                                        id =0
                                        if target_table !="":
                                            destination_model = Model(member_id = member, date_entered=date.today(),transaction_type=transaction_type ,description=description,debit=0,credit=credit,source_id =source_id ,category =category )
                                            destination_model.save() 
                                            id = destination_model.id
                                        filter_fields = {"destination_acct_code": destination_acct_code,"destination_acct_id": id}
                                        if old_amount != credit:
                                            filter_fields["change"]= credit
                                        change_deposit = Change_Table.objects.filter(venture_id = source_id).update( **filter_fields)
                                        return {"Success":True}
                                except Exception as e:
                                            print (f"destination_acct != old_destination_acct:adding rec: {e}, {type(e)}")
                                            return {"Success":False}
                    
                    print(f"source_id{source_id}, wallet_id:{destination_acct_id}, venture_id:{source_id}, credit:{credit}")
                    if credit > 0:
                                print(f"-------if credit > 0: add_regular_transaction:code > 0,destination_acct_id:{destination_acct_id},credit:{credit}") 
                                     
                                try:
                                        print(f"---- try : target_table:{target_table}")
                                        if  target_table != "": 
                                                 destination = Model.objects.filter(id = destination_acct_id).update( credit = credit)
                                        wallet_change_deposit = Change_Table.objects.filter(venture_id = source_id).update( change = credit)
                                        return {"Success":True}
                                except Exception as e:
                                        print (f"add_regular_transaction:update change:  credit > :{e}, {type(e)}")
                                        return {"Success":False}
                                            
                    else:
                                print(" else of credit > 0: add_regular_transaction*************************************************ERROR")
                                print(f"model_name:")
                                try:
                                        try:
                                                print(f"model_name:{model_name}, destination_acct_id:{destination_acct_id}")
                                                delete_wallet_change = Model.objects.get(id = destination_acct_id).delete() 
                                                print("deleting.........")
                                        except Exception as e:
                                               print("add_regular_transaction*************************************************ERROR in except")
                                              
                                        delete_change = Change_Table.objects.get(venture_id = source_id).delete()
                                        print("deleting wallet change")
                                        return {"Success":True}
                                except Exception as e:
                                        print (f"add_regular_transaction:delete wallet and change tables:else credit >  0:{e}, {type(e)}")
                                        return {"Success":False}

                        
                    
                    
            else: # of code > 0:
                    wallet_id =0
                    if target_table != "":
                                try:
                                        wallet = Model(member_id = member, date_entered=date.today(),transaction_type=transaction_type ,description=description,debit=0,credit=credit,source_id =source_id ,category =category )
                                        wallet.save() 
                                        wallet_id = wallet.id
                                        print("success saving change to the selected account")
                                except Exception as e:
                                            print (f"writing to selected account:{e}, {type(e)}")
                                            logger.warning(f"error writing an amount of {credit}  to selected account:{e}, {type(e)}")
                                            #return {"Success":False}
                    
                    try:    
                            change = Change_Table(destination_acct_id = wallet_id, date_entered=date.today(),venture_id=source_id ,change=credit,destination_acct_code = destination_acct_code)
                            change.save() 
                            
                            return {"Success":True,"id":change.id}
                    
                    except Exception as e:
                            print (f"add_change_transaction:add new rec at Change_table:{e}, {type(e)}")
                            return {"Success":False}
                    
                    return {"Success":True,"id":wallet.id}
    


 #    saveTransHistory(request.user.id,member_id,TRANS_VENTURE,venture_id,description, amount,NEW_RECORD) # new entry
#.,
def saveTransHistory(account_code,user_id,member_id,category,source_id,data,code):
    print(f"data: {data},code ={code},source id :{source_id},account_code:{account_code}") #data or amount
    id =0
    try:
            id =  MemberModel.objects.get(user_id  = user_id).id
            print(f"..id:{id}")
    except Exception as e:
           # raise Http404("Sorry. User id does not exist!")
            print(f"def cuv @exception, id: None , e:{e}")
            logger.warning(f"def cuv @exception,e:{e}" ) 
    if code == NEW_RECORD:
            print("------------writing on saveHistory")
            try:
                    daytransactionmodel_qs = dayTransactionModel(account_code =account_code,in_charge_id = id,customer_id = member_id,category =category, amount = data,source_id = source_id,date_entered =date.today())
                    daytransactionmodel_qs.save()
                    #venture_id =venture_qs.id
            except Exception as e:
                print(f"creating new record on saveTransHistory: {e}")
    elif code == EDIT_RECORD:
            try:
                print("success eedting on savetrans")
                account_qs = dayTransactionModel.objects.filter (source_id = source_id , account_code = account_code) .update( **data)
                print("success eedting on savetrans")
            except Exception as e:
                Success = False
                print(f"updating new record on saveTransHistory: {e}")
    
    
    elif code == DELETE_RECORD:
        pass
    

def getLoanPayment(member_id):
    try:    
        loan_qs = LoanSummaryModel.objects.get(member_id=member_id)
        max_loan = loan_qs.max_loan
        percent = loan_qs.percent
    except Exception as e:
        print (f"retrieving LoanSummaryModel:{e}, {type(e)}")
        return {}
    return {"max_loan":max_loan,"percent":percent}




def po(request):
    
    context ={}
                   
        
    return render(request, 'fx/venture/venture_pos.html', context)
    
     
def get_pos(request):
    if request.is_ajax and request.method == "GET"  and request.user.is_authenticated is True:  
            member = true
            venture_id = request.POST.get('venture_id',"0").strip()
            if venture_id > 0:
                    if venture_id > 0: #edit
                        try:
                           venture_qs= VentureModel.objects.et( id=venture_id)
                           
                        except Exception as e:
                            print ("unable to retrieve transaction number")
                            logger.warning ("unable to retrieve transaction number")
                             
                    customer_id = 0
                    asset_balance={}
                    print(f"venture_id:{venture_id}")
                    

           # if venture_id > 0:
            cc_balance = get_running_finance_balance("cc","member_id",venture_qs.customer_id)["running_balance"]
            if maximum_deposit < cc_balance: 
                cc_balance = maximum_deposit
            asset_balance ={"cc_balance":cc_balance}
                        
            customer_info = get_member_info( venture_qs.customer_id,"#create_update_venture. 1") #create_update_venture. 1
            ventureForm.totalCost = venture_qs.amount + venture_qs.cc
           # ventureForm.request_action =request_action
            if member:
                    asset_balance["cc_balance"] = asset_balance["cc_balance"] + venture_qs.cc
            #print(f"........asset_balance['cc_balance'] {asset_balance['cc_balance']} ,") 
            if venture_qs.note_id > 0: #note has been provided
                    try:
                            ventureForm.note = NoteModel.objects.get(id=venture_qs.note_id).note #todo: handler
                    except Exception as e:
                        print(f"loan app note: {e}")
            else: 
                    ventureForm.note =""
            try:
                        change_table_qs = Change_Table.objects.get(venture_id= venture_id)
                        ventureForm.change = change_table_qs.change
                        ventureForm.tender =  venture_qs.amount + change_table_qs.change
                        ventureForm.destination_acct_code =change_table_qs.destination_acct_code
                        print(f"venture form: {ventureForm}")
                        print(f"ventureForm.tender:{ventureForm.tender},change_table_qs.change:{change_table_qs.change},change_table_qs.destination_acct_code:{change_table_qs.destination_acct_code} ")
                        return JsonResponse({"type":'success', "message":"Success","data":ventureForm})
            except Exception as e:
                    ventureForm.change =""
                    ventureForm.tender =""
                    print(f"cresate_update_venture:change_table: {e}")     
                    logger.warning(f" Technical error in def get pos: {e} ")
                    return JsonResponse({"type":'error', "message":"Technical error","data":{}})
                           
                        
                        
    else:
                        return JsonResponse({"type":'error', "message":"Invalid Transaction Request!","data":{}})
                    
                    
                    
                    
                    
class new_note_view(View):
    def post(self, request, *args, **kwargs):
         
                 
                if request.user.is_staff and request.user.is_active:
                            print (f"user: {request.user}")
                            staff_info = ""
                            try:
                                staff_info =  MemberModel.objects.get(user_id  = request.user.id) 
                                print(f"..staff_info:{staff_info.name}")
                            except Exception as e:
                            # raise Http404("Sorry. User id does not exist!")
                                print(f"def cuv @exception, id: None , e:{e}")
                                logger.warning(f"def cuv @exception,e:{e}" ) 
                else:
                                print("going to unauthorized user page")  
                                return redirect('/venture_login/') #
                            # return redirect('/unauthorized_user/') #
               
                
                
                customer = parseint(  request.POST.get('customer','0').strip())
                code =  request.POST.get('code','').strip().upper()
                id = parseint(  request.POST.get('id','0').strip())
                print(f"------Post--------L idL {id}")
                 
                
                note =   request.POST.get('note','').strip()
                if customer =="test":
                     return JsonResponse({"type":'success', "message":"Completed!","data":{}})
                
                
                print(f"customer: {customer}, note: {note}")
                if note=="":
                       try:
                            customerNoteModel_qs = CustomerNoteModel.objects.get(id = id).delete()  #todo id = source_id
                            print(f"code:{code}, Success:True")
                            return JsonResponse({"type":'success',"code":0, "message":"Note has been successfully deleted","data":{}})
                       except Exception as e:
                            print(f"Delete customer note: {e}")
                            return JsonResponse({"type":'error', "message":"Unable to delete record!","data":{}})
                      
                    
                if code == "SAVE NOTE":
                        try:
                                note_qs = CustomerNoteModel(note = note,member_id = customer)
                                note_qs.save() 
                                return JsonResponse({"type":'success', "code":1, "message":"Note has been succesfully added!","data":{"id":note_qs.id}})
                        except Exception as e:
                            print(f"Adding new note error: {e}")
                            return JsonResponse({"type":'error', "message":"Unable to save!","data":{}})
                else:
                        try:
                                #   venture_result = Model.objects.filter(id = venture_id).update( **filter_fields)
                                print(f"id = :{id}")
                                note_qs = CustomerNoteModel.objects.filter(id = id ).update(note=note)
                                #note_qs.save() 
                                return JsonResponse({"type":'success',"code":2, "message":"Note has been succesfully changed!"})
                        except Exception as e:
                            print(f"Editing  note error: {e}")
                            return JsonResponse({"type":'error', "message":"Unable to edit data!","data":{}})
                    
                       
                
                
                
                    
             
# @login_required(login_url='/venture_login/')
#pos
class pos_view(View):
    
    def get(self, request, *args, **kwargs):
        print("---get")
        if  request.user.is_authenticated is True:  
                member = True
                venture_id = parseint(request.GET.get('venture_id',"0").strip())
                print(f"Vent:{venture_id}")
               
                if venture_id > 0:
                        print(f"customer id.. {venture_id}")
                     
                        try: 
                                venture_qs= VentureModel.objects.get( id=venture_id)
                        except Exception as e:
                            print ("unable to retrieve transaction number")
                            logger.warning ("unable to retrieve transaction number")
                                
                         
                        asset_balance={}
                        
                        print(f"venture_id:{venture_id},amount: {venture_qs.amount}")
                        try:
                                 member_qs = MemberModel.objects.get(id=venture_qs.customer_id) 
                        except Exception as e:
                                 print(f"pos error: {e}")
                                 logger.warning(f" at pos: {e}")
                        
            # if venture_id > 0:
                cc_balance = get_running_finance_balance("cc","member_id",venture_qs.customer_id)["running_balance"]
               
                if maximum_deposit < cc_balance: 
                    cc_balance = maximum_deposit
                asset_balance ={"cc_balance":cc_balance}
                print("XXXX")          
                customer_info = get_member_info( venture_qs.customer_id,"#create_update_venture. 1") #create_update_venture. 1
                print(f"customer name: {customer_info.name}")
                totalCost = venture_qs.amount + venture_qs.cc
            # ventureForm.request_action =request_action
                if member:
                        asset_balance["cc_balance"] = asset_balance["cc_balance"] + venture_qs.cc
                print(f"........asset_balance['cc_balance'] {asset_balance['cc_balance']} ,") 
                if venture_qs.note_id > 0: #note has been provided
                        try:
                                desc = NoteModel.objects.get(id=venture_qs.note_id).note #todo: handler
                              
                        except Exception as e:
                            print(f"Pos description: {e}")
                            logger.warning(f"Pos description: {e}")
                            desc = ""
                else: 
                        desc =""
               
                try:
                            change_table_qs = Change_Table.objects.get(venture_id= venture_id)
                            print("first")
                            change = change_table_qs.change
                           # change =  venture_qs.amount + change_table_qs.change
                            destination_acct_code =change_table_qs.destination_acct_code
                            print("Try")
                             #print(f"venture form: {ventureForm}")
                           # data={"totalCost":totalCost,"change":change,"tender":tender,"destination_acct_code":destination_acct_code}

                            print(f"----change_table_qs.change:{change_table_qs.change},change_table_qs.destination_acct_code:{change_table_qs.destination_acct_code} ")
                          #  return JsonResponse({"type":'success', "message":"Success","data":data})
                except Exception as e:
                        change =0
                        tendered =0
                        destination_acct_code=""
                        print(f"cresate_update_venture:change_table: {e}")     
                        logger.warning(f" Technical error in def get pos: {e} ")
                        print("XXX")
                        #return JsonResponse({"type":'error', "message":"Technical error","data":{}})
                print(f" member qs: {member_qs}")
                member_info = {"member_id":member_qs.member_id.upper(),"name":member_qs.name,"id": member_qs.id}
                print("X")
                print(f"member_info:{member_info}")
                #cm_balance = get_running_finance_balance("cc","member_id",member_qs.id)["running_balance"]
                balances =get_all_balances(member_qs.id)
                print(f"balances: {balances}")
               # return JsonResponse({"data":"Success","member_info":member_info,"balances":balances}, status = 200)
                data={"venture_id":venture_id,"source_type":venture_qs.source_type,"percent": venture_qs.percent,"amount":venture_qs.amount,"cc":venture_qs.cc,"change":change,"destination_acct_code":destination_acct_code,"desc":desc}
                print(f"--- source type: {venture_qs.source_type}")
                
#                  items = ProductModel.objects.all()
#    # item_list = serializers.serialize('json', items)
#  #  return HttpResponse(item_list, content_type="text/json-comment-filtered")
#     data = list(items.values())
#     # data = [{'label': 'Peter', 'email': 'peter@example.org'},
#     #         {'label': 'Julia', 'email': 'julia@example.org'}]
#     return JsonResponse({"data":data})


                notes= []
            
                try:
                    notes_qs = CustomerNoteModel.objects.filter(date_entered__lte=datetime.today(), date_entered__gt=datetime.today()-timedelta(days=30),   member_id =member_qs.id).order_by("pk")[:100]
                    
                    for row in notes_qs:
                        row ={"id":row.id,"note":row.note,"date_entered":row.date_entered}
                        notes.append(row)
                except Exception as e:
                    print(f"Retrieving customer note error: {e}")
                ps = []
                try:
                        productSold = ProductSold.objects.filter(transaction_id=venture_id) #todo: handler
                        
                        for row in productSold:
                                row ={"description":row.description,"qty":row.qty,"price":row.price,"cm":row.cm,"amount":row.amount,"item_id":row.item_id }
                                ps.append(row)
                                       #   itemsold= ProductSold (member_id = customer,qty=obj["qty"],cm=obj["cm"],amount=obj["amount"],item_id=obj["item_id"],description=obj["description"],transaction_id=obj["transaction_id"])
 
                except Exception as e:
                    
                            print(f"Pos description: {e}")
                            logger.warning(f"Pos description: {e}")
                
                return JsonResponse({"type":'success', "message":"Success","data":data,"member_info":member_info,"balances":balances,"ps":ps,"notes":notes})
            
                        
        else:
                        print("here------------------------------- ")
                        return JsonResponse({"type":'error', "message":"Invalid Transaction Request!","data":{}})
    def post(self, request, *args, **kwargs):
         
                member = True
                if request.user.is_staff and request.user.is_active:
                            print (f"user: {request.user}")
                            staff_info=""
                            try:
                                staff_info =  MemberModel.objects.get(user_id  = request.user.id) 
                                print(f"..staff_info:{staff_info.name}")
                            except Exception as e:
                            # raise Http404("Sorry. User id does not exist!")
                                print(f"def cuv @exception, id: None , e:{e}")
                                logger.warning(f"def cuv @exception,e:{e}" ) 
                else:
                                print("going to unauthorized user page")  
                                return redirect('/venture_login/') #
                            # return redirect('/unauthorized_user/') #
               
                
                print(f"------Post--------")
                customer =   request.POST.get('customer','0').strip()
                if customer =="test":
                     return JsonResponse({"type":'success', "message":"Completed!","data":{}})
                    
                
                customer = parseint( customer)
                
                source_type = request.POST.get('source_type',"").strip()
                amount =float(request.POST.get('amount',"0").strip())
                cc = float(request.POST.get('cc','0').strip())
                credit_line = float(request.POST.get('credit_line','0').strip())
                note = request.POST.get('note',"").strip()
                
                print(f" type cust: {type(customer)}")
                 
                venture_id = parseint( request.POST.get('venture_id',"0").strip())
                change_deposit_to  = request.POST.get("change_deposit_to","").strip()
                
                change_amount  = request.POST.get("change","0").strip()
                
                if change_amount == "":
                        change_amount =0
                else:
                        change_amount =float(change_amount)
                #----------------b
                print(f"---source_type: {source_type} amount: {amount}, cc: {cc}, note: {note}, customer: {customer}, venture_id:{venture_id}, change_deposit_to: {change_deposit_to}")
                print (f"--- user: {request.user}")
                #-----------------e
                
                ##request_action =request_action.strip().lower()
                ##model_name =model_list.get(request_action) 
                Model = apps.get_model('fx', "VentureModel")
                all_valid = True 
                default_percentage = 95  #
                member_id = customer
                member_info= {}
                print("1---------------1")
                # if member_id > 0:
                #        print("====")
                #        member_info = get_member_info( member_id,"#create_update_venture. 1")  #create_update_venture. 1
                print("2---------------")
                message= ""
                category = CAT_VENTURE
                description ="GROCERY"
                customer_source_fund = SOURCE_REGULAR
                seller_dest_fund =SOURCE_VENTURE
                
              # print(f"--- member_info: {member_info}")
                
                 
                
            ## ??
              
                print(f"type venture_id: {type(venture_id)}")
                if venture_id > 0:
                    print(">>>>>>>>>>>>>>>")
                    venture_qs= Model.objects.get(id=venture_id)
                 
              #  print(f"venture: {venture_qs}")
                customer_id = 0
                asset_balance={}
               # customer_info = get_member_info(cust,"#request.method == 'POST'. 1") #request.method == 'POST'. 1
                print(f"--------------")
                 
                if venture_id > 0:
                            try:
                                 old_venture_qs =  VentureModel.objects.get(id=venture_id)
                            except Exception as e:
                                print("Error: venture > 0 at POST: {e}")
                                logger.warning("Error: venture > 0 at POST: {e}")
                                
                            if  old_venture_qs.source_type =="W": #1
                                    old_amount = old_venture_qs.amount
                            else:
                                 old_amount =0
                            old_source_type = old_venture_qs.source_type
                            old_cc = old_venture_qs.cc
                            old_customer_cc_id = old_venture_qs.customer_cc_id
                            old_customer_id =  old_venture_qs.customer_id
                            old_note_id = old_venture_qs.note_id
                            print(f"old_venture_qs: {old_venture_qs}")
                            
                            #+
                            # if request_action == "trade":
                            #     old_role_type=  old_venture_qs.role_type
                            # else:
                            #     old_role_type =""

                            if old_note_id > 0:
                                    try:
                                        old_note = NoteModel.objects.get(id = old_note_id ).note
                                    except Exception as e:
                                        print(f"getting note: {e}")
                            else:
                                    old_note = ""
                            
                else:
                            old_amount = 0 
                            old_customer_id = customer
                            old_cc = 0
                
              
                if member:
                        cc_running_balance = get_running_finance_balance("cc","member_id",customer)["running_balance"]
                print("Community account side")
                if credit_line > 0 and  member and  int(cc) > cc_running_balance + old_cc:
                            all_valid = False
                            if cc_running_balance + old_cc <=0: ##?? y 2000
                                     message= "Sorry. Community Money Account  is empty!"
                            else:
                                     message= f"Please enter a number that is no more than {cc_running_balance+ old_cc}"
                           
                print("wallet accout side")
                if member and source_type =="W":
                        running_balance = get_running_finance_balance("wallet","member_id",customer)["running_balance"]
                        print(f"runnin balance: {running_balance}, amount: {amount}, old_amount: {old_amount}")
                        if  int(amount) > running_balance + old_amount:
                                all_valid = False
                                if running_balance + old_amount <=0:
                                                message= "Sorry. Wallet Account is empty!"
                                                print(f"Message: Sorry. Wallet Account is empty!")
                                                logger.warning(f"Message: Sorry. Wallet Account is empty!")
                                              #  messages.error(request, f"Message: Sorry. Wallet Account is empty!")
                                    
                                else:
                                                running_balance ='{:,.2f}'.format(running_balance +old_amount)
                                                message= f"Please enter an amount that is no more than P{running_balance}"
                                                print(message)
                                                logger.warning(message)
                                               # messages.error(request, message)
                                print("..all_valid:",all_valid)
                else:
                         customer_source_id = 0
                print(f"--- cc_running_balance: {cc_running_balance}")
                if venture_id <=0:
                                    if all_valid:
                                        print(".....ventureForm is valid!")
                                        Success = True
                                        venture_id_change =venture_id
                                        venture_id = 0
                                        #----------------b
                                        #inside:[if venture_id <=0]
                                        print(f" amount: {amount}, cc: {cc}, note: {note}, customer: {customer}, venture_id:{venture_id}, change_deposit_to: {change_deposit_to}")
                                       # print(f"cateory: {cateory},transaction_type:{ transaction_type}, source_type: {source_type} percent: {percent}")
                                        print (f"writing to venture")
                                        #-----------------e
                                        try:
                                                venture_qs = Model(customer_id = customer,category =category,
                                                amount = amount,cc = cc,transaction_type ="W",date_entered = date.today(),
                                                source_type =source_type,in_charge_id=staff_info.id,flag=1)
                                                venture_qs.save()
                                                venture_id =venture_qs.id
                                                print(f"Success in writin to model, id: {venture_id}")
                                        except Exception as e:
                                            Success = False
                                            print(f"creating venture transaction: {e}")
                                        filter_fields = {} 
                                             
                                        if source_type =="W": #create new record. A
                                                customer_source_id = account_manager_create(customer,customer_source_fund, venture_id,description,category,'W', date.today(),amount,0,"#create new record. A")
                                                filter_fields["customer_source_id"] =customer_source_id
                                                if customer_source_id <=0:
                                                    Success = False
                                        
                                        if cc > 0: #create new record. C
                                                customer_cc_id = cc_manager_create(venture_id,description,"W",cc,0,customer,category,date.today(),customer_source_fund,"create new record. C")
                                                filter_fields["customer_cc_id"]= customer_cc_id
                                                if customer_cc_id <= 0:
                                                    Success = False
                                                print(f"cc recording success:Success {Success}")

                                        else:
                                            filter_fields["customer_cc_id"] =0
                                            try:
                                                    credit_limit_qs = CreditLineModel(amount =credit_line,member_id = customer)
                                                    credit_limit_qs.save() 
                                                    print(f"success :customer {customer},credit limit : {credit_line}")
                                            except Exception as e:
                                                    print(f"Unable to save to credit line  , e:{e}")
                                            
                                            
                                            
                                            #$
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                        note_id = 0
                                        response = {}    
                                        print(f"today filter_fields: {filter_fields} ")
#2121
                                        if note != "":
                                            response = create_or_update_venture_note(NEW_RECORD,venture_id,note,2) #todo 
                                            if response["Success"] and response["result"] > 0:
                                                note_id  = response["result"]
                                        else:
                                            note_id = 0  
                                        filter_fields["note_id"] = note_id
                                        
                                        
                                        if Success:
                                                Success = True
                                                try:
                                                    venture_result = Model.objects.filter(id = venture_id).update( **filter_fields)
                                                    print(f"venture: filter_fields: {filter_fields} ,venture_result: {venture_result}")
                                                    
                                                except Exception as e:
                                                        print (f"error result:{e}, {type(e)}")
                                                        Success = False
                                                #11-25
                                                if Success and change_amount > 0:
                                                        print(f"============ change amnt:{change_amount}")
                                                        response = add_regular_transaction(0,change_deposit_to,customer,"Change Deposit","D",change_amount,0,venture_id)
                                                        if response["Success"] :
                                                        #  response = add_change_transaction(venture_id_change, response["id"],venture_id,amount)
                                                               print("success................")
                                                else:
                                                    print(f"ELSE:  change_amount:{change_amount}")
                                                    
                                                if Success: #save day transaction for the cashier
                                                   # pass
                                                  # def saveTransHistory(account_code,user_id,member_id,category,source_id,data,code):
                                                  
                                                        if source_type =="W":
                                                              acct_code = ACCOUNT_WALLET
                                                        elif source_type =="S":
                                                              acct_code =ACCOUNT_SAVINGS
                                                        else: 
                                                              acct_code = NO_ACCOUNT
                                                        saveTransHistory(acct_code,request.user.id,member_id,category,venture_id,amount,NEW_RECORD)
                                                     #   saveTransHistory(request.user.id,member_id,TRANS_VENTURE,venture_id,description, amount,NEW_RECORD) # new entry
                                                        print("-----saveTransHistory updated")
                                                
                                                
                                                
                                                    
                                            # if Success and source_id > 0:
                                            #       wallet_qs = WalletModel.objects.filter( id = source_id).update(source_id = venture_id)
                                            # if Success and cc_create_result > 0:
                                            #    cc_qs = CcModel.objects.filter( id = cc_create_result).update(source_id = venture_id)
                                        else:
                                               print("Unable to complete the ventureModel update above") 
                                               logger.warnin("Unable to complete the ventureModel update above")       
                                        print(f"Success: {Success}")
                                        msg ="Customer Payment has been successfully recorded!"
                                        print("returnin...")
                                        
                                        #here
                                        data ={"venture_id":venture_id,"amount":venture_qs.amount,'cc':venture_qs.cc,"source":venture_qs.source_type}
                                        return JsonResponse({"type":'success', "message":"Completed!","data":data})

                                       # return redirect(f'/success/create_update_venture_result/{customer.id}/{venture_id}/{msg}/{request_action}')
                                        

                                    else:
                                        print(".....ventureForm is not valid!")
                                        print(f"all_valid: {all_valid}")
                                        return JsonResponse({"type":'error', "message":message,"data":{}})
                                        # amount  = request.POST.get("amount",0) 
                                        # cc  = request.POST.get("cc",0) 
                                        # ventureForm.totalCost =  float(amount) + float(cc)
                                        # context = {
                                        #         'asset_balance':asset_balance,
                                        #             'venture': ventureForm,   
                                        #             'limits':limits,
                                        #             'customer_info':customer_info,
                                        #             'member_info':member_info,
                                        #         }
                                        # print("returnin...")
                                        # return
                                        #return render(request, 'fx/venture/pos.html', context)
                
                else:   # for venture id > 0 --------------------------------------------------
                          print("-----------POST begins ")
                          if all_valid:
                                Success = True
                                percent = 95   ##?? rec:var
                                filter_fields = {"amount":amount,"cc":cc,"percent":percent,"in_charge":staff_info.id}
                                update_venture_qs ="" #delete
                                
                                if source_type != old_source_type:
                                        filter_fields["source_type"] = source_type
                                
                                if source_type == 'K':
                                        filter_fields['customer_source_id'] = 0
                                        print("----source type is k")
                                        # filter_fields['seller_source_id'] = 0
                                        if old_source_type == 'W':
                                                Success = account_manager_delete(venture_qs.customer_source_id,customer_source_fund,"@customer:if old_source_type == 'W'")
                                                # if Success:
                                                #      Success = account_manager_delete(venture_qs.seller_source_id,seller_dest_fund,"@seller:if old_source_type == 'W'")
                                else:  #source_type == old_source_type:
                                        
                                        if old_source_type != 'W': 
                                                return_id = account_manager_create(customer,customer_source_fund, venture_id,description,category,'W', date.today(),amount,0,"@customer:old_source_type != 'W'")
                                                if return_id <=0:
                                                        Success = False
                                                else:
                                                        filter_fields['customer_source_id'] = return_id
                                                # if Success:
                                                #         return_id = account_manager_create(seller,seller_dest_fund, venture_id,description,category,'D', date.today(),0,amount,"@customer:old_source_type != 'W'")
                                                #         if return_id <=0:
                                                #                Success = False
                                                #         else:
                                                #               filter_fields['seller_source_id'] = return_id
                                        else:    
                                                Success = account_manager_update(venture_qs.customer_source_id, amount,0,customer_source_fund,"@customer:account_manager_update:")
                                                # if Success:
                                                #       Success = account_manager_update(venture_qs.seller_source_id, 0,amount,seller_dest_fund,"@customer:account_manager_update:")
                                
                                if  old_customer_cc_id <=0: # save new record if there is not existing cc yet
                                        if cc > 0: 
                                                cc_id = cc_manager_create(venture_id,description,"W",cc,0,customer,category,date.today(),customer_source_fund,"@customer:cc_manager_create")
                                                filter_fields["customer_cc_id"] = cc_id
                                                if cc_id <= 0:
                                                        Success = False
                                                # if Success:
                                                #         cc_id = cc_manager_create(venture_id,description,"D",0,cc,seller,category,date.today(),seller_dest_fund,"@seller:cc_manager_create" )
                                                #         filter_fields["seller_cc_id"] = cc_id
                                                #         if cc_id <= 0:
                                                #             Success = False
                                else:
                                        if cc <=0:
                                                Success = cc_manager_delete(venture_qs.customer_cc_id,customer_source_fund,"@customer:cc_manager_delete") 
                                                filter_fields["customer_cc_id"] = 0
                                                # if  Success:
                                                #         Success = cc_manager_delete(venture_qs.seller_cc_id,seller_dest_fund,"@seller:cc_manager_delete" )
                                                #         filter_fields["seller_cc_id"] = 0
                                        else:
                                                if old_cc != cc:
                                                        Success = cc_manager_update(venture_qs.customer_cc_id,cc,0, customer_source_fund,"@customer:cc_manager_update:")
                                                        # if Success:
                                                        #         Success = cc_manager_update(venture_qs.seller_cc_id,0,cc,seller_dest_fund,"@seller:cc_manager_update:")
                                response ={}
                                 
                                if old_note != note:
                                        if note =="":
                                                filter_fields["note_id"] = 0
                                                if old_note_id > 0:
                                                    response= create_or_update_venture_note(DELETE_RECORD,old_note_id,"",2) #delete note  
                                        else:
                                                #3334
                                                print("-----------editing.....")
                                                response= create_or_update_venture_note (EDIT_RECORD,venture_qs.note_id,note,2) #todo 
                                                if response["Success"] and response["result"] > 0 and old_note_id <=0:
                                                        filter_fields["note_id"] = response["result"]
                                                        ##11-25
                                if Success:
                                        update_venture_qs = Model.objects.filter(id =venture_id).update( **filter_fields)
                                        print(f"response:{response} update_venture_qs: {update_venture_qs}, filter_fields : {filter_fields}")
                                        
                                        if Success:
                                            response = add_regular_transaction(1,change_deposit_to,customer,"Change Deposit","D",change_amount,0,venture_id) 
                                        if response["Success"]:
                                            # response = add_change_transaction(venture_id, response["id"],venture_id,amount)
                                             print("success................")
                                        #msg ="Customer Payment has been successfully recorded!"
                                        data ={"venture_id":venture_id,"amount":venture_qs.amount,'cc':venture_qs.cc,"source":venture_qs.source_type}
                                        return JsonResponse({"type":'success', "message":"Completed!","data":data})
                                       # return redirect(f'/success/create_update_venture_result/{customer.id}/{venture_qs.id}/{msg}/{request_action}')
                                else:
                                    
                                       print("Sorry. Technical error has been encountered!")
                                       logger.warning ("Sorry. Technical error has been encountered at pos_view venture_id > 0!")
                                       return JsonResponse({"type":'error', "message":"Unable to process this request!","data":{}})
                    
                    
    
#heys


class price_edit_view(View):
    
    def get(self, request, *args, **kwargs):
        print("---price_edit_view-")
      
        if  request.user.is_authenticated is True:  
               
                product_id = request.GET.get('product_id',"").strip()
                print(f">>> >product_id:{product_id}")
                try:
                       product_qs =  ProductModel.objects.get(product_id=product_id)
                       data ={"title":product_qs.title,"qty":product_qs.qty,"price":product_qs.price,"reg_price":product_qs.reg_price,"whole_sale":product_qs.whole_sale_price,"hasbarcode":product_qs.hasbarcode }
                except Exception as e:
                    print(f"Error: venture > 0 at POST: {e}")
                    logger.warning("Error: venture > 0 at POST: {e}")
                    return JsonResponse({"type":'error', "message":"Unable to read price!","data":{}})
               
                return JsonResponse({"type":'success', "message":"Success","data":data })
            
                        
        else:
                        print("here------------------------------- ")
                        return JsonResponse({"type":'error', "message":"Invalid Transaction Request!","data":{}})
    def post(self, request, *args, **kwargs):
         
              
                if request.user.is_staff and request.user.is_active:
                            print (f"user: {request.user}")
                            # staff_info=""
                            # try:
                            #     staff_info =  MemberModel.objects.get(user_id  = request.user.id) 
                            #     print(f"..staff_info:{staff_info.name}")
                            # except Exception as e:
                            # # raise Http404("Sorry. User id does not exist!")
                            #     print(f"def cuv @exception, id: None , e:{e}")
                            #     logger.warning(f"def cuv @exception,e:{e}" ) 
                else:
                                print("going to unauthorized user page")  
                                return redirect('/venture_login/') #
                            # return redirect('/unauthorized_user/') #
               
                
                print(f"------Post--------")
                barcode =   request.POST.get('barcode','').strip()
                title = request.POST.get('title',"").strip()
                quantity =float(request.POST.get('quantity',"0").strip())
                unit_price = float(request.POST.get('unit_price','0').strip())
                regular_price = float(request.POST.get('regular_price','0').strip())
                whole_sale = request.POST.get('whole_sale',"0").strip()
                
                print(f"barcode: {barcode}, title: {title}, quantity: {quantity},unit price: {unit_price}, regular price: {regular_price}, whole: {whole_sale}")
                filter_dict = {"product_id":barcode,"title":title,"qty":quantity,"price":unit_price,"reg_price":regular_price,"whole_sale_price":whole_sale}
                try:
                        res = ProductModel.objects.filter( product_id =barcode ).update( **filter_dict) #3 done editing
                        return JsonResponse({"type":'success', "message":"Successfully updated"})
                except Exception as e:
                        
                        print (f"error:{e}, {type(e)}")
                        return JsonResponse({"type":'error', "message":"Unable to update item!","data":{}})
                    #loan = ""
                    #loan_qs = PersonalLoan.objects.filter(id=loan_qs.id) 
                    # for result in loan_qs:
                    #         loan = {"cc_loan":result.cc_loan,"saving":result.saving,"percent":result.percent,"source_type":result.source_type,"note":note}
                        return {"type":"error"} 
                return
            
             
                    
                               
def display_itemList(request):

    return render(request, 'fx/venture/display_itemlist.html', {})
    
    
class JsonRead(View):
    template_name = 'MW_Etc/jsonpost.html'
    def get(self,request):
        return render(request, self.template_name)

    def post(self,request):
        print("---------------:post")
       
        items = json.loads(request.body)
        print(f"---------------:{items }")
        try:
                for  obj in items:
                    print(obj)
                   # print(f"obj.customer :{}")
                    customer = qty=obj["customer"]
                    if customer == 1:
                        customer =4
                    itemsold= ProductSold (member_id = customer,qty=obj["qty"],price=obj['price'], cm=obj["cm"],amount=obj["amount"],item_id=obj["item_id"],description=obj["description"],transaction_id=obj["transaction_id"])
                    itemsold.save()
                    print("success addin to product sold")
                  
        except Exception as e:
             print(f"error writin: {e}")
             logger.waning(f"error at jsonRead: e: {e}")
             return JsonResponse({"type":"error"})
        
        return JsonResponse({"type":"success"})
         
    #       customer = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL ) # todo null=False
    #   item = models.ForeignKey(ItemModel,null =True, on_delete =models.SET_NULL ) # todo null=False
    #   product_id = models.CharField(max_length=13,blank =True)
    #   qty = models.PositiveIntegerField(default =0)
    #   amount = models.FloatField(default =0 )
    #   cm = models.FloatField(default =0 )
    #   price = models.FloatField(default =0 )
    #   transaction_id = models.PositiveIntegerField(default =0)
    
    # venture_qs = Model(customer = customer,category =category,
    #                                     amount = amount,cc = cc,transaction_type =transaction_type,date_entered =date_entered,
    #                                     source_type =source_type,percent =percent)

    #                             venture_qs.save()

def post_itemSold(request):
    print("-------------ok")
    try:
            items = json.loads(request.POST.get('data'))
            print(items)
    except Exception as e:
         print(f" error: {e}")
   # name = item['nameOfSchedule']['schedule_name']
   # Schedule.objects.create(schedule_name = name)
    return JsonResponse({"type":"success"})
         


       
def itemList(request):
    items = ProductModel.objects.all()
   # item_list = serializers.serialize('json', items)
 #  return HttpResponse(item_list, content_type="text/json-comment-filtered")
    data = list(items.values())
    # data = [{'label': 'Peter', 'email': 'peter@example.org'},
    #         {'label': 'Julia', 'email': 'julia@example.org'}]
    return JsonResponse({"data":data})
   #return HttpResponse(data, content_type="text/json-comment-filtered")
    
    
    #other way
    
    # data = [{'label': 'Peter', 'email': 'peter@example.org'},
    #         {'label': 'Julia', 'email': 'julia@example.org'}]

    # return JsonResponse(data, safe=False)
       

            

#def cuv2
def backup(request):
   
    items = MemberModel.objects.all()
   # item_list = serializers.serialize('json', items)
 #  return HttpResponse(item_list, content_type="text/json-comment-filtered")
    data = list(items.values())
    # data = [{'label': 'Peter', 'email': 'peter@example.org'},
    #         {'label': 'Julia', 'email': 'julia@example.org'}]
    #return JsonResponse({"data":data})
   #return HttpResponse(data, content_type="text/json-comment-filtered")
    
    
    #other way
    
    # data = [{'label': 'Peter', 'email': 'peter@example.org'},
    #         {'label': 'Julia', 'email': 'julia@example.org'}]

    # return JsonResponse(data, safe=False)
       
     

    with open('data_2_18.txt', 'w') as outfile:
        json.dump(data, outfile)
                
    return JsonResponse({"data":data})

@login_required(login_url='/venture_login/')


def create_update_venture1(request,customer_id,venture_id ):
    qs= VentureModel.objects.last()
    qs1= ProductModel.objects.all()
    
    post_list = serializers.serialize('json', qs1)
    print("----------  to json")
   # print(post_list)
    
    
    print(f"---------- id:{qs.id}")
    print (f"user: {request.user}")
    
    repeated_names = ProductModel.objects.values('title', 'product_id').annotate(Count('product_id')).order_by().filter(product_id__count__gt=1) 
    for row in repeated_names:
       print(f"title: {row['title']}------item__title: ")
    
    default_percentage = 95  #
    if request.user.is_staff and request.user.is_active:
        print (f"user: {request.user}")
        staff_info=""
        member_info={}
        customer_info={}
        try:
            staff_info =  MemberModel.objects.get(user_id  = request.user.id) 
            print(f"..staff_info:{staff_info.name}")
        except Exception as e:
           # raise Http404("Sorry. User id does not exist!")
            print(f"def cuv @exception, id: None , e:{e}")
            logger.warning(f"def cuv @exception,e:{e}" ) 
    else:
            print("going to unauthorized user page")  
            return redirect('/venture_login/') #
           # return redirect('/unauthorized_user/') #

    asset_balance ={}
    if  venture_id > 0:
                cc_balance = get_running_finance_balance("cc","member_id",venture_qs.customer_id)["running_balance"]
                if maximum_deposit < cc_balance: 
                    cc_balance = maximum_deposit
                asset_balance ={"cc_balance":cc_balance}
                
    tx = VentureModel.objects.select_related('customer').filter(date_entered__lte=datetime.today(),   in_charge_id =staff_info.id).order_by("-pk")[:30]   #.values('createdate').annotate(count=Count('id'))
    #date_entered__lte=datetime.today(), date_entered__gt=datetime.today()-timedelta(days=30
   # notes = CustomerNoteModel.objects.filter(date_entered__lte=datetime.today(), date_entered__gt=datetime.today()-timedelta(days=30),   member_id =4).order_by("-pk")[:100]
    print(f"--- in charge: {staff_info.id}")
    venture ={'transaction_type':'W','customer':walk_in_id,'source_type':'K','percent':default_percentage,"venture_id":0,"transId":qs.id}  
    items = ProductModel.objects.all()
     
         
 

   
    
    # for row in product_codes:
    #     print(f"code: {row['item__product_id']}------item__title: ")
    context = {      
                    'asset_balance':asset_balance,
                    'venture': venture,  
                    'transactions':tx,
                    'member_info':member_info,
                    'customer_info':customer_info,
                    'items':items,
                    
                }
    # print(f"transaction:{tx.query}")
    # for  obj in tx:
    #     print(f"key:, value : {obj.customer.member_id}")
  
    
    return render(request, 'fx/venture/venture_pos.html', context)

@login_required(login_url='/venture_login/')
def create_update_venture(request,customer_id,venture_id ):
    member_id =customer_id
    # v =ValidateUsername("DA1212-1") 
    # print(f"v: {v}")
    # return
    # logger.info('>>>>>>>>>>>>>> init cuv!')
    # print('>>>>>>>>>>>>>> init cuv!')
    
  #  saveTransHistory(11,2,TRANS_VENTURE,111,"test",100,NEW_RECORD)
    
  #  return
    print (f"user: {request.user}")
    if request.user.is_staff and request.user.is_active:
        print (f"user: {request.user}")
        staff_info=""
        try:
            staff_info =  MemberModel.objects.get(user_id  = request.user.id) 
            print(f"..staff_info:{staff_info.name}")
        except Exception as e:
           # raise Http404("Sorry. User id does not exist!")
            print(f"def cuv @exception, id: None , e:{e}")
            logger.warning(f"def cuv @exception,e:{e}" ) 
    else:
            print("going to unauthorized user page")  
            return redirect('/venture_login/') #
           # return redirect('/unauthorized_user/') #

  
    ##request_action =request_action.strip().lower()
    ##model_name =model_list.get(request_action) 
    Model = apps.get_model('fx', "VentureModel")
    customer = int(request.POST.get("customer",-1))
    if customer == walk_in_id:
        member = False
    else:
        member = True
        
    
    
    
    print(f" customer: {customer}--- member: {member}")
    all_valid = True 
    default_percentage = 95  #
    member_info = get_member_info( member_id,"#create_update_venture. 1")  #create_update_venture. 1
   # print(f"model_name:{model_name}")
    #return
    request_action = "venture"
    if  request_action == "venture":
            category = CAT_VENTURE
            description ="GROCERY"
            customer_source_fund = SOURCE_REGULAR
            seller_dest_fund =SOURCE_VENTURE
     
   ## seller = member_info.id
    if venture_id > 0: #edit
        venture_qs= get_object_or_404(Model, id=venture_id)
    customer_id = 0
    asset_balance={}
    print(f"venture_id:{venture_id}, category:{category}")

    if member and venture_id > 0:
                cc_balance = get_running_finance_balance("cc","member_id",venture_qs.customer_id)["running_balance"]
                if maximum_deposit < cc_balance: 
                    cc_balance = maximum_deposit
                asset_balance ={"cc_balance":cc_balance}
    if request.method == 'GET':
                if venture_id > 0:  # requesting to edit the existing   data
                            if  request_action == "venture":
                                    customer = venture_qs.customer_id
                                    ventureForm = VentureForm( instance=venture_qs) # instance=saving bcoz editing process, none when new record
                            # else:
                            #         if   venture_qs.role_type == "S": #here the the default seller becomes the buyer or customer
                            #                 customer = venture_qs.seller_id
                            #         else:
                            #                 customer = venture_qs.customer_id
                            #         ventureForm = TradeForm( instance=venture_qs) # instance=saving bcoz editing process, none when new record
                            #print(f"........ventureForm.id: {venture_qs.id}")
                            customer_info = get_member_info( customer,"#create_update_venture. 1") #create_update_venture. 1
                            ventureForm.id= venture_qs.id
                            ventureForm.totalCost = venture_qs.amount + venture_qs.cc
                            ventureForm.request_action =request_action
                            if member:
                                   asset_balance["cc_balance"] = asset_balance["cc_balance"] + venture_qs.cc
                            #print(f"........asset_balance['cc_balance'] {asset_balance['cc_balance']} ,") 
                            if venture_qs.note_id > 0: #note has been provided
                                    try:
                                          ventureForm.note = NoteModel.objects.get(id=venture_qs.note_id).note #todo: handler
                                    except Exception as e:
                                        print(f"loan app note: {e}")
                            else: 
                                    ventureForm.note =""
                            try:
                                        change_table_qs = Change_Table.objects.get(venture_id= venture_id)
                                        ventureForm.change = change_table_qs.change
                                        ventureForm.tender =  venture_qs.amount + change_table_qs.change
                                        
                                        ventureForm.destination_acct_code =change_table_qs.destination_acct_code

                                        
                                        print(f"ventureForm.tender:{ventureForm.tender},change_table_qs.change:{change_table_qs.change},change_table_qs.destination_acct_code:{change_table_qs.destination_acct_code} ")
                            except Exception as e:
                                    ventureForm.change =""
                                    ventureForm.tender =""
                                    print(f"cresate_update_venture:change_table: {e}")
                else:  # NEW VENTURE 
                    if  request_action == "venture":
                            initial_data ={'in_charge':member_id,'transaction_type':'W','customer':member_id, 'cc':'','source_type':'K','date_entered': date.today(),'percent':default_percentage}  
                            ventureForm = VentureForm(initial =initial_data)
                    # else:
                    #         initial_data ={'transaction_type':'W', 'seller':member_id,'customer':customer_id, 'cc':'','source_type':'K','date_entered': date.today(),'percent':default_percentage} 
                    #         ventureForm = TradeForm(initial =initial_data)
                    
                   # ventureForm = VentureForm(initial =initial_data)
                    # ventureForm.request_action = request_action
                    # print(f"request_action: {ventureForm.request_action}")
                    ventureForm.note = "" #delete
                    customer_info=""
                    
                ventureForm.staff = staff_info.name
                
                context = {
                    'asset_balance':asset_balance,
                    'venture': ventureForm,  
                    'limits':limits,
                    'member_info':member_info,
                    'customer_info':customer_info,
                }
                return render(request, 'fx/venture/pos.html', context)

    else:   # request.method == 'POST':
        
        
        change_deposit_to  = request.POST.get("change_deposit_to","").strip()
        print(f"change_deposit_to:"+ change_deposit_to)
         
        change_amount  = request.POST.get("change","0").strip()
        if change_amount == "":
             change_amount =0
        else:
            change_amount =float(change_amount)
            
             
        
        print(f"change_deposit_to:{change_deposit_to}, change_amount:{change_amount}")
        customer  = int(request.POST.get("customer",-1))
         
        
        amount  = request.POST.get("amount",0) 
        cc  = request.POST.get("cc","00") 
        print(f"---------- cc: {cc}")
        percent  = float(request.POST.get("percent",-1)) #delete
        # customer  = int(request.POST.get("customer",-1))
        seller  = int(request.POST.get("seller",-1))
        
        source_type  = request.POST.get('source_type','K') 
        note = request.POST.get("venture_note", "").strip()

        print(f".......note: {note}")
        print(f"--- customer:{customer},cust type: {type(customer)}..note:{note},cc: {cc} cc-type:{type(cc)} ,amount:{amount}, customer: {customer}, type: {type(customer)} ,source_type:{source_type} ")
         
        running_balance =-1
        old_amount = 0
        #+
        if request_action == "trade":
              role_type  = request.POST.get("role_type","").strip()
        else:
              role_type ="" 
        if role_type == 'S':
            cust = seller
        else:
            cust = customer

        customer_info = get_member_info(cust,"#request.method == 'POST'. 1") #request.method == 'POST'. 1
        if venture_id > 0:
                    old_venture_qs =  get_object_or_404(Model, id=venture_id)
                    if  old_venture_qs.source_type =="W": #1
                             old_amount = old_venture_qs.amount
                    old_source_type = old_venture_qs.source_type
                    old_cc = old_venture_qs.cc
                    old_customer_cc_id = old_venture_qs.customer_cc_id
                    old_customer_id =  old_venture_qs.customer_id
                    old_note_id = old_venture_qs.note_id

                    #+
                    if request_action == "trade":
                         old_role_type=  old_venture_qs.role_type
                    else:
                         old_role_type =""

                    if old_note_id > 0:
                            try:
                                old_note = NoteModel.objects.get(id = old_note_id ).note
                            except Exception as e:
                                print(f"getting note: {e}")
                    else:
                            old_note = ""
        else:
                    #old_amount = 0 
                    old_customer_id = customer
                    old_cc = 0
        if old_customer_id != customer:
                    all_valid = False
                    print("Technical problem encountered while saving record.")
                    messages.error(request, f"Message: Technical problem encountered while saving record.")
        if member:
            cc_running_balance = get_running_finance_balance("cc","member_id",customer)["running_balance"]
        
        if member and len(cc.strip()) > 0 and float(cc) > cc_running_balance + old_cc:
                    all_valid = False
                    if running_balance > 2000:
                         messages.error(request, f"Message: Insufficient funds in  Community Coin(CC) Account!")
                    else:
                        running_balance ='{:,.2f}'.format(running_balance)
                        messages.error(request, f"Message: Please enter an CC amount that is no more than {running_balance}")

        if member and source_type =="W":
            running_balance = get_running_finance_balance("wallet","member_id",customer)["running_balance"]
            if  len(amount.strip()) > 0 and float(amount) > running_balance + old_amount:
                all_valid = False
               
                if running_balance > 2000:
                     messages.error(request, f"Message: Insufficient funds in Wallet Account!")
                else:
                    if running_balance > 0:
                            running_balance ='{:,.2f}'.format(running_balance)
                            messages.error(request, f"Message: Please enter an amount that is no more than P{running_balance}")
                    else:
                         messages.error(request, f"Message: Sorry. Wallet Account is empty!")
                print("..all_valid:",all_valid)
        else:
            customer_source_id = 0
    # EDIT EXISTING RECORD (POST)---------------------------------------------------------------
        ##here
        if venture_id >  0:
                        
                       
                        ventureForm = VentureForm(request.POST,request.POST,instance=venture_qs )
                        form_valid = ventureForm.is_valid()
                        if all_valid and form_valid:
                                Success = True
                                amount = ventureForm.cleaned_data['amount']
                                customer = ventureForm.cleaned_data['customer']
                                # # seller = ventureForm.cleaned_data['seller']
                                cc = ventureForm.cleaned_data['cc']  
                                percent = ventureForm.cleaned_data['percent']
                                source_type = ventureForm.cleaned_data['source_type'] 
                                
                                filter_fields = {"amount":amount,"cc":cc,"percent":percent,"in_charge":staff_info.id}
                                update_venture_qs ="" #delete
                                #+
                                # if request_action == "trade":
                                #     role_type = ventureForm.cleaned_data['role_type'] 
                                #     if old_role_type != role_type: # indent to the right
                                #         filter_fields["role_type"] = role_type

                                if source_type != old_source_type:
                                        filter_fields["source_type"] = source_type
                                if source_type == 'K':
                                        filter_fields['customer_source_id'] = 0
                                        # filter_fields['seller_source_id'] = 0
                                        if old_source_type == 'W':
                                                Success = account_manager_delete(venture_qs.customer_source_id,customer_source_fund,"@customer:if old_source_type == 'W'")
                                                # if Success:
                                                #      Success = account_manager_delete(venture_qs.seller_source_id,seller_dest_fund,"@seller:if old_source_type == 'W'")
                                else:  #source_type == old_source_type:
                                        if old_source_type != 'W': 
                                                return_id = account_manager_create(customer,customer_source_fund, venture_id,description,category,'W', date.today(),amount,0,"@customer:old_source_type != 'W'")
                                                if return_id <=0:
                                                        Success = False
                                                else:
                                                        filter_fields['customer_source_id'] = return_id
                                                # if Success:
                                                #         return_id = account_manager_create(seller,seller_dest_fund, venture_id,description,category,'D', date.today(),0,amount,"@customer:old_source_type != 'W'")
                                                #         if return_id <=0:
                                                #                Success = False
                                                #         else:
                                                #               filter_fields['seller_source_id'] = return_id
                                        else:    
                                                Success = account_manager_update(venture_qs.customer_source_id, amount,0,customer_source_fund,"@customer:account_manager_update:")
                                                # if Success:
                                                #       Success = account_manager_update(venture_qs.seller_source_id, 0,amount,seller_dest_fund,"@customer:account_manager_update:")
                                
                                if  old_customer_cc_id <=0: # save new record if there is not existing cc yet
                                        if cc > 0: 
                                                cc_id = cc_manager_create(venture_id,description,"W",cc,0,customer,category,date.today(),customer_source_fund,"@customer:cc_manager_create")
                                                filter_fields["customer_cc_id"] = cc_id
                                                if cc_id <= 0:
                                                        Success = False
                                                # if Success:
                                                #         cc_id = cc_manager_create(venture_id,description,"D",0,cc,seller,category,date.today(),seller_dest_fund,"@seller:cc_manager_create" )
                                                #         filter_fields["seller_cc_id"] = cc_id
                                                #         if cc_id <= 0:
                                                #             Success = False
                                else:
                                        if cc <=0:
                                                Success = cc_manager_delete(venture_qs.customer_cc_id,customer_source_fund,"@customer:cc_manager_delete") 
                                                filter_fields["customer_cc_id"] = 0
                                                # if  Success:
                                                #         Success = cc_manager_delete(venture_qs.seller_cc_id,seller_dest_fund,"@seller:cc_manager_delete" )
                                                #         filter_fields["seller_cc_id"] = 0
                                        else:
                                                if old_cc != cc:
                                                        Success = cc_manager_update(venture_qs.customer_cc_id,cc,0, customer_source_fund,"@customer:cc_manager_update:")
                                                        # if Success:
                                                        #         Success = cc_manager_update(venture_qs.seller_cc_id,0,cc,seller_dest_fund,"@seller:cc_manager_update:")
                                response ={}
                                if old_note != note:
                                        if note =="":
                                                filter_fields["note_id"] = 0
                                                if old_note_id > 0:
                                                    response= create_or_update_venture_note(old_note_id,"",2) #delete note  
                                        else:
                                                response= create_or_update_venture_note(venture_qs.note_id,note,2) #todo 
                                                if response["Success"] and response["result"] > 0 and old_note_id <=0:
                                                        filter_fields["note_id"] = response["result"]
                                                        ##11-25
                                if Success:
                                        update_venture_qs = Model.objects.filter(id =venture_id).update( **filter_fields)
                                        print(f"response:{response} update_venture_qs: {update_venture_qs}, filter_fields : {filter_fields}")
                                        
                                        if Success:
                                            response = add_regular_transaction(1,change_deposit_to,customer,"Change Deposit","D",change_amount,0,venture_id) 
                                        if response["Success"]:
                                            # response = add_change_transaction(venture_id, response["id"],venture_id,amount)
                                            
                                             print("success................")
                                        
                                       
                                       
                                        msg ="Customer Payment has been successfully recorded!"
                                        return redirect(f'/success/create_update_venture_result/{customer.id}/{venture_qs.id}/{msg}/{request_action}')
                                else:
                                    
                                    messages.info("Sorry. Technical error has been encountered!")
                        #NOT VALID---------------------------------------------------------
                        
                        print("not valid..")
                        ventureForm.totalCost = venture_qs.total_cost #float(amount) + float(cc)
                        context = {'asset_balance':asset_balance,'venture': ventureForm,'limits':limits,'customer_info':customer_info,'member_info':member_info}   
                        return render(request, 'fx/venture/pos.html', context)
        else: #venture_id == 0:              ----  P O S T  ----
                    
                    if  request_action == "venture":
                            ventureForm = VentureForm(request.POST)
                            form_valid = ventureForm.is_valid()
                   
                    if all_valid and form_valid:
                        print(".....ventureForm is valid!")
                        amount = ventureForm.cleaned_data['amount']
                        customer = ventureForm.cleaned_data['customer']
                        print(f">>>>>>>>>>>>>> customer id: {customer.member_id} ,{customer.id}")
                    
                        transaction_type = ventureForm.cleaned_data['transaction_type']
                        date_entered = ventureForm.cleaned_data['date_entered']
                        source_type = ventureForm.cleaned_data['source_type']
                        cc =  ventureForm.cleaned_data['cc']
                        percent = ventureForm.cleaned_data['percent']
                     
                                      
                        Success = True
                        venture_id_change =venture_id
                        venture_id = 0
                        try:
                                if request_action == "trade":
                                      pass
                                else:
                                        venture_qs = Model(customer = customer,category =category,
                                        amount = amount,cc = cc,transaction_type =transaction_type,date_entered =date_entered,
                                        source_type =source_type,percent =percent)

                                venture_qs.save()
                                venture_id =venture_qs.id
                        except Exception as e:
                            Success = False
                            print(f"creating venture transaction: {e}")
                        filter_fields = {"flag":1,'in_charge':staff_info.id} 
                       
                                 
                                 
                        if source_type =="W": #create new record. A
                                customer_source_id = account_manager_create(customer,customer_source_fund, venture_id,description,category,'W', date.today(),amount,0,"#create new record. A")
                                filter_fields["customer_source_id"] =customer_source_id
                                if customer_source_id <=0:
                                       Success = False
                                # if Success: #create new record. B
                                #        # filter_fields["customer_source_id"] =customer_source_id
                                #         seller_source_id = account_manager_create(seller,seller_dest_fund, venture_id,description,category,'D', date.today(),0,amount,"create new record. B")
                                #         if seller_source_id <=0:
                                #             Success = False
                                #         if Success:
                                #             filter_fields["seller_source_id"] =seller_source_id
                                         
                        # print(f"...seller:,customer:{customer}, customer: {customer} ,source_type:{source_type} ")
                        # print(f"...transaction_type:{transaction_type}, date_entered: {date_entered} ,cc:{cc} , percent: {percent}")
                        
                        if cc > 0: #create new record. C
                                customer_cc_id = cc_manager_create(venture_id,description,"W",cc,0,customer,category,date.today(),customer_source_fund,"create new record. C")
                                filter_fields["customer_cc_id"]= customer_cc_id
                                if customer_cc_id <= 0:
                                    Success = False
                                # if Success: #create new record. D
                                #     seller_cc_id = cc_manager_create(venture_id,description,"D",0,cc,seller,category,date.today(),seller_dest_fund,"create new record. D")
                                #     filter_fields["seller_cc_id"]= seller_cc_id
                                #     if seller_cc_id <= 0:
                                #         Success = False

                        else:
                           filter_fields["customer_cc_id"] =0
                        note_id = 0
                        response = {}    
                        print(f"today filter_fields: {filter_fields} ")
                                 
                                 
                                 
                                         
                      
                        if note != "":
                            response = create_or_update_venture_note(0,note,2) #todo 
                            if response["Success"] and response["result"] > 0 :
                                note_id  = response["result"]
                        else:
                              note_id = 0  
                        filter_fields["note_id"] = note_id
                        # if response:
                        #      print(f".... note id: {note_id}, success:{response['Success']}, result:{response['result']} ")
                        # print(f"filter_fields: {filter_fields}")
                        
                        
                        
                        
                        
                        
                        
                        if Success:
                                Success = True
                                try:
                                    venture_result = Model.objects.filter(id = venture_id).update( **filter_fields)
                                    print(f"venture: filter_fields: {filter_fields} ,venture_result: {venture_result}")
                                    
                                except Exception as e:
                                        print (f"error result:{e}, {type(e)}")
                                        Success = False
                                #11-25
                                if Success and change_amount > 0:
                                      
                                        print(f"============ change amnt:{change_amount}")
                                        response = add_regular_transaction(0,change_deposit_to,customer,"Change Deposit","D",change_amount,0,venture_id)
                                        if response["Success"] :
                                           #  response = add_change_transaction(venture_id_change, response["id"],venture_id,amount)
                                            
                                             print("success................")
                                else:
                                     print(f"ELSE:  change_amount:{change_amount}")
                                     
                                if Success: #save day transaction for the cashier
                                     pass
                                    
                                     # saveTransHistory(request.user.id,member_id,TRANS_VENTURE,venture_id,description, amount,NEW_RECORD) # new entry
                                
                                
                                
                                    
                            # if Success and source_id > 0:
                            #       wallet_qs = WalletModel.objects.filter( id = source_id).update(source_id = venture_id)
                            # if Success and cc_create_result > 0:
                            #    cc_qs = CcModel.objects.filter( id = cc_create_result).update(source_id = venture_id)
                                  
                        print(f"Success: {Success}")
                        msg ="Customer Payment has been successfully recorded!"
                        return redirect(f'/success/create_update_venture_result/{customer.id}/{venture_id}/{msg}/{request_action}')
                        

                    else:
                        print(".....ventureForm is not valid!")
                        print(f"all_valid: {all_valid}")
                        amount  = request.POST.get("amount",0) 
                        cc  = request.POST.get("cc",0) 
                        ventureForm.totalCost =  float(amount) + float(cc)
                        context = {
                                   'asset_balance':asset_balance,
                                    'venture': ventureForm,   
                                    'limits':limits,
                                    'customer_info':customer_info,
                                    'member_info':member_info,
                                }
                        return render(request, 'fx/venture/pos.html', context)

def get_due_date_string(value):
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
def get_all_balances(member_id):
        try:
            filter_field_value = member_id #WalletTransaction.objects.get(client_id = member_id) # if client has previous transaction with interest entry and soon then
            wallet = get_running_finance_balance("wallet","member_id",filter_field_value)["running_balance"]
            cc = get_running_finance_balance("cc","member_id",member_id)["running_balance"]
            saving = get_running_finance_balance("saving","member_id",member_id)["running_balance"]
            loan = get_running_finance_balance("payment","member_id",member_id)["running_balance"]
            credit_limit = get_running_finance_balance("credit_limit","member_id",member_id)["running_balance"]
            
            print(f"credit limit balance-------------:  {credit_limit}")
            return {"wallet":round(wallet,2),"loan":round(loan,2),"cc":round(cc),"saving":round(saving,2),"credit_limit":round(credit_limit,2)}
        except Exception as e:
            print (f"Get all balances: {e}, {type(e)}")
            return False

def get_balances(request):
   

    #21
    if request.is_ajax and request.method == "GET":
        member_id = int(request.GET.get("member_id", 0).strip())
        balance = get_all_balances(member_id)
        if balance:
          return JsonResponse({"data":"Success","balances":balance}, status = 200)
        #todo what action?

    return JsonResponse({}, status = 400)

def data_load_more(request):
    if request.is_ajax and request.method == "GET"  and request.user.is_authenticated is True:
        total_no_of_row_per_page= int(request.GET.get("total_no_of_row_per_page", 5))  # total rows to be displayed
        last_row = int(request.GET.get("last_row", 5))
        filter_field_value = int(request.GET.get("filter_field_value",0))
        filter_field = request.GET.get("filter_field","").strip()
        filter_dict = {filter_field: filter_field_value}
        total_records = PersonalLoanModel.objects.filter( **filter_dict ).count()
        last_page = False
        print(f"....,(b4)last page:{last_page}, total_no_of_row_per_page: {total_no_of_row_per_page}")
        if last_row  + total_no_of_row_per_page  >= total_records:
                new_total_row = total_records - last_row
                total_no_of_row_per_page = new_total_row
                last_page = True
        print(f"....,(after)last page:{last_page},last row: {last_row} , total_no_of_row_per_page:{total_no_of_row_per_page}, total_records:{total_records} ,filter_field_value:{filter_field_value} filter_field: {filter_field}")
         
        loan_qs = PersonalLoanModel.objects.filter( **filter_dict )[last_row:last_row + total_no_of_row_per_page]
        data=[]
      
        for row in loan_qs:
            row ={"id":row.id,"cc_loan":row.cc_loan,"source_type":row.source_type,"saving":row.saving,"percent":row.percent,"date_entered":row.date_entered}
            data.append(row)
          
        return JsonResponse({"data":data,"last_page":last_page,"properties":{"total_record":total_records}}, status = 200)

    return JsonResponse({}, status = 400)

def create_update_loan_details(member_id,loan_qs,loanForm):
            note =loanForm.note.strip()
            saving_amount=loanForm.cleaned_data['saving']
            cc_loan =loanForm.cleaned_data['cc_loan']
            source_type =loanForm.cleaned_data['source_type']
            source_id =loanForm.cleaned_data['source_id']
            note_id = loanForm.cleaned_data['note_id']
            cc_id = loanForm.cleaned_data['cc_id']
            saving_id = loanForm.cleaned_data['saving_id']
            percent =loanForm.cleaned_data['percent']

            print(f"saving:{ saving_amount}, cc_loan:{ cc_loan},NOTE: {note}")
            print(f"source-type:{ source_type}, source_id:{ source_id}, note_id:{ note_id},cc_id:{ cc_id},saving_id:{saving_id}")
            
            Success = True
            if loan_qs: #EDIT LOAN
                    if source_type != "W":
                        source_id = 0
                    else:
                       source_id = loan_qs.source_id
                    try:
                        Pending_loan_qs = PendingLoanModel.objects.filter(loan_id =loan_qs.id ).update(saving =loan_qs.saving,cc_loan =loan_qs.cc_loan,percent =loan_qs.percent,source_id =loan_qs.source_id,source_type = loan_qs.source_type)
                        print(f"...success update  in pending_loan Pending_loan_qs: {Pending_loan_qs}")
                    except Exception as e:
                        Pending_loan_qs =0
                        print(f"...error creating new entries in pending_loan")
                        print (f"error:{e}, {type(e)}")
                    if  Pending_loan_qs <= 0:
                        try:
                            pending_qs = PendingLoanModel.objects.create(loan_id=loan_qs.id, saving = loan_qs.saving,cc_loan =loan_qs.cc_loan,percent =loan_qs.percent,source_id=loan_qs.source_id,source_type = loan_qs.source_type)
                            print(f"...creating new entries in pending_loan")
                        except Exception as e:
                                Success = False
                                print(f"...creating new entries in pending_loan")
                                print (f"error:{e}, {type(e)}")
                    if Success:
                        try:
                            loan = PersonalLoanModel.objects.filter(id = loan_qs.id).update(saving =saving_amount,cc_loan = cc_loan,percent = percent,source_type = source_type,source_id = source_id,flag = 2) # editing
                        except Exception as e: 
                            Success =False
                            print(f"...loan update")
                            print (f"error:{e}, {type(e)}")
                    if Success:
                        print(f" loan_qs.saving_id:{loan_qs.id}")
                        print(f"amount:{saving_amount} <> loan_qs.saving:{loan_qs.saving}")
        #-SAVING
                        if saving_amount != loan_qs.saving:
                            saving_qs = SavingModel.objects.filter(id = loan_qs.saving_id).update(credit = saving_amount)
        #-CC 
                        if cc_loan != loan_qs.cc_loan:
                            cc_qs = CcModel.objects.filter(id = loan_qs.cc_id).update(credit = cc_loan)
        #- PAYMENT
                        if Success:
                            try:  
                                category = 5 #loan
                                payment_qs = PaymentModel.objects.filter(id = loan_qs.saving_id).update(credit = saving_amount)
                            except Exception as e:
                                Success= False
                                print (f"error result:{e}, {type(e)}")
        #- WALLET               
                        if  source_type == "C" and loan_qs.source_type == "W":
                            print('deleting wallet')
                            wallet_qs=WalletModel.objects.get(id=loan_qs.source_id).delete()
                        print(f"(loan_qs.source_type:{loan_qs.source_type} and source_type:{source_type}  and (loan_qs.saving:{loan_qs.saving} != saving_amount:{saving_amount}")
                        if (loan_qs.source_type == "W" and source_type == "W")  and (loan_qs.saving != saving_amount):
                            print('updating wallet')
                            wallet_qs = WalletModel.objects.filter(id = loan_qs.source_id).update(debit = saving_amount)
                        new_wallet_entry = False
        
                        if loan_qs.source_type == "C" and source_type =="W":
                            try:  
                                description= "CC loan deposit"
                                category = 5
                                wallet = WalletModel(member_id = member_id, date_entered=date.today(),transaction_type='W' ,description=description,credit=0,debit=saving_amount,source_id =loan_qs.id ,category=category )
                                wallet.save() 
                                new_wallet_entry =True
                            except Exception as e:
                                Success= False
                                print(f"...result Wallet:")
                                print (f"{e}, {type(e)}")
                    note_id =0
                    note_result= {"action":-1,"note_id":0}
        #- NOTES
                    if Success and note !="":
                        note_result =  create_or_update_note(loan_qs.id,note,1,loan_qs.note_id)
                        if note_result["action"] < 0:
                            print("unable to update/create note")
                    if Success:
                        if new_wallet_entry:
                            filter_dict={"source_type":source_type, "source_id": wallet.id,"flag":3}
                        else:
                            filter_dict={"flag":3}
                    if note == "":
                        note_id =0 # for note ==""
                    else:
                        note_id = note_result["note_id"] #id of the note field
                        # 0 means edit and note_id > 0 note_id is needed because loan.note_id == 0
                    if note_id >= 0: # means 0 and greater must be  
                        filter_dict["note_id"] = note_id
                    print(f" filter_dict:{filter_dict},note_id:{note_id} old id:{loan_qs.note_id}, note: {note}" )
                    try:
                        res = PersonalLoanModel.objects.filter( id =loan_qs.id ).update( **filter_dict) #3 done editing
                    except Exception as e:
                        Success = False
                        print(f"...loan update last")
                        print (f"error:{e}, {type(e)}")
                    #loan = ""
                    #loan_qs = PersonalLoan.objects.filter(id=loan_qs.id) 
                    # for result in loan_qs:
                    #         loan = {"cc_loan":result.cc_loan,"saving":result.saving,"percent":result.percent,"source_type":result.source_type,"note":note}
                    return {"Success":Success} 
                    #print(f"......Success: {Success}")
        #- E L S E    
            else:  # New loan Application
                    try:
                        source_id = 0
                        saving = saving_amount
                        loan_qs = PersonalLoanModel(member_id = member_id, date_entered=date.today(),source_type=source_type ,source_id=source_id,saving=saving_amount ,cc_loan=cc_loan,percent = percent,flag = 0 )
                        loan_qs.save()
                    except Exception as e:
                        Success= False
                        print (f"error message in loan :{e}, {type(e)}")
                    #client,description,date_entered,transaction_type,debit,credit,category
                    if (Success and source_type == 'W'): #wallet only not cash
                        try:  
                            description= "Deposit for Loan Application"
                            category = 5
                            wallet = WalletModel(member_id = member_id, date_entered=date.today(),transaction_type='W' ,description=description,credit=0,debit=saving_amount,source_id =loan_qs.id ,category =category )
                            wallet.save() 
                        except Exception as e:
                            Success= False
                            print (f"error result:{e}, {type(e)}")
                             
                    if Success:
                        try:  
                            description= "Deposit For Loan Application"
                            category = 5 #loan
                            saving_qs = SavingModel(member_id = member_id, date_entered=date.today(),transaction_type='D' ,description=description,debit=0,credit=saving_amount,source_id =loan_qs.id,category=category  )
                            saving_qs.save() 
                        except Exception as e:
                            Success= False
                            print(f"...result saving_qs:")
                            print (f"error result: {e}, {type(e)}")
                            
                    if Success:
                        try:  
                            #description= "Saving from loan"
                            category = 5 #loan
                            payment_qs = PaymentModel(member_id = member_id, date_entered=date.today(),transaction_type='D',credit=cc_loan,debit=0,source_id =loan_qs.id,category=category  )
                            payment_qs.save() 
                        except Exception as e:
                            Success= False
                            print(f"...result payment_qs:")
                            print (f"error result:{e}, {type(e)}")
                             
                    
                    if Success:
                        try:  
                            description = "Loan amount granted"
                            category = 5 #loan
                            Cc_qs = CcModel(member_id = member_id, date_entered=date.today(),transaction_type='D' ,description=description,credit=cc_loan,debit=0,category=category,source_id =loan_qs.id )
                            Cc_qs.save() 
                        except Exception as e:
                            Success= False
                            print (f"error result:{e}, {type(e)}")
                    note_id =0
                    if Success and note !="":
                        
                        note_result =  create_or_update_note(loan_qs.id,note,1)
                        note_id = note_result["note_id"]
                        if note_result["action"] < 0:
                           Success =False
                    
                    if Success:
                        try:
                            #source_id referring to wallet field source_id  
                            if source_type == 'W':
                                result = PersonalLoanModel.objects.filter(id=loan_qs.id).update(source_id= wallet.id,saving_id =saving_qs.id,cc_id= Cc_qs.id,note_id=note_id,flag = 1)
                            else: #cash or may be saving account
                                result = PersonalLoanModel.objects.filter(id=loan_qs.id).update(source_id= 0,saving_id =saving_qs.id,cc_id= Cc_qs.id,note_id=note_id,flag = 1)
                            
                            #loan_qs = PersonalLoan.objects.filter(id=loan_qs.id)  #use by 'for result in loan_qs:'
                            print(f"...result Loan:",result)
                        except Exception as e:
                            Success= False
                            print(f"...result Cc_qs:")
                            print (f"{e}, {type(e)}")
                           # return JsonResponse({}, status = 400)
                        return {"Success":Success,"loan_id":loan_qs.id}
            return {"Success":False}
             
def create_update_loan_result(request,id,loan_id,msg):
       
        member_info = get_member_info(id,"#create_update_loan_result. 1")  #create_update_loan_result. 1
        loan_qs= get_object_or_404(PersonalLoanModel, id=loan_id)
        loanForm = PersonalLoanForm( instance=loan_qs)
        loanForm.id= loan_qs.id
        if loan_qs.note_id > 0: #note has been provided
            loanForm.note = NoteModel.objects.get(id=loan_qs.note_id).note #todo: handler
        else: 
            loanForm.note =""
        context = { 
                'post_data':True,
                'asset_liabities':get_all_balances(id),   #id = member_id
                'loan': loanForm,   
                'member_info':member_info,
            }
        print(f"::{context}")
        messages.success(request, msg)
        return render(request, 'fx/member/templates/loan_application.html', context)
def loan_application(request,member_id,loan_id):
            all_valid = True 
            allowed_percentage =200
            member_info = get_member_info(member_id,"#loan_application. 1") #loan_application. 1
            if loan_id > 1: #edit
                loan_qs= get_object_or_404(PersonalLoanModel, id=loan_id)
            account_name =""
            if request.method == 'GET':
                    if loan_id > 1:  # requesting to edit the existing loan data
                        loanForm = PersonalLoanForm( instance=loan_qs) # instance=saving bcoz editing process, none when new record
                        if loan_qs.source_type =="W":
                            account_name ="WALLET"
                        if loan_qs.note_id > 0: #note has been provided
                            try:
                               loanForm.note = NoteModel.objects.get(id=loan_qs.note_id).note #todo: handler
                            except Exception as e:
                                print(f"loan app note: {e}")
                        else: 
                            loanForm.note =""
                    else:  # requesting new loan application
                        initial_data ={'source_type':'C','date_entered': date.today(),'percent':allowed_percentage} #note: new loan app 
                        loanForm = PersonalLoanForm(initial =initial_data)
                        
                        loanForm.note = ""
                    loanForm.account_name= {account_name:"selected_account"} 
                    context = {
                            'asset_liabities':get_all_balances(member_id),
                            'loan': loanForm,   
                            'member_info':member_info,
                        }
                    return render(request, 'fx/member/templates/loan_application.html', context)
            else:  # request.method == 'POST'
               # print(f"......requested_action:{requested_action}")
                source_type = request.POST.get("source_type")
                saving_amount = request.POST.get("saving") 
                note = request.POST.get("note", "")
                 
                print(f"saving_amount:{saving_amount}, source_type:{source_type}, note:{note}")
                old_saving =0
                if loan_id > 0:
                    old_saving = loan_qs.saving 
                else:
                     old_saving =0
                if source_type =="W":
                        running_balance = get_running_finance_balance("wallet","member_id",member_id)["running_balance"]
                        if  len(saving_amount.strip()) > 0 and float(saving_amount) > running_balance + old_saving:
                            all_valid = False
                            running_balance ='{:,.2f}'.format(running_balance)
                            messages.error(request, f"The amount to deposit to Saving Account must not be more than {running_balance}")
                print("..all_valid:",all_valid)
                 
                if loan_id >  1: #edit
                        old_loan_qs =  get_object_or_404(PersonalLoanModel, id=loan_id)
                        loanForm = PersonalLoanForm(request.POST , instance=loan_qs )
                        loanForm.note =note
                        if all_valid and loanForm.is_valid():
                            result = create_update_loan_details(member_id,old_loan_qs,loanForm)
                            if  result["Success"]:
                                print("valid..")
                                msg ="Loan transaction has been successfully updated!"
                                return redirect(f'/success/create_update_loan_result/{member_id}/{loan_qs.id}/{msg}')
                        else:
                                print("not valid..")
                                context = {
                                    'asset_liabities':get_all_balances(member_id),
                                    'loan': loanForm,   
                                    'member_info':member_info,
                                }
                                return render(request, 'fx/member/templates/loan_application.html', context)
                else: #requested_action == 0: #new data entry
                    loanForm = PersonalLoanForm(request.POST)
                    loanForm.note = note
                    if all_valid and loanForm.is_valid():
                        result = create_update_loan_details(member_id,False,loanForm) #false  or loan_qs ="" because new entry: 
                        if  result["Success"] and result["loan_id"] > 0:
                            loan_id =result["loan_id"]
                            print("....success  new loan")
                            msg ="Loan transaction has been successfully added to the database!"
                            return redirect(f'/success/create_update_loan_result/{member_id}/{loan_id}/{msg}')
                        else:
                            messages.error(request, f"We apolized that we encountered unexpected error while saving.")


                    else:
                        context = {
                                    'asset_liabities':get_all_balances(member_id),
                                    'loan': loanForm,   
                                    'member_info':member_info,
                                }
                    return render(request, 'fx/member/templates/loan_application.html', context)

###          
def get_transfer_details(request):
    #note: source_id is the id of sources(Wallet,Saving)
    id = int(request.GET.get("source_id", 0).strip())
    source_name = request.GET.get("source_name", "").strip().lower() # or account name
    #source_type = request.GET.get("source_type", 0).strip()
     
    print(f"source_id: {id}, source_name: {source_name}")
    
    if request.is_ajax and request.method == "GET":
        model_list= {"cc":"CcModel","wallet":"WalletModel","saving":"SavingModel"}
        model_name =model_list.get(source_name) 
        Model = apps.get_model('fx', model_name)
        source_qs = Model.objects.get(id=id) 
         
       # date_entered =get_due_date_string (loan_qs.date_entered)
        if source_qs.transaction_type == 'D':
            amount = source_qs.credit
        else:
            amount = source_qs.debit
        

        print(f"....transfer_qs.source_id: {source_qs.source_id}")
        transfer_qs = TransferModel.objects.get(id=source_qs.source_id) 
        #print(f"...dir:{dir(transfer_qs.receiver)}")
        status_list={"A":"Accepted","C":"Cancelled","W":"Waiting","R":"Rejected"}
        if transfer_qs.status == 'W':
            date_accounted =""
        else:
          date_accounted = transfer_qs.date_accounted
        fullname = transfer_qs.receiver.gender.title() +" "+ transfer_qs.receiver.firstname.title()+ " "+transfer_qs.receiver.lastname.title()
        transfer_dict = {"fullname":fullname ,"date":date_accounted,"status":status_list.get(transfer_qs.status),"amount":amount,"transaction":source_qs.transaction_type,"date_entered":source_qs.date_entered,"description":source_qs.description}
        filter_dict = {"code":transfer_qs.code,"sender_id": transfer_qs.sender_id }
        receiver_qs = TransferModel.objects.select_related('receiver').order_by('receiver_id').filter( **filter_dict )
        count = receiver_qs.count()
        print(f"......count recrs: {count}")
        data=[]
        # if count == 1:
        #     data.append("name":)
        if count > 1:
                for row in receiver_qs:
                    row ={ "id":row.id,"date":row.date_entered ,"purpose": row.purpose,"gender":row.receiver.gender,"firstname":row.receiver.firstname.title(),"lastname":row.receiver.lastname.title(),"address":row.receiver.address.title(),"amount":row.amount,"status":row.status,"username":row.receiver.user.username}
                    data.append(row)
        
      
        print("data of receiver:",data)
        return JsonResponse({"data":"Success","transfer":transfer_dict,"receivers":data}, status = 200)
            
    return JsonResponse({}, status = 400)   
def get_source_details(request):
    #note: source_id is the id of sources(Wallet,Saving)
    id = int(request.GET.get("source_id", 0).strip())
    source_name = request.GET.get("source_name", "").strip().lower() # or account name
    #source_type = request.GET.get("source_type", 0).strip()
     
    print(f"source_id: {id}, source_name: {source_name}")
    
    if request.is_ajax and request.method == "GET":
        model_list= {"wallet":"WalletModel","saving":"SavingModel"}
        model_name =model_list.get(source_name) 
        Model = apps.get_model('fx', model_name)
        source_qs = Model.objects.get(id=id) 
         
       # date_entered =get_due_date_string (loan_qs.date_entered)
        if source_qs.transaction_type == 'D':
           # transaction="DEPOSIT"
            amount = source_qs.credit
        else:
           # transaction="WITHDRAWAL"
            amount = source_qs.debit
        source_dict = {"amount":amount,"transaction":source_qs.transaction_type,"date_entered":source_qs.date_entered,"description":source_qs.description}
         
         
        print("source_dict:",source_dict)
        return JsonResponse({"data":"Success","source":source_dict}, status = 200)
            
    return JsonResponse({}, status = 400)



def get_payment_details(request):
    payment_id = int(request.GET.get("payment_id", 0).strip())
    print(f"payment_id:{payment_id}")
    if request.is_ajax and request.method == "GET":
        payment_qs = PaymentModel.objects.get(id=payment_id) 
        payment = {"id":payment_qs.id,"transaction_type":payment_qs.transaction_type,"date_entered":payment_qs.date_entered,"amount":payment_qs.debit,"category":payment_qs.category,"source_id":payment_qs.source_id,"source_type":payment_qs.source_type}
        return JsonResponse({"data":"Success","payment":payment}, status = 200)
            
    return JsonResponse({}, status = 400)



def get_loan_details(request):
    
    
    loan_id = int(request.GET.get("loan_id", 0).strip())
    #source_type = request.GET.get("source_type", 0).strip()
     
    print(f"loan_id:{loan_id}")
   

    #21
    if request.is_ajax and request.method == "GET":
        loan_qs = PersonalLoanModel.objects.get(id=loan_id) 
        note_id =0
       # date_entered =get_due_date_string (loan_qs.date_entered)
        loan = {"cc_loan":loan_qs.cc_loan,"saving":loan_qs.saving,"percent":loan_qs.percent,"source_type":loan_qs.source_type,"date_entered":loan_qs.date_entered}
        note_id = loan_qs.note_id
        if note_id > 0:
           note_qs = NoteModel.objects.get(id=note_id)
           print(f"note_qs note:{note_qs.note} ,note_id: {note_id}")
           loan["note"]= note_qs.note
        else:
            loan["note"]= ""
        print("loan:",loan)
        return JsonResponse({"data":"Success","loan":loan}, status = 200)
            
    return JsonResponse({}, status = 400)
def create_or_update_note(loan_id,note,category, loan_note_id = 0):
        #-1 : no-action, 0:edit,1: create
        try:  
             result = NoteModel.objects.filter(source_id = loan_id).update(note=note,category=category)
             print(f"...updating notes notes_id:")
             if result > 0:
                if loan_note_id == 0:
                    note_qs =NoteModel.objects.get(source_id=loan_id)
                    note_id =note_qs.id
                else:
                    note_id = -1
                return {"action":0,"result":result,"note_id":note_id} 
        except Exception as e:
            print(f"...result notes:")
            print (f"{e}, {type(e)}")
            return {"action": -1}
        # create new record
        if result <= 0:
            note_qs = NoteModel(source_id = loan_id ,category=category ,note = note  )
            note_qs.save() 
            print(f"...writing notes notes_id:")
            return {"action":1,"note_id":note_qs.id} 
        #return JsonResponse({}, status = 400) 
        return {"action": -1}

def reset_show_password(request):
    # note: the member_id in tmppassword should have no repition
    member_id = int(request.GET.get("member_id", 0).strip())
    request_action = request.GET.get("request_action", "").strip()
    print(f"member_id: {member_id} , request_action: {request_action} ")
    pwd = ""
    if request.is_ajax and request.method == "GET":
           
            if request_action =="show":
                try:
                    pwd = Tmp_PasswordModel.objects.get(member_id = member_id).pwd
                    pwd = base64.b64decode(pwd)
                    pwd =pwd.decode("utf-8")
                    print (f"....pwd: {pwd}")
                except Exception as e:
                    print (f"{e}, {type(e)}")

            else: # reset action
                print(f".....request_action: {request_action}, id:{member_id}" )
                newPassword = gen_password()
                #fields = {"password":newPassword}
                user = False
                try:
                    user = MemberModel.objects.get(id = member_id).user
                    print("user name:",user.username)
                except  Exception as e:
                    print (f"{e}, {type(e)}")
                if user:
                    pwd = newPassword
                    qs = User.objects.get(username= user.username)
                    qs.set_password(newPassword)
                    qs.save()
                    #result = User.objects.filter(id = user.id).update(password ="5010" )# **fields)
                    #print(f"...qs:",qs)
                    try:
                        
                       newPassword = newPassword.encode("utf-8")
                       encoded = base64.b64encode(newPassword).decode("utf-8")
                       result = Tmp_PasswordModel.objects.filter(member_id =member_id).update( pwd = encoded,qrcode_pwd =encoded)
                       print(f"...result tmp password saving:",result)
                       if result <=0:
                          res = Tmp_PasswordModel.objects.create(member_id= member_id, pwd = encoded)
                         
                    except Exception as e:
                        print (f"{e}, {type(e)}")
                        print("Something happened during saving data to Tmp_Password.")
                        pwd=""
                        

                        
                    
                else:
                    print("unable to reset password!")
            if pwd != "":
                   return JsonResponse({"data":"Success","pass":pwd}, status = 200)
        #return JsonResponse({"data":"Success","pass":pwd}, status = 200) #todo remove False use var
    return JsonResponse({}, status = 400)

   #user = User.objects.create_user( newUsername, email = None,password= newPassword)
   #pwd = Tmp_Password.objects.create(user_id= id, pwd = newPassword )


#2
def update_transfer_status(request):

    if request.is_ajax and request.method == "GET":
        #id of the  sender and receiver are needed bcoz is already in the cashtransfer table sender_id, receiver_id
        id = int(request.GET.get("code", 0))
        request_action = request.GET.get("request_action", "").strip().upper()
        print("....request_action:",request_action)
        try:
            transfer_qs = TransferModel.objects.get(id = id)
            model_list= {"W":"WalletModel","S":"SavingModel","C":"CcModel"}
            model_name =model_list.get(transfer_qs.source_type).lower()
            Model = apps.get_model('fx', model_name)
            print(f"model_name: {model_name}")
            if  request_action == "CANCEL":
                field_value = "C"
            elif  request_action == "REJECT":
                field_value = "R"
            else:   #For ACCEPT
                description ="Transfer (Cash In)"
                member_id =transfer_qs.receiver_id
                field_value ="A"

            fields ={"status":field_value,"date_accounted":date.today()}
            # fields["source_id"] = 0
            # print(f".....fields:{fields}")
            # return
            date_entered = date.today()
            
            if  request_action == "CANCEL" or request_action == "REJECT":
                success = True
                try:
                    account_qs = Model.objects.get(id=transfer_qs.source_id).delete()
                    fields["source_id"] = 0  # so that it does nt require edit button
                    print(f"account_qs:{account_qs}")
                    print("...deleted...")
                except  Exception as e:
                    success =False
                    print (f"{e}, {type(e)}")
                    
                 
                
            elif  request_action == "ACCEPT":
                    debit = 0
                    credit = transfer_qs.amount
                    transType ='D' #deposit
                    category = 1 # means transfer
                    success = True
                    try:
                        account_qs = Model(source_id =transfer_qs.id ,date_entered=date_entered,transaction_type=transType ,description=description,credit=credit,debit=debit ,member_id=member_id,category=category)
                        account_qs.save()  #todo now {uncomment}    #add19
                        
                        print(f"accepted.....")
                    except Exception as e:       #add this new lines jul-23
                        print (f"{e}, {type(e)}")
                        success = False  #todo add logger
                        print(f"..Error saving to {model_name} at def update_transfer_status: ")
            if success:
                    print(f"fields :{fields}")
                    result= TransferModel.objects.filter(id =id).update( **fields)
                    #result = 1    #add19
            else:
                print("success is false:")
            if result <= 0: #not update
                    print(".......failed update.")
                    return JsonResponse({}, status = 400)


        except Exception as e:
            print (f"{e}, {type(e)}")
            print(".......failed update. at try...except")
            return JsonResponse({}, status = 400) #todo
         
        return JsonResponse({"data":"Success"}, status = 200) #todo remove False use var
    return JsonResponse({}, status = 400)

#1
def Transfer_check_balance(request):
    if request.is_ajax and request.method == "GET":
        total_amount = int(request.GET.get("total_amount", ""))
        sender =int(request.GET.get("sender", ""))
        try:
           # WalletTransaction_Qs= WalletTransaction.objects.get(member_id = sender)
            wallet_running_balance = get_running_finance_balance("wallet","member_id",sender)["running_balance"]  # todo i added sender
            balance_long = wallet_running_balance
            balance_short= abbrNum(wallet_running_balance,2) 
        except  Exception as e:
            balance_long =0
        balance ={"balance_long":balance_long,"balance_short":balance_short}
        print("balance",balance)
        if total_amount > balance_long:
            exceed = True
        else:
            exceed =False


        print(f"...total_amount:{total_amount}, sender:{sender}")
        # print(f"....at views sender balance:{balance_long}")
        
         
        return JsonResponse({"balance":balance_long,"exceed":exceed}, status = 200) #todo remove False use var
    return JsonResponse({}, status = 400)






def get_cash_on_hand_balance():
    qs_deposit = WalletModel.objects.filter(transaction_type ='D').aggregate(total_deposit=Sum('credit'))
    qs_withdrawal = WalletModel.objects.filter(transaction_type ='W').aggregate(total_withdrawal=Sum('debit'))
    if not qs_deposit['total_deposit']:
        qs_deposit['total_deposit'] =0
    if not qs_withdrawal['total_withdrawal']:
        qs_withdrawal['total_withdrawal']=0
    print(f"qs_deposit:{qs_deposit}, qs_withdrawal:{qs_withdrawal}")
    cash_on_hand_balance = qs_deposit['total_deposit']  - qs_withdrawal['total_withdrawal'] 
    cash_on_hand_balance  =round(cash_on_hand_balance, 4)
    print(f".....cash_on_hand_balance:{cash_on_hand_balance} ")

    return {'cash_on_hand_balance':cash_on_hand_balance,'cash_in':qs_deposit['total_deposit'],'cash_out':qs_withdrawal['total_withdrawal'] }

#sr
def search_receiver(request):
    print("search_reciever......>>>")
    if request.is_ajax and request.method == "GET":
        action_request = request.GET.get("action_request", "").strip()
        last_row = total_record =0
        if action_request=="search":  # search first 
            start = 0
        else:           # this is for loading more data, because there 2 ajax in one html page
            last_row = int(request.GET.get("last_row", 0))
            start = last_row 
          
        query= request.GET.get("filter_field_value", "").strip()
        print(f" query: {query}")
           
        total_no_of_row_per_page = int(request.GET.get("total_no_of_row_per_page", 10)) 
        total_record = MemberModel.objects.select_related('user').filter( Q(id__gt=1),Q(firstname__icontains=query)|  Q(lastname__icontains=query) |  Q(user__username__icontains=query)).count()
        print(f" query: {query}, total_record:{total_record}")
        # print(f".....query:{query},action_request: {action_request}")
        # print(f"1. total_record: {total_record}, total_no_of_row_per_page:{total_no_of_row_per_page} ")
        last_page = False
        if len(query) > 0:
                #if   action_request != "search":  #this for loading
                #print(f"......last row: {last_row} ,total_no_of_row_per_page:{total_no_of_row_per_page},total_rec:{total_record}")
                 
                if last_row  + total_no_of_row_per_page  >= total_record:
                    new_total_row = total_record - last_row
                    total_no_of_row_per_page = new_total_row #total_record - last_row
                    last_page = True
                # print(f"query:{query},last_row:{last_row}, start:{start}" )
                # print(f"2. total_record: {total_record}, total_no_of_row_per_page:{total_no_of_row_per_page} ")

           # object_list = Client.objects.select_related('user').filter( Q(id__gt=1),Q(firstname__icontains=query)|  Q(lastname__icontains=query) |  Q(user__username__icontains=query))[start:start + total_no_of_row_per_page] 
        else:
            return JsonResponse({}, status = 200)
        data=[]
        print(f"......last row: {last_row} ,total_no_of_row_per_page:{total_no_of_row_per_page},total_rec:{total_record}")
        print(f"start:{start}:start:{start} + total_no_of_row_per_page:{total_no_of_row_per_page}")
        # start =0
        # total_no_of_row_per_page =3
        qs= MemberModel.objects.select_related('user').filter( Q(id__gt=1),Q(firstname__icontains=query)| Q(lastname__icontains=query) |  Q(user__username__icontains=query))[start:start + total_no_of_row_per_page] #   .iterator():
        print(f"qs:{qs}")
        
        for row in qs:
           row ={"id":row.id,"gender":row.gender,"firstname":row.firstname,"lastname":row.lastname,"address":row.address,"telephone":row.telephone,"username":row.member_id}
           data.append(row)
          
           #print("...row:",row)
        properties ={"total_record":total_record}
        return JsonResponse({"data":data,"last_page":last_page,"properties":properties}, status = 200) #todo remove False use var
    return JsonResponse({}, status = 400)
#wmd /123
def finance_load_more(request):
    if request.is_ajax and request.method == "GET":

        properties = {}
        for key,value in request.GET.items(): 
                properties[key] = value
        #print(f"properties: {properties}")
        total_no_of_row=  request.GET.get("total_no_of_row", 1)  #todo replace with (int)
        last_row = request.GET.get("last_row", 1)
       # wallet_transaction_id = request.GET.get("value",1)
        filter_field_value = request.GET.get("filter_field_value",3)
        filter_field = request.GET.get("filter_field",3)
        print(f"....init....last row: {last_row} , total_no_of_row:{total_no_of_row}, ,wallet_transaction_id:{filter_field_value}")

        model_name =  request.GET.get("model").strip().lower()
        model_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel"}
        model_name =model_list.get(model_name).lower()
        Model = apps.get_model('fx', model_name)
        filter_dict = {filter_field: filter_field_value}
        
        total_rows = Model.objects.filter( **filter_dict ).count()
        print(f".........model_name: {model_name}, last row: {last_row} , total_no_of_row:{total_no_of_row}, total-rows:{total_rows} ,wallet_transaction_id:{filter_field_value}")

        last_page = False
        if int(last_row ) + int(total_no_of_row ) >= total_rows:
                new_total_row = total_rows - int( last_row)
                total_no_of_row = str(new_total_row)
                last_page = True
        #query ='''select "fx_cc"."id","fx_cc"."transaction_type","fx_cc"."description","fx_cc"."credit","fx_cc"."debit", sum("fx_cc"."credit") over (order by "fx_cc"."id" ) - sum("fx_cc"."debit") over (order by "fx_cc"."id")  as balance from "fx_cc" where "fx_cc"."member_id" = {} order by "fx_cc"."id" desc offset {} limit {} '''.format(filter_field_value,last_row,total_no_of_row)
       # model_name =model_name.lower()

        # if model_name=="WalletModel":
        #    query ='''select "fx_wallet"."id","fx_wallet"."category","fx_wallet"."source_id","fx_wallet"."date_entered","fx_wallet"."transaction_type","fx_wallet"."description","fx_wallet"."credit","fx_wallet"."debit", sum("fx_wallet"."credit") over (order by "fx_wallet"."id" ) - sum("fx_wallet"."debit") over (order by "fx_wallet"."id")  as balance from "fx_wallet" where "fx_wallet"."member_id" = {}  order by "fx_wallet"."id" desc offset {} limit {} '''.format(filter_field_value,last_row,total_no_of_row)
        if model_name =="paymentmodel":
            query ='''select "fx_paymentmodel"."id","fx_paymentmodel"."source_id","fx_paymentmodel"."transaction_type","fx_paymentmodel"."credit","fx_paymentmodel"."category","fx_paymentmodel"."debit", sum("fx_paymentmodel"."credit") over (order by "fx_paymentmodel"."id" ) - sum("fx_paymentmodel"."debit") over (order by "fx_paymentmodel"."id")  as balance from "fx_paymentmodel" where "fx_paymentmodel"."member_id" = {} order by "fx_paymentmodel"."id" desc offset {} limit {} '''.format(filter_field_value,last_row,total_no_of_row)
        else:
           query ='''select "fx_model"."id","fx_model"."source_id","fx_model"."date_entered","fx_model"."transaction_type","fx_model"."description","fx_model"."credit","fx_model"."debit", sum("fx_model"."credit") over (order by "fx_model"."id" ) - sum("fx_model"."debit") over (order by "fx_model"."id")  as balance from "fx_model" where "fx_model"."member_id" = {}  order by "fx_model"."id" desc offset {} limit {} '''.format(filter_field_value,last_row,total_no_of_row)
           query = query.replace("_model",f"_{model_name}") 
         #  query ='''select "fx_payment"."id","fx_payment"."source_id","fx_payment"."transaction_type","fx_payment"."credit","fx_payment"."category","fx_payment"."debit", sum("fx_payment"."credit") over (order by "fx_payment"."id" ) - sum("fx_payment"."debit") over (order by "fx_payment"."id")  as balance from "fx_payment" where "fx_payment"."member_id" = {} order by "fx_payment"."id" desc offset {} limit {} '''.format(filter_field_value,last_row,total_no_of_row)
        data=[]
        print(f".......query:{query}")
         
        qs =Model.objects.raw(query)
        description_list={"W":"Payment","D":"Loan Owing"}
         
        for o in qs:
            # if o.category in categories:
            #     edit = False
            # else:
            #     edit =True
            if model_name =="paymentmodel":
               row ={"description":description_list.get(o.transaction_type), "category":o.category,"id":o.id,"source_id":o.source_id,"transaction_type":o.transaction_type,"credit":'{:,.2f}'.format(o.credit),"debit":'{:,.2f}'.format(o.debit),"balance": '{:,.2f}'.format(o.balance),"date":o.date_entered}
            else:
                row ={"category":o.category,"id":o.id,"source_id":o.source_id,"transaction_type":o.transaction_type,"description":o.description,"credit":'{:,.2f}'.format(o.credit),"debit":'{:,.2f}'.format(o.debit),"balance": '{:,.2f}'.format(o.balance),"date":o.date_entered}
            data.append(row)
        #print("...data at views:",data)
        return JsonResponse({"data":data,"last_page":last_page}, status = 200)

    return JsonResponse({}, status = 400)

#11
def Transfer_load_more(request):
    if request.is_ajax and request.method == "GET"  and request.user.is_authenticated is True:
 
        total_no_of_row_per_page= int(  request.GET.get("total_no_of_row_per_page", 5))  # total rows to be displayed
        last_row = int(request.GET.get("last_row", 5))
        filter_field_value = int(request.GET.get("filter_field_value",0))
        filter_field = request.GET.get("filter_field","").strip()
        request_list =  request.GET.get("request_list","").strip()
        filter_dict = request.GET.get('filter_dict','').replace("&#x27;","\"")
    
        filter_dict= json.loads(filter_dict)
      #  print("... .ajax.filter_dict:",filter_dict)
        #filter_dict = {filter_field: filter_field_value}
        if request_list == "transfer-receiver":
            distinct =True
            total_records = TransferModel.objects.select_related('receiver').order_by('receiver_id').distinct('receiver_id').filter( **filter_dict ).count()
        else:
            distinct = False
            total_records = TransferModel.objects.select_related('receiver').order_by('receiver_id').filter( **filter_dict ).count()
          
        if request_list == "claim-transfer":    
            receiver = filter_field_value
            table = TransferReceiver_cls( **filter_dict) #filter_field=filter_field,filter_field_value=receiver)
        else: 
           sender = filter_field_value
           table = TransferReceiver_cls( **filter_dict) 
        last_page = False
      #  print(f"....,(b4)last page:{last_page}, total_no_of_row_per_page: {total_no_of_row_per_page}")
        if last_row  + total_no_of_row_per_page  >= total_records:
                new_total_row = total_records - last_row
                total_no_of_row_per_page = new_total_row
                last_page = True
        table.filter_dict= filter_dict
        table.setData(last_row,last_row + total_no_of_row_per_page,distinct) #   qs[0:Cash_transfer_nos_of_row]
        data=[]
        for row in table.data:
            if request_list == "transfer-receiver":
                row ={"id":row.id,"source_type":row.source_type,"sender_id":row.sender_id,"receiver_id":row.receiver_id,"gender":row.receiver.gender,"firstname":row.receiver.firstname,"lastname":row.receiver.lastname,"address":row.receiver.address,"telephone":row.receiver.telephone}
            elif request_list == "claim-transfer":        
                 row ={"id":row.id,"source_type":row.source_type,"sender_id":row.sender_id,"receiver_id":row.receiver_id,"gender":row.sender.gender,"date_entered":row.date_entered,"firstname":row.sender.firstname,"lastname":row.sender.lastname,"purpose":row.purpose,"amount":'{:,.2f}'.format(row.amount)}
            else:
               row ={"id":row.id,"source_type":row.source_type,"sender_id":row.sender_id,"receiver_id":row.receiver_id,"gender":row.receiver.gender,"firstname":row.receiver.firstname,"lastname":row.receiver.lastname,"purpose":row.purpose,"date_entered":row.date_entered,"amount":'{:,.2f}'.format(row.amount),"status":row.status}
            data.append(row)
        return JsonResponse({"data":data,"last_page":last_page,"properties":{"total_record":total_records}}, status = 200)

    return JsonResponse({}, status = 400)

def  abbrNum(number, decPlaces):
    if number is None:
        return "0"
    print(f"abbrNum(), number: {number} ")
    decPlaces = pow(10,decPlaces)
    abbrev = [ "k", "m", "b", "t" ]
    i = len(abbrev) - 1
    while i >= 0: # first while loop code
            size = pow(10,(i+1)*3)
           
            if size <= number:
                number = round(number*decPlaces/size)/decPlaces 
                print("number:",round(number))
                if((number == 1000) and (i < len(abbrev) - 1)):
                   number = 1
                   i=i + 1
                number =  "{}{}".format(number,abbrev[i])      
                
                return   number.replace('.0k', 'k')
                 
            i=i- 1
    
        
    return number  
def services(request,id):
    print("......services.....")
 
    try:
        member_info = MemberModel.objects.get(user = request.user.id)
    except Exception as e:
        print(f"member_info: {e}")
   # member_info={"id":0}
    try:
               # live = LivePostModel.objects.all().values("status","remarks","customer__member_id").filter(customer_id = id,active =True)

                qs = LivePostModel.objects.all().values("code","id","in_charge","status","remarks","customer__member_id","customer","customer__gender","customer__firstname","customer__lastname").filter( in_charge = id)
    except Exception as e:
               print(f"services: member_info: {e}")

    context={
      "member_info":member_info,
      "data":qs,
    }   
    return render(request, "fx/services.html", context)

@login_required(login_url='/login/')
def dashboard(request):
    #note:  removed tale from context menu
    print("......dashboard.....")
   
    
    class obj:
        pass
    table =obj()
    table.cards=[]
      
     
    # table.cards.append({"name":"Reserve","card_name":"reserve","id":1})
    # table.cards.append({"name":"store","card_name":"store","id":1})
    # table.cards.append({"name":"Cash On Hand","card_name":"COH","id":0})
    # table.template_name = "fx/card_template.html"
    
    member_info={"id":0}
    print(f"dashboard-------------id:{request.user.id}")
    try: 
        member_info["user_id"] = MemberModel.objects.get(user = request.user.id).id
    except Exception as e:
         print("dashboard:error: {e}")
    print(f" member_info.user_id: {member_info}")
    context={
      "member_info":member_info,
    #  "table":table,  
     # "State":{"dashboard":"active"}
    }   
    
    return render(request, "fx/dashboard.html", context)

def dash(request,message):

    return render(request, "fx/pagenotfound.html", {"message":message})

def admin(request):
    print('admin_request')
    
    return redirect("/admin/")
def user_logout_request(request):
    print('logout_request')
    logout(request)
    return redirect("/index/")

def logout_request(request): #venture
    print('logout_request')
    logout(request)
    return redirect("/venture_main_request/")
def staff_logout_request(request): #venture
    print('staff logout_request')
    logout(request)
    return redirect("/venture_main_request/")
    
def venture_main_request(request):
    context={}
    return render(request, "fx/venture/venture_main.html", context)
#.,
def main_page_request(request):
    context={}
    return render(request, "fx/users/index.html", context)
         

#vlr
def venture_login_request(request):
    print("venture_login_request:----------")
    if request.method == 'GET' and request.user.is_authenticated is True and request.user.is_active is True:
        return redirect('/logout/')
    user = None
    nextl = request.GET.get('next')
    print(f"....next:{nextl}")
    nextl = '' if nextl == 'None' or nextl is None or nextl.isspace() else nextl
    if request.method == 'POST':
        form = UserLoginForm( data=request.POST) # remove request =request before data=request.POST  but still valid if not remove
        if form.is_valid(): # valid() is used to get the right error messages and it alreadry authenticates user for username,password
            # the 2 statements are used to dobule check the user permission
            user = form.get_user()
            if user and  user.is_active:
                    login(request, user)
                    if user.is_staff:
                            print("success login in venture. staff")
                            member_info = MemberModel.objects.get(user = request.user.id)
                            return redirect(f'/fx_pos/{member_info.id}/{0}/')
                    else:
                            print("success login in venture")
                             
                            if nextl:
                               print(f"redirect to {nextl}")
                            
                               return redirect(nextl)  
                            else:    
                                member_info = MemberModel.objects.get(user = user.id)
                                print(f"member_info;:{member_info}")
                            # client_info ={'id':client_info.id}  #todo eliminate extra fields
                                return redirect('/user_dashboard/{}'.format(member_info.id)) # without / before user_ django will add /login before /user_
        else:
            print("not valid..")     
            member_info ={} #todo
        return render(request, './registration/venture/venture_login.html', {'form': form,'member_info':member_info})

    form = UserLoginForm()
    return render(request = request,
                    template_name = "./registration/venture/venture_login.html",
                    context={"form":form})
#lr
def login_request(request):
    print("login request:----------")
    if request.method == 'GET' and request.user.is_authenticated is True and request.user.is_active is True:
        return redirect('/staff_logout/')
    user = None
    nextl = request.GET.get('next')
    print(f"....next:{nextl}")
    nextl = '' if nextl == 'None' or nextl is None or nextl.isspace() else nextl
    if request.method == 'POST':
        form = UserLoginForm( data=request.POST) # remove request =request before data=request.POST  but still valid if not remove
        if form.is_valid(): # valid() is used to get the right error messages and it alreadry authenticates user for username,password
            # the 2 statements are used to dobule check the user permission
            user = form.get_user()
            if user and  user.is_active:
                login(request, user)
                if user.is_staff:
                     print(f".....nextl:{nextl}")
                     if nextl:
                          if "venture_main_request" in nextl:
                             return redirect(nextl)  
                     return redirect('/dashboard/')
                else:
                    if nextl:
                      return redirect(nextl)  
                    else:    
                        member_info = MemberModel.objects.get(user = user.id)
                        print(f"member_info:{member_info}")
                       # client_info ={'id':client_info.id}  #todo eliminate extra fields
                        return redirect('/user_dashboard/{}'.format(member_info.id)) # without / before user_ django will add /login before /user_
        else:
            print("not valid..")     
            member_info ={} #todo
        return render(request, './registration/login.html', {'form': form,'member_info':member_info})

    form = UserLoginForm()
    return render(request = request,
                    template_name = "./registration/login.html",
                    context={"form":form})
 

 
 

def venture_login_requestssss(request):
    print("login request:----------")
    if request.method == 'GET' and request.user.is_authenticated is True and request.user.is_active is True:
        return redirect('/logouts/')
    user = None
    nextl = request.GET.get('next')
    print(f"....next:{nextl}")
    nextl = '' if nextl == 'None' or nextl is None or nextl.isspace() else nextl
    if request.method == 'POST':
        form = UserLoginForm( data=request.POST) # remove request =request before data=request.POST  but still valid if not remove
        if form.is_valid(): # valid() is used to get the right error messages and it alreadry authenticates user for username,password
            # the 2 statements are used to dobule check the user permission
            user = form.get_user()
            if user and  user.is_active:
                login(request, user)
                if user.is_staff:

                  return redirect('/dashboard/')
                else:
                    if nextl:
                      return redirect(nextl)  
                    else:    
                        member_info = MemberModel.objects.get(user = user.id)
                        print(f"member_info:{member_info}")
                       # client_info ={'id':client_info.id}  #todo eliminate extra fields
                        return redirect('/user_dashboard/{}'.format(member_info.id)) # without / before user_ django will add /login before /user_
        else:
            print("not valid..")     
            member_info ={} #todo
        return render(request, './registration/login.html', {'form': form,'member_info':member_info})

    form = UserLoginForm()
    return render(request = request,
                    template_name = "./registration/login.html",
                    context={"form":form})
 

 
def unauthorized_user(request):
     
         print(" id and request id   is not same.")
         context ={'message':" Sorry. This  page is for authorized user only. Thank you."}
         return render(request, "fx/messages/unauthorized_user.html", context) 
 

 
def my_home_page(request):
         print("initiating home page")
         context ={'message':" Welcome to Fair Exchange!"}
         #deleteModel=LivePostModel.objects.get(in_charge_id = 6).delete()
         
        # return render(request, "fx/underconstruction.html",context) 
         #return render(request, "fx/users/main/member-page.html",context)
        #  items = dayTransactionModel.objects.filter(date_entered__lte=datetime.today(), date_entered__gt=datetime.today()-timedelta(days=7), customer = 2)   #.values('createdate').annotate(count=Count('id'))
        #  print(f"items: {items}")
        #  return
        
        #  try:
        #         delete_source_qs_result = LivePostModel.objects.get(in_charge_id=3).delete() #todo: if delete_source_qs_result <= 0 Success is False
        #         print (f"success..delete_source_qs_result: {delete_source_qs_result}")
        #  except Exception as e:
        #         Success = False
        #         print (f"deleting source: {account_name}, {e}, {type(e)}") 
        
        
        
         return render(request, "fx/users/index.html",context) 
              

    
def create_update_payment_result(request,account_name,id,payment_id,msg):
        print(f"account_name:{account_name}")
        member_info = get_member_info(id,"#create_update_payment_result. 1") #create_update_payment_result. 1
        payment_qs= get_object_or_404(PaymentModel, id=payment_id)
        paymentForm = PaymentForm( instance=payment_qs,prefix="payment")  

        paymentForm.payment_id =payment_id
        paymentForm.account_name = account_name
        print(f"paymentForm.account_name: {paymentForm.account_name}")
        paymentForm.account_name = account_name
        paymentForm.account = {account_name:"selected_account"}
        
        
        loan_details = getLoanPayment(id)
        all_balances= get_all_balances(id)
        max_loan = loan_details["max_loan"]     
        owing_balance = all_balances["loan"]
        percent = loan_details["percent"]
        paid = max_loan - owing_balance
        
        paymentForm.paid = loan_details["max_loan"] - all_balances["loan"] # 200  #remove and below
        paymentForm.max =max_loan
        paymentForm.percent = f"{percent}  %"

        context = { 
                'asset_liabities':get_all_balances(id),
                'post_data':True,
                'member_info':member_info, 
                'payment':paymentForm,
            }
        
        messages.success(request, msg)
        return render(request, 'fx/e_wallet/create_update_payment.html',context)

#cufr

def finance_venture_result(request,account_name,id,account_id,msg):
        model_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel"}
        model_name =model_list.get(account_name).lower()
        Model = apps.get_model('fx', model_name)
        member_info = get_member_info(id,"#create_update_result.1") #create_update_result.1
        account= get_object_or_404(Model, id=account_id)
        #Form = apps.get_form('fx', 'WalletForm')
        if account_name =="wallet":
            accountForm = WalletForm( instance=account,prefix="deposit_withdraw")
           # accountForm.wallet_id =account_id
        else:
            accountForm = SavingForm( instance=account,prefix="deposit_withdraw")
        accountForm.account_id =account_id
        accountForm.account_name = account_name
        accountForm.account = {account_name:"selected_account"}
        accountForm.requested_action = account.transaction_type
        context = { 
                'asset_liabities':get_all_balances(id),
                'post_data':True,
                'member_info':member_info, 
                'account':accountForm,
            }
        
        messages.success(request, msg)
        return render(request, 'fx/venture/finance.html',context)

#cuf
def finance_venture(request,account_name,member_id,account_id,transType):
        transType_description= {'D': 'Cash In', 'W': 'Cash out' }[transType] 
        model_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel"}
        model_name =model_list.get(account_name).lower()
        Model = apps.get_model('fx', model_name)
        member_info = get_member_info(member_id,"# create_update_member_finance.1") # create_update_member_finance.1
        
        running_balance = 0
        running_balance = get_running_finance_balance(account_name,"member_id",member_id)["running_balance"]
        #         No_Transaction_Yet = False
        # except  WalletTransaction.DoesNotExist:
        #         running_balance =0
        amount =0
        if request.method == 'POST':
                print(f"......... past request.method == 'POST':")
                valid =True 
                if transType == 'W': 
                        if account_id == 0:
                            temp_balance = running_balance
                            amount= request.POST.get("deposit_withdraw-debit")
                        else:
                            wallet=Model.objects.get(id=account_id)  #todo try:
                            debit =wallet.debit 
                            temp_balance = running_balance + debit
                            amount= request.POST.get("deposit_withdraw-debit")
                        
                        if  len(amount.strip()) > 0 and float(amount) > temp_balance:
                            valid = False
                            messages.error(request, f"Amount to cash out must not be more than {running_balance}")

                if account_id == 0:   #---------------------  Save New record -----------------------------------
                        print(f"......... if account_id == 0:")
                       # memberTrans = WalletTransaction.objects.get (member_id=id) # add try exception
                        if account_name == "wallet":
                            
                            accountForm = WalletForm(request.POST,prefix="deposit_withdraw")
                           # accountForm.account_id=account_id   # extra field inserted  used in .html
                        else:
                            accountForm = SavingForm(request.POST,prefix="deposit_withdraw")
                        accountForm.account_id=account_id
                        accountForm.account = {account_name:"selected_account"}
                        accountForm.requested_action = transType
                        if valid and accountForm.is_valid():
                                if transType == 'D':
                                    
                                    debit=0
                                    credit=accountForm.cleaned_data['credit']
                                else:  # this withdrawal
                                    debit=accountForm.cleaned_data['debit']
                                    credit =0
                                category = 0 #means normal debit and credit transaction
                                date_entered =accountForm.cleaned_data['date_entered']
                                description =accountForm.cleaned_data['description']
                                #walletTransaction_id = memberTrans.id  
                                account = Model(date_entered=date_entered,transaction_type=transType ,description=description,credit=credit,debit=debit ,member_id=member_id,category=category)
                                account.save()  #todo now {uncomment}
                                source_id = account.id
                                if transType == 'W': 
                                    category = TX_WITHRAWAL
                                    
                                else:
                                   category = TX_DEPOSIT
                                if account_name == "wallet":
                                     account_code = ACCOUNT_WALLET
                                else:
                                     account_code = ACCOUNT_SAVINGS
                                amount = debit + credit
                                saveTransHistory(account_code,request.user.id,member_id,category,source_id,amount,NEW_RECORD)
                                print(f"tx money: {transType}")
                                # account = dayTransactionMode((date_entered=date_entered,transaction_type=transType ,description=description,credit=credit,debit=debit ,member_id=member_id,category=category)

                                
                                #print("after saving wallet id:",wallet.id)
                              #  parameters["wallet_id"] = wallet.id
                                
                                msg ="New transaction has been successfully added!"
                                return redirect(f'/success/finance_venture_result/{account_name}/{member_id}/{account.id}/{msg}')
                                #return render(request, 'products/e_wallet/create_update_member_wallet.html',context)
                        else:
                                print("invalid entry...")
                                messages.error(request, 'Please fill the box with red color. Thanks.')
                              #  messages.error(request, 'Error encountered while saving new record!')
                                context = {
                                        'asset_liabities':get_all_balances(member_id),
                                        'member_info':member_info, 
                                        'account': accountForm,
                                }
                                return render(request, 'fx/venture/finance.html', context)
                                
                #--------------------- end of Save New record -----------------------------------
                else: # update existing record in  wallet database


                    
                            #print(f"......... else of if wallet_id == 0: ")
                            account= get_object_or_404(Model, id=account_id)
                            # wallet_transaction_type =  wallet.transaction_type
                            if account_name == "wallet":
                                account_code = ACCOUNT_WALLET # used by savehistory
                                 #accountForm = WalletForm(request.POST,prefix="deposit_withdraw")
                                accountForm = WalletForm(request.POST , instance=account,prefix="deposit_withdraw")
                            else:
                                account_code = ACCOUNT_SAVINGS  # used by savehistory
                                accountForm = SavingForm(request.POST , instance=account,prefix="deposit_withdraw")
                            accountForm.account = {account_name:"selected_account"} #to mark the remaining balance of an account
                            accountForm.account_id=account_id
                            accountForm.requested_action = transType
                            
                             # saving to day transaction
                            if valid and accountForm.is_valid():
                               # print(f"......past <if valid and walletForm.is_valid()>:")
                                account =accountForm.save()
                               
                                
                                # saving to day transaction
                                source_id = account_id
                                if transType == 'W': 
                                    category = WITHRAWAL
                                    amount =account.debit
                                else:
                                    category = DEPOSIT
                                    amount =account.credit
                                
                                if account_name == "wallet":
                                     new_account_code = ACCOUNT_WALLET
                                     
                                else:
                                     new_account_code = ACCOUNT_SAVINGS
                                data = {'amount':amount}
                                saveTransHistory(account_code,0,0,0,source_id,data,EDIT_RECORD)
                                print ("edit savetrans")
                                # endto saving to day transaction
                                context = { 
                                           'asset_liabities':get_all_balances(member_id),
                                            'member_info':member_info, 
                                            'account':accountForm ,  
                                        }
                                msg ="Following record has been successfully updated!"
                                return redirect(f'/success/finance_venture_result/{account_name}/{member_id}/{account.id}/{msg}')
                               # messages.success(request, 'Following record has been successfully updated!.')
                                #return render(request, 'products/e_wallet/create_update_member_wallet.html',context) 
#111
                            else:
                                messages.error(request, 'Please fill the box with red color. Thanks.')

                                print("invalid form.....")
                                
                                context = {
                                        'asset_liabities':get_all_balances(member_id),
                                        'account': accountForm,
                                        'member_info':member_info,
                                        
                                }
                                return render(request, 'fx/venture/finance.html', context)
                                #todo replace with code to go bac to form
                           # return redirect("/display_client_saving/{}".format(client.id))  #todo change to wallet from saving

                    
        else: #  GET: 'else' of if request.method == 'POST': 
                                #---------------------  create New record -----------------------------------
                
                print(f"........ create record reach..")
                if account_id == 0: # add new record
                                # client = get_object_or_404(Client,id=id)
                                    if transType =="W":
                                        debit=""
                                        credit=0
                                    else:
                                        credit=""
                                        debit =0
                                    initial_data ={'debit':debit,'credit':credit, 'transaction_type':transType, 'date_entered': date.today(),'description':transType_description} #note: not for editing data
                                    
                                    if account_name == "wallet":
                                            accountForm = WalletForm(initial =initial_data,prefix="deposit_withdraw")  #--- saving
                                         #   accountForm.account_id=account_id
                                    else:
                                        accountForm = SavingForm(initial =initial_data,prefix="deposit_withdraw")  #--- saving
                                    accountForm.account_id=account_id
                                    accountForm.account = {account_name:"selected_account"}
                                    accountForm.account_name = account_name
                                    accountForm.requested_action = transType
                                    
                                    #1111

                                    # if No_Transaction_Yet:  #   SavingTransaction.DoesNotExist:
                                    #         running_balance = 0
                                    #         qs_wallet_info = WalletTransaction(date_entered=date.today(),member_id=id)
                                    #         qs_wallet_info.save()
                                    print(f"....member_id: {member_info.id}")
                                    context = { 
                                            'asset_liabities':get_all_balances(member_id),
                                            'account': accountForm,
                                            'member_info':member_info,
                                            
                                        }
                                    return render(request, 'fx/venture/finance.html', context)
                                    #---------------------end  Save New record -----------------------------------

                else:  #request a update for existing wallet entry
                    account= get_object_or_404(Model, id=account_id)
                    # wallet_transaction_type =  account.transaction_type
                    if account_name == 'wallet':
                        accountForm = WalletForm( instance=account,prefix ="deposit_withdraw") # instance=saving bcoz editing process, none when new record
                     
                    else:
                        accountForm = SavingForm( instance=account,prefix ="deposit_withdraw") # instance=saving bcoz editing process, none when new record
                    accountForm.account_id=account_id
                    accountForm.account = {account_name:"selected_account"}
                    accountForm.account_name = account_name
                    accountForm.requested_action = transType

                    context = {
                        'asset_liabities':get_all_balances(member_id),
                        'account': accountForm,   
                        'member_info':member_info,
                    }
                    return render(request, 'fx/venture/finance.html', context)




####
def create_update_payment(request,member_id,payment_id):
     member_info = get_member_info(member_id,"#create_update_payment. 1") #create_update_payment. 1
     running_balance = 0
     account_name="cash" #default
     account_name_list={"W":"wallet","S":"saving","K":"cc","C":"cash"}
     all_balances=get_all_balances(member_id)
    
     if request.method == 'POST':
                    
                    valid =True 
                    source_type= request.POST.get("payment-source_type").strip()
                    amount= request.POST.get("payment-debit")
                    if payment_id > 0 :
                        payment_qs= PaymentModel.objects.get(id=payment_id)
                        old_source_type = payment_qs.source_type 
                        old_source_id = payment_qs.source_id
                        old_debit=  payment_qs.debit
                      
                    Model=""
                    source_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel"}
                    if(source_type != 'C'):
                            account_name =account_name_list.get(source_type )
                            running_balance = get_running_finance_balance(account_name,"member_id",member_id)["running_balance"]
                            model_name =source_list.get(account_name).lower()
                            Model = apps.get_model('fx', model_name) 

                           
                            if payment_id == 0:
                                temp_balance = running_balance
                                amount= request.POST.get("payment-debit")
                            else:
                                payment_qs= PaymentModel.objects.get(id=payment_id)  #todo try:
                                debit =payment_qs.debit 
                                temp_balance = running_balance + debit
                                amount= request.POST.get("payment-debit")
                            print(f"...amount:{amount}, temp_balance:{temp_balance}")
                            if  len(amount.strip()) > 0 and float(amount) > temp_balance:
                                valid = False
                                messages.error(request, f"Amount to withdraw must not be more than {running_balance}")
                    else: # C A S H PAID
                       source_id=0

                    credit =0
                    category = 6 #means   payment, 5 for loan
                    description= "Loan Payment"
                    transaction_type="W"
                    date_entered = date.today()    
                  
                    if payment_id ==0:
                            paymentForm = PaymentForm(request.POST,prefix="payment")
                            if valid and paymentForm.is_valid():
                                print("succ")
                                loan_details = getLoanPayment(member_id)
                                max_loan = loan_details["max_loan"]
                                owing_balance = all_balances["loan"]
                                percent = loan_details["percent"]
                                paid = max_loan - owing_balance
                                print(f"percent: {percent}  paid:{paid},max Loan:{max_loan},amount:{amount}, remaining:{owing_balance}")
                                amount = float(amount)
                                
                               
                                
                                
                                
                                debit=paymentForm.cleaned_data['debit']
                                Success = True
                                if source_type != 'C':
                                        try:
                                            account_qs = Model(description=description,date_entered=date_entered,transaction_type=transaction_type ,credit=credit,debit=debit ,member_id=member_id,category=category)
                                            account_qs.save() 
                                            source_id = account_qs.id
                                        except Exception as e:
                                            Success = False
                                            print (f"payment deduction from source: {account_name}, {e}, {type(e)}")
                                #walletTransaction_id = memberTrans.id  
                                print(f".....debit:{debit} ")
                                if Success:
                                    try:
                                            payment_qs = PaymentModel(source_type=source_type,source_id=source_id ,date_entered=date_entered,transaction_type=transaction_type ,credit=credit,debit=debit ,member_id=member_id,category=category)
                                            payment_qs.save()   
                                    except Exception as e:
                                            Success = False
                                            print (f"payment deduction from PaymentModel, {e}, {type(e)}")
                                    if  Success and source_type != 'C': 
                                        try:
                                            account_qs = Model.objects.filter (id = account_qs.id).update( source_id =payment_qs.id)
                                        except Exception as e:
                                            Success = False
                                            print (f"deduction from  source:{account_name}, {e}, {type(e)}")
                                    
                                    if amount == owing_balance:
                                            print(f"amount == owing_balance:{amount == owing_balance}")
                                            additional_loan = max_loan
                                            if  Success:
                                                    try:
                                                        source_type ="M" # additional loan
                                                        payment_additional_qs = PaymentModel(source_type=source_type,source_id = payment_qs.id ,date_entered=date_entered,transaction_type='D' ,credit=additional_loan,debit=0 ,member_id=member_id,category=category)
                                                        payment_additional_qs.save()   
                                                        print(f"success in recording additional loan max:{max_loan}")
                                                    except Exception as e:
                                                        Success = False
                                                        print (f"Error: recording additional loan, {e}, {type(e)}")
                                            if Success:
                                                    try:
                                                             
                                                            description = "Additional Loan"
                                                            category = 5 #loan
                                                            Cc_qs = CcModel(member_id = member_id, date_entered=date.today(),transaction_type='D' ,description=description,credit=additional_loan,debit=0,category=category,source_id = payment_qs.id ) #source_id =loan_qs.id 
                                                            Cc_qs.save() 
                                                            
                                                            print(f"success Additional Loan")
                                                    except Exception as e:
                                                            Success= False
                                                            print (f"error result:{e}, {type(e)}")
                                     
                                    else:
                                        
                                            additional_loan = amount * (percent/100)
                                            print(f" owing_balance:{type(owing_balance)}")
                                            print(f"additonal_loan:{additional_loan}")
                                            try:
                                                source_type ="A" # additional loan
                                                payment_additional_qs = PaymentModel(source_type=source_type,source_id = payment_qs.id ,date_entered=date_entered,transaction_type='D' ,credit=additional_loan,debit=0 ,member_id=member_id,category=category)
                                                payment_additional_qs.save()   
                                                print(f"success in recording additional loan")
                                            except Exception as e:
                                                Success = False
                                                print (f"Error: recording additional loan, {e}, {type(e)}")
                                            if Success:
                                                    try:
                                                            #12-4
                                                            description = "Additional Loan"
                                                            category = 5 #loan
                                                            Cc_qs = CcModel(member_id = member_id, date_entered=date.today(),transaction_type='D' ,description=description,credit=additional_loan,debit=0,category=category,source_id = payment_qs.id ) #source_id =loan_qs.id 
                                                            Cc_qs.save() 
                                                            
                                                            print(f"success Additional Loan")
                                                    except Exception as e:
                                                            Success= False
                                                            print (f"error result:{e}, {type(e)}") 
                                    if Success:
                                        
                                            saveTransHistory(ACCOUNT_PAYMENT,request.user.id,member_id,TX_LOAN_PAYMENT,payment_qs.id,amount,NEW_RECORD)
                                            msg ="New payment has been successfully added!"
                                            return redirect(f'/success/create_update_payment_result/{account_name}/{member_id}/{payment_qs.id}/{msg}')
                                if not Success:
                                        messages.error(request, 'Sorry,Unexpected error has been encountered while saving payment transaction. Thank you.')
                                        #return render(request, 'products/e_wallet/create_update_member_wallet.html',context)
                            else:
                                        print("invalid entry...")
                                        messages.error(request, 'Please fill the box with red color. Thanks.')
                    else:   # E D I T
                            paymentForm = PaymentForm(request.POST , instance=payment_qs,prefix="payment")
                            paymentForm.account = {account_name:"selected_account"} #to mark the remaining balance of an account
                            paymentForm.payment_id = payment_id
                           # paymentForm.requested_action = transType
                            if valid and paymentForm.is_valid():
                                source_id= -1
                                debit = paymentForm.cleaned_data['debit']
                                Success = True
                                print(f"valid....source_type :{source_type}")
                                if source_type != old_source_type:
                                    if old_source_type != 'C':
                                            account_name =account_name_list.get(old_source_type )
                                            model_name =source_list.get(account_name).lower()
                                            Model = apps.get_model('fx', model_name) 
                                            try:
                                                delete_source_qs_result = Model.objects.get(id=old_source_id).delete() #todo: if delete_source_qs_result <= 0 Success is False
                                                print (f"delete_source_qs_result: {delete_source_qs_result}")
                                            except Exception as e:
                                                Success = False
                                                print (f"deleting source: {account_name}, {e}, {type(e)}")   

                                    if source_type =='C':
                                        source_id =0
                                    else:

                                        
                                        new_account_name =account_name_list.get(source_type )
                                        model_name =source_list.get(new_account_name).lower()
                                        new_Model = apps.get_model('fx', model_name) 
                                        if Success:
                                            try:
                                                
                                                new_source_qs = new_Model(description=description,date_entered=date_entered,transaction_type=transaction_type ,credit=credit,debit=debit ,member_id=member_id,category=category,source_id=payment_id)
                                                new_source_qs.save() 
                                                source_id =new_source_qs.id
                                            except Exception as e:
                                                Success = False
                                                print (f"payment deduction from source: {account_name}, {e}, {type(e)}")   
                                        print(f"Success: {Success}, source_id:{source_id} ,model_name: {model_name}")
                                         
                                else:   # source_type == payment_qs.source_type:  
                                        if source_type != 'C':
                                            model_qs_result= Model.objects.filter(id = old_source_id).update(debit=debit) # Model is already declared under  if(source_type != 'C'): 
                                            print(f"payment_id: {payment_id} model_qs_result:{model_qs_result}")
                                            if model_qs_result <= 0:
                                                Success= False
                                        source_id = -1
                                filter_dict={}
                                if source_id >=0: #   > 0 mean there was a change
                                     filter_dict={"source_id":source_id,"source_type":source_type}
                                if debit != old_debit:
                                    filter_dict["debit"] = debit
                                print(f"success: {Success}....filter_dict: {filter_dict}")
                                if Success and filter_dict:
                                    payment_qs_result= PaymentModel.objects.filter(id = payment_id).update( **filter_dict)
                                    print(f"payment_qs:{payment_qs_result}")
                                    #12-4
                                    
                                    #for max,paid,owing
                                    loan_details = getLoanPayment(member_id)
                                    max_loan = loan_details["max_loan"]
                                    owing_balance = all_balances["loan"]
                                    percent = loan_details["percent"] /100
                                    paid = max_loan - owing_balance 
                                   # partial_payment =amount - ( amount * percent)
                                    #paid = paid - partial_payment
                                    print(f"---------------percent: {percent}  paid:{paid},max Loan:{max_loan},amount:{amount}, remaining:{owing_balance}")
                                    amount = float(amount)
                                    
                                    print(f"------- 1 edit part---- amount == owing_balance:{amount == owing_balance},additonal_")

                                    if amount == owing_balance or amount == max_loan:
                                            additional_loan = max_loan
                                            print(f"-------2  edit part---- amount == owing_balance:{amount == owing_balance},additonal_loan: {additional_loan}")
                                            
                                            if  Success:
                                                    edit = False
                                                    try:
                                                            payment_additional= PaymentModel.objects.get(source_id=payment_qs.id)  #todo try:
                                                            edit = True
                                                           # source_type = payment_additional.source_type 
                                                    except Exception as e:
                                                           print ("Cant read source_type from payment table")
                                                    if edit == False:
                                                            try:
                                                                source_type ="M" # MAx additional loan
                                                                payment_additional_qs = PaymentModel(source_type=source_type,source_id = payment_qs.id ,date_entered=date_entered,transaction_type='D' ,credit=additional_loan,debit=0 ,member_id=member_id,category=category)
                                                                payment_additional_qs.save()   
                                                                #12-5
                                                                print(f"success in recording additional loan max's:{max_loan}")
                                                            except Exception as e:
                                                                Success = False
                                                                print (f"Error: recording additional loan, {e}, {type(e)}")
                                                    else:
                                                            try:
                                                                    payment_qs_result= PaymentModel.objects.filter(source_id = payment_id).update( credit = additional_loan,source_type ="M")
                                                            except Exception as e:
                                                                        Success = False
                                                                        print (f"addition loan at payment table: {e}, {type(e)}") 
                                                            
                                            if Success:
                                                    try:
                                                            #12-4
                                                            description = "Additional Loan"
                                                            category = 5 #loan
                                                            Cc_qs = CcModel(member_id = member_id, date_entered=date.today(),transaction_type='D',description=description,credit=additional_loan,debit=0,category=category,source_id = payment_additional_qs.id ) #source_id =loan_qs.id 
                                                            Cc_qs.save() 
                                                            
                                                            print(f"success Additional Loan to ccmodel")
                                                    except Exception as e:
                                                            Success= False
                                                            print (f"error result:{e}, {type(e)}") 
                                         
                                         
                                         
                                    else:
                                            print("-------------additional loan pass else-----------")
                                            additional_loan = amount * percent
                                            try:
                                                    payment_qs_result= PaymentModel.objects.filter(source_id = payment_id).update( credit = additional_loan,source_type ="A")
                                            except Exception as e:
                                                        Success = False
                                                        print (f"addition loan at payment table: {e}, {type(e)}") 
                                            try:
                                                    cc_qs_result = CcModel.objects.filter(source_id = payment_id).update( credit = additional_loan)
                                            except Exception as e:
                                                        Success = False
                                                        print (f"addition loan at Cc table: {e}, {type(e)}") 
                                                        
                                            
                                    print(f"last. succcess in writing additional loan:additonal_loan:{additional_loan}")
                                    data ={"amount":debit}
                                    saveTransHistory(ACCOUNT_PAYMENT,0,0,0,payment_id,data,EDIT_RECORD)
                                    msg ="New payment has been successfully added!"
                                    return redirect(f'/success/create_update_payment_result/{account_name}/{member_id}/{payment_id}/{msg}')
                                else:
                                    account_name_list={"W":"wallet","S":"saving","K":"cc","C":"loan"}
                                    account_name=account_name_list.get( payment_qs.source_type )
                                    if payment_qs.source_type != 'C':
                                        all_balances[account_name] =round( all_balances[account_name] + payment_qs.debit,2)
                                    all_balances["loan"] = round( all_balances['loan']  + payment_qs.debit,2)
                                    messages.info(request, f"No changes has been detected!")

                            context = {
                                    'asset_liabities':all_balances,
                                    'member_info':member_info, 
                                    'payment': paymentForm,
                            }
                            
                            return render(request, 'fx/e_wallet/create_update_payment.html', context)

     else: #request.method == 'GET':
            loan_details = getLoanPayment(member_id)
            partial_payment = 0
            all_balances= get_all_balances(member_id)
            max_loan = loan_details["max_loan"]
            owing_balance = all_balances["loan"]
            percent = loan_details["percent"]
            print(f"get----owing_balance: {owing_balance} ")
           # paid = max_loan - owing_balance
            per = percent / 100
            if payment_id == 0: # add new record
                    initial_data ={'debit':'', 'credit':0, 'transaction_type':'W', 'date_entered': date.today()} #note: not for editing data
                    paymentForm = PaymentForm(initial =initial_data,prefix="payment")  
                    paymentForm.payment_id=0    #used in make changes btn
                    paymentForm.account = {account_name:"selected_account"}
                    paymentForm.payment_id = payment_id # used date format
                    
                    paid = (loan_details["max_loan"] - all_balances["loan"]) - partial_payment
            else: #payment_id > 0:
                    payment_qs = PaymentModel.objects.get(id=payment_id)
                    paymentForm = PaymentForm(instance=payment_qs,prefix="payment")  
                    account_name = account_name_list.get( payment_qs.source_type )
                    paymentForm.account = {account_name:"selected_account"}
                    paymentForm.account_name = account_name
                    paymentForm.payment_id = payment_id # used date format
                    account_name_list={"W":"wallet","S":"saving","K":"cc","C":"loan"}
                    account_name=account_name_list.get( payment_qs.source_type )
                    print(f"1---balance loan : {all_balances['loan']}")
                    if payment_qs.source_type != 'C':
                         all_balances[account_name] =round( all_balances[account_name] + payment_qs.debit,2)
                         print(f"...payment_qs.source_type != 'C':all_balances[account_name]: {all_balances[account_name]}")
                   
                   # all_balances["loan"] = round( all_balances['loan']  + payment_qs.debit,2)
                    print(f"2---balance loan : {all_balances['loan']}")
                    print(f"payment_qs.source_type: {payment_qs.source_type}")
                    percent = loan_details["percent"]/100
                    
                    
                    try:
                        payment_additional= PaymentModel.objects.get(source_id=payment_qs.id)  #todo try:
                        source_type = payment_additional.source_type 
                    except Exception as e:
                        print ("Cant read source_type from payment table")
                         
                    if  source_type == 'M':
                           paid = max_loan - payment_qs.debit
                           all_balances["loan"] = payment_qs.debit
                           print(f"pass source == M, paid:{paid}, all_balance: {all_balances['loan']}")
                    else:  
                           print(f"1. else, all_balances['loan'] :{all_balances['loan']}")
                           
                           partial_payment = payment_qs.debit - ( payment_qs.debit * percent)
                           all_balances['loan'] = all_balances['loan'] + partial_payment
                           print(f"2. else, all_balances['loan'] :{all_balances['loan']}")
                           paid = (loan_details["max_loan"] - all_balances["loan"]) 
                           print(f"else...paid:{paid}")
                          # all_balances["loan"] =all_balances["loan"] + partial_payment
                           
                    print(f"percent:{percent}, payment_qs.debit: {payment_qs.debit}, partial_payment: {partial_payment}")
                    print(f"paid:, allbalances: {all_balances['loan'] }")
                    
                    
                   
             #12-1
             
            
            
            #partial_payment = payment_qs.debit - ( payment_qs.debit * per)
            print(f"----- partila pay: {partial_payment}, ")
            paymentForm.paid = paid  # 200  #remove and below
            paymentForm.max =max_loan
            paymentForm.percent = f"{percent}  %"
           # all_balances["loan"] =all_balances["loan"] + partial_payment
            
            
            
            print(f"percent: {percent} ,max Loan:{max_loan}, remaining:{owing_balance}")
            
            context = { 
                    'asset_liabities':all_balances,
                    'payment': paymentForm,
                    'member_info':member_info,
                    
                }
            return render(request, 'fx/e_wallet/create_update_payment.html', context)
                                    #---------------------end  Save New record -----------------------------------

        
def payment_venture_result(request,account_name,id,payment_id,msg):
        print(f"account_name:{account_name}")
        member_info = get_member_info(id,"#create_update_payment_result. 1") #create_update_payment_result. 1
        payment_qs= get_object_or_404(PaymentModel, id=payment_id)
        paymentForm = PaymentForm( instance=payment_qs,prefix="payment")  

        paymentForm.payment_id =payment_id
        paymentForm.account_name = account_name
        print(f"paymentForm.account_name: {paymentForm.account_name}")
        paymentForm.account_name = account_name
        paymentForm.account = {account_name:"selected_account"}
        
        
        loan_details = getLoanPayment(id)
        all_balances= get_all_balances(id)
        max_loan = loan_details["max_loan"]     
        owing_balance = all_balances["loan"]
        percent = loan_details["percent"]
        paid = max_loan - owing_balance
        
        paymentForm.paid = loan_details["max_loan"] - all_balances["loan"] # 200  #remove and below
        paymentForm.max =max_loan
        paymentForm.percent = f"{percent}  %"

        context = { 
                'asset_liabities':get_all_balances(id),
                'post_data':True,
                'member_info':member_info, 
                'payment':paymentForm,
            }
        
        messages.success(request, msg)
        return render(request, 'fx/venture/payment.html',context)


####    pv
def payment_venture(request,member_id,payment_id):
     member_info = get_member_info(member_id,"#create_update_payment. 1") #create_update_payment. 1
     running_balance = 0
     account_name="cash" #default
     account_name_list={"W":"wallet","S":"saving","K":"cc","C":"cash"}
     all_balances=get_all_balances(member_id)
    
     if request.method == 'POST':
                    
                    valid =True 
                    source_type= request.POST.get("payment-source_type").strip()
                    amount= request.POST.get("payment-debit")
                    if payment_id > 0 :
                        payment_qs= PaymentModel.objects.get(id=payment_id)
                        old_source_type = payment_qs.source_type 
                        old_source_id = payment_qs.source_id
                        old_debit=  payment_qs.debit
                      
                    Model=""
                    source_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel"}
                    if(source_type != 'C'):
                            account_name =account_name_list.get(source_type )
                            running_balance = get_running_finance_balance(account_name,"member_id",member_id)["running_balance"]
                            model_name =source_list.get(account_name).lower()
                            Model = apps.get_model('fx', model_name) 

                           
                            if payment_id == 0:
                                temp_balance = running_balance
                                amount= request.POST.get("payment-debit")
                            else:
                                payment_qs= PaymentModel.objects.get(id=payment_id)  #todo try:
                                debit =payment_qs.debit 
                                temp_balance = running_balance + debit
                                amount= request.POST.get("payment-debit")
                            print(f"...amount:{amount}, temp_balance:{temp_balance}")
                            if  len(amount.strip()) > 0 and float(amount) > temp_balance:
                                valid = False
                                messages.error(request, f"Amount to withdraw must not be more than {running_balance}")
                    else: # C A S H PAID
                       source_id=0

                    credit =0
                    category = CAT_LOAN #means   payment, 5 for loan
                    description= "Loan Payment"
                    transaction_type="W"
                    date_entered = date.today()    
                  
                    if payment_id ==0:
                            paymentForm = PaymentForm(request.POST,prefix="payment")
                            if valid and paymentForm.is_valid():
                                print("succ")
                                loan_details = getLoanPayment(member_id)
                                max_loan = loan_details["max_loan"]
                                owing_balance = all_balances["loan"]
                                percent = loan_details["percent"]
                                paid = max_loan - owing_balance
                                print(f"percent: {percent}  paid:{paid},max Loan:{max_loan},amount:{amount}, remaining:{owing_balance}")
                                amount = float(amount)
                                
                               
                                
                                
                                
                                debit=paymentForm.cleaned_data['debit']
                                Success = True
                                if source_type != 'C':
                                        try:
                                            account_qs = Model(description=description,date_entered=date_entered,transaction_type=transaction_type ,credit=credit,debit=debit ,member_id=member_id,category=category)
                                            account_qs.save() 
                                            source_id = account_qs.id
                                        except Exception as e:
                                            Success = False
                                            print (f"payment deduction from source: {account_name}, {e}, {type(e)}")
                                #walletTransaction_id = memberTrans.id  
                                print(f".....debit:{debit} ")
                                if Success:
                                    try:
                                            payment_qs = PaymentModel(source_type=source_type,source_id=source_id ,date_entered=date_entered,transaction_type=transaction_type ,credit=credit,debit=debit ,member_id=member_id,category=category)
                                            payment_qs.save()   
                                    except Exception as e:
                                            Success = False
                                            print (f"payment deduction from PaymentModel, {e}, {type(e)}")
                                    if  Success and source_type != 'C': 
                                        try:
                                            account_qs = Model.objects.filter (id = account_qs.id).update( source_id =payment_qs.id)
                                        except Exception as e:
                                            Success = False
                                            print (f"deduction from  source:{account_name}, {e}, {type(e)}")
                                    
                                    if amount == owing_balance:
                                            print(f"amount == owing_balance:{amount == owing_balance}")
                                            additional_loan = max_loan
                                            if  Success:
                                                    try:
                                                        source_type ="M" # additional loan
                                                        payment_additional_qs = PaymentModel(source_type=source_type,source_id = payment_qs.id ,date_entered=date_entered,transaction_type='D' ,credit=additional_loan,debit=0 ,member_id=member_id,category=category)
                                                        payment_additional_qs.save()   
                                                        print(f"success in recording additional loan max:{max_loan}")
                                                    except Exception as e:
                                                        Success = False
                                                        print (f"Error: recording additional loan, {e}, {type(e)}")
                                            if Success:
                                                    try:
                                                             
                                                            description = "Additional Loan"
                                                            category = 5 #loan
                                                            Cc_qs = CcModel(member_id = member_id, date_entered=date.today(),transaction_type='D' ,description=description,credit=additional_loan,debit=0,category=category,source_id = payment_qs.id ) #source_id =loan_qs.id 
                                                            Cc_qs.save() 
                                                            
                                                            print(f"success Additional Loan")
                                                    except Exception as e:
                                                            Success= False
                                                            print (f"error result:{e}, {type(e)}")
                                     
                                    else:
                                        
                                            additional_loan = amount * (percent/100)
                                            print(f" owing_balance:{type(owing_balance)}")
                                            print(f"additonal_loan:{additional_loan}")
                                            try:
                                                source_type ="A" # additional loan
                                                payment_additional_qs = PaymentModel(source_type=source_type,source_id = payment_qs.id ,date_entered=date_entered,transaction_type='D' ,credit=additional_loan,debit=0 ,member_id=member_id,category=category)
                                                payment_additional_qs.save()   
                                                print(f"success in recording additional loan")
                                            except Exception as e:
                                                Success = False
                                                print (f"Error: recording additional loan, {e}, {type(e)}")
                                            if Success:
                                                    try:
                                                            #12-4
                                                            description = "Additional Loan"
                                                            category = 5 #loan
                                                            Cc_qs = CcModel(member_id = member_id, date_entered=date.today(),transaction_type='D' ,description=description,credit=additional_loan,debit=0,category=category,source_id = payment_qs.id ) #source_id =loan_qs.id 
                                                            Cc_qs.save() 
                                                            
                                                            print(f"success Additional Loan")
                                                    except Exception as e:
                                                            Success= False
                                                            print (f"error result:{e}, {type(e)}") 
                                    if Success:
                                        
                                            # save to history
                                            #pv,.
                                             
                                            saveTransHistory(ACCOUNT_PAYMENT,request.user.id,member_id,TX_LOAN_PAYMENT,payment_qs.id,amount,NEW_RECORD)
                                            print ("edit savetrans")
                                            msg ="New payment has been successfully added!"
                                            return redirect(f'/success/payment_venture_result/{account_name}/{member_id}/{payment_qs.id}/{msg}')
                                if not Success:
                                        messages.error(request, 'Sorry,Unexpected error has been encountered while saving payment transaction. Thank you.')
                                        #return render(request, 'products/e_wallet/create_update_member_wallet.html',context)
                            
                            
                            
                            else:
                                        print("invalid entry...")
                                        messages.error(request, 'Please fill the box with red color. Thanks.')
                    else:   # E D I T
                            paymentForm = PaymentForm(request.POST , instance=payment_qs,prefix="payment")
                            paymentForm.account = {account_name:"selected_account"} #to mark the remaining balance of an account
                            paymentForm.payment_id = payment_id
                           # paymentForm.requested_action = transType
                            if valid and paymentForm.is_valid():
                                source_id= -1
                                debit = paymentForm.cleaned_data['debit']
                                Success = True
                                print(f"valid....source_type :{source_type}")
                                if source_type != old_source_type:
                                    if old_source_type != 'C':
                                            account_name =account_name_list.get(old_source_type )
                                            model_name =source_list.get(account_name).lower()
                                            Model = apps.get_model('fx', model_name) 
                                            try:
                                                delete_source_qs_result = Model.objects.get(id=old_source_id).delete() #todo: if delete_source_qs_result <= 0 Success is False
                                                print (f"delete_source_qs_result: {delete_source_qs_result}")
                                            except Exception as e:
                                                Success = False
                                                print (f"deleting source: {account_name}, {e}, {type(e)}")   

                                    if source_type =='C':
                                        source_id =0
                                    else:

                                        
                                        new_account_name =account_name_list.get(source_type )
                                        model_name =source_list.get(new_account_name).lower()
                                        new_Model = apps.get_model('fx', model_name) 
                                        if Success:
                                            try:
                                                
                                                new_source_qs = new_Model(description=description,date_entered=date_entered,transaction_type=transaction_type ,credit=credit,debit=debit ,member_id=member_id,category=category,source_id=payment_id)
                                                new_source_qs.save() 
                                                source_id =new_source_qs.id
                                            except Exception as e:
                                                Success = False
                                                print (f"payment deduction from source: {account_name}, {e}, {type(e)}")   
                                        print(f"Success: {Success}, source_id:{source_id} ,model_name: {model_name}")
                                         
                                else:   # source_type == payment_qs.source_type:  
                                        if source_type != 'C':
                                            model_qs_result= Model.objects.filter(id = old_source_id).update(debit=debit) # Model is already declared under  if(source_type != 'C'): 
                                            print(f"payment_id: {payment_id} model_qs_result:{model_qs_result}")
                                            if model_qs_result <= 0:
                                                Success= False
                                        source_id = -1
                                filter_dict={}
                                if source_id >=0: #   > 0 mean there was a change
                                     filter_dict={"source_id":source_id,"source_type":source_type}
                                if debit != old_debit:
                                    filter_dict["debit"] = debit
                                print(f"success: {Success}....filter_dict: {filter_dict}")
                                if Success and filter_dict:
                                    payment_qs_result= PaymentModel.objects.filter(id = payment_id).update( **filter_dict)
                                    print(f"payment_qs:{payment_qs_result}")
                                
                                    loan_details = getLoanPayment(member_id)
                                    max_loan = loan_details["max_loan"]
                                    owing_balance = all_balances["loan"]
                                    percent = loan_details["percent"] /100
                                    paid = max_loan - owing_balance 
                                   # partial_payment =amount - ( amount * percent)
                                    #paid = paid - partial_payment
                                    print(f"---------------percent: {percent}  paid:{paid},max Loan:{max_loan},amount:{amount}, remaining:{owing_balance}")
                                    amount = float(amount)
                                    
                                    print(f"------- 1 edit part---- amount == owing_balance:{amount == owing_balance},additonal_")

                                    if amount == owing_balance or amount == max_loan:
                                            additional_loan = max_loan
                                            print(f"-------2  edit part---- amount == owing_balance:{amount == owing_balance},additonal_loan: {additional_loan}")
                                            
                                            if  Success:
                                                    edit = False
                                                    try:
                                                            payment_additional= PaymentModel.objects.get(source_id=payment_qs.id)  #todo try:
                                                            edit = True
                                                           # source_type = payment_additional.source_type 
                                                    except Exception as e:
                                                           print ("Cant read source_type from payment table")
                                                    if edit == False:
                                                            try:
                                                                source_type ="M" # MAx additional loan
                                                                payment_additional_qs = PaymentModel(source_type=source_type,source_id = payment_qs.id ,date_entered=date_entered,transaction_type='D' ,credit=additional_loan,debit=0 ,member_id=member_id,category=category)
                                                                payment_additional_qs.save()   
                                                                #12-5
                                                                print(f"success in recording additional loan max's:{max_loan}")
                                                            except Exception as e:
                                                                Success = False
                                                                print (f"Error: recording additional loan, {e}, {type(e)}")
                                                    else:
                                                            try:
                                                                    payment_qs_result= PaymentModel.objects.filter(source_id = payment_id).update( credit = additional_loan,source_type ="M")
                                                            except Exception as e:
                                                                        Success = False
                                                                        print (f"addition loan at payment table: {e}, {type(e)}") 
                                                            
                                            if Success:
                                                    try:
                                                            #12-4
                                                            description = "Additional Loan"
                                                            category = 5 #loan
                                                            Cc_qs = CcModel(member_id = member_id, date_entered=date.today(),transaction_type='D',description=description,credit=additional_loan,debit=0,category=category,source_id = payment_additional_qs.id ) #source_id =loan_qs.id 
                                                            Cc_qs.save() 
                                                            
                                                            print(f"success Additional Loan to ccmodel")
                                                    except Exception as e:
                                                            Success= False
                                                            print (f"error result:{e}, {type(e)}") 
                                         
                                         
                                         
                                    else:
                                            print("-------------additional loan pass else-----------")
                                            additional_loan = amount * percent
                                            try:
                                                    payment_qs_result= PaymentModel.objects.filter(source_id = payment_id).update( credit = additional_loan,source_type ="A")
                                            except Exception as e:
                                                        Success = False
                                                        print (f"addition loan at payment table: {e}, {type(e)}") 
                                            try:
                                                    cc_qs_result = CcModel.objects.filter(source_id = payment_id).update( credit = additional_loan)
                                            except Exception as e:
                                                        Success = False
                                                        print (f"addition loan at Cc table: {e}, {type(e)}") 
                                                        
                                            
                                    print(f"last. succcess in writing additional loan:additonal_loan:{additional_loan}")
                                    data = {"amount":debit}
                                    saveTransHistory(ACCOUNT_PAYMENT,0,0,0,payment_id,data,EDIT_RECORD)

                                    msg ="New payment has been successfully added!"
                                    return redirect(f'/success/payment_venture_result/{account_name}/{member_id}/{payment_id}/{msg}')
                                else:
                                    account_name_list={"W":"wallet","S":"saving","K":"cc","C":"loan"}
                                    account_name=account_name_list.get( payment_qs.source_type )
                                    if payment_qs.source_type != 'C':
                                        all_balances[account_name] =round( all_balances[account_name] + payment_qs.debit,2)
                                    all_balances["loan"] = round( all_balances['loan']  + payment_qs.debit,2)
                                    messages.info(request, f"No changes has been detected!")

                            context = {
                                    'asset_liabities':all_balances,
                                    'member_info':member_info, 
                                    'payment': paymentForm,
                            }
                            
                            return render(request, 'fx/venture/payment.html', context)

     else: #request.method == 'GET':
            loan_details = getLoanPayment(member_id)
            partial_payment = 0
            all_balances= get_all_balances(member_id)
            max_loan = loan_details["max_loan"]
            owing_balance = all_balances["loan"]
            percent = loan_details["percent"]
            print(f"get----owing_balance: {owing_balance} ")
           # paid = max_loan - owing_balance
            per = percent / 100
            if payment_id == 0: # add new record
                    initial_data ={'debit':'', 'credit':0, 'transaction_type':'W', 'date_entered': date.today()} #note: not for editing data
                    paymentForm = PaymentForm(initial =initial_data,prefix="payment")  
                    paymentForm.payment_id=0    #used in make changes btn
                    paymentForm.account = {account_name:"selected_account"}
                    paymentForm.payment_id = payment_id # used date format
                    
                    paid = (loan_details["max_loan"] - all_balances["loan"]) - partial_payment
            else: #payment_id > 0:
                    payment_qs = PaymentModel.objects.get(id=payment_id)
                    paymentForm = PaymentForm(instance=payment_qs,prefix="payment")  
                    account_name = account_name_list.get( payment_qs.source_type )
                    paymentForm.account = {account_name:"selected_account"}
                    paymentForm.account_name = account_name
                    paymentForm.payment_id = payment_id # used date format
                    account_name_list={"W":"wallet","S":"saving","K":"cc","C":"loan"}
                    account_name=account_name_list.get( payment_qs.source_type )
                    print(f"1---balance loan : {all_balances['loan']}")
                    if payment_qs.source_type != 'C':
                         all_balances[account_name] =round( all_balances[account_name] + payment_qs.debit,2)
                         print(f"...payment_qs.source_type != 'C':all_balances[account_name]: {all_balances[account_name]}")
                   
                   # all_balances["loan"] = round( all_balances['loan']  + payment_qs.debit,2)
                    print(f"2---balance loan : {all_balances['loan']}")
                    print(f"payment_qs.source_type: {payment_qs.source_type}")
                    percent = loan_details["percent"]/100
                    
                    
                    try:
                        payment_additional= PaymentModel.objects.get(source_id=payment_qs.id)  #todo try:
                        source_type = payment_additional.source_type 
                    except Exception as e:
                        print ("Cant read source_type from payment table")
                         
                    if  source_type == 'M':
                           paid = max_loan - payment_qs.debit
                           all_balances["loan"] = payment_qs.debit
                           print(f"pass source == M, paid:{paid}, all_balance: {all_balances['loan']}")
                    else:  
                           print(f"1. else, all_balances['loan'] :{all_balances['loan']}")
                           
                           partial_payment = payment_qs.debit - ( payment_qs.debit * percent)
                           all_balances['loan'] = all_balances['loan'] + partial_payment
                           print(f"2. else, all_balances['loan'] :{all_balances['loan']}")
                           paid = (loan_details["max_loan"] - all_balances["loan"]) 
                           print(f"else...paid:{paid}")
                          # all_balances["loan"] =all_balances["loan"] + partial_payment
                           
                    print(f"percent:{percent}, payment_qs.debit: {payment_qs.debit}, partial_payment: {partial_payment}")
                    print(f"paid:, allbalances: {all_balances['loan'] }")
                    
                    
                   
             #12-1
             
            
            
            #partial_payment = payment_qs.debit - ( payment_qs.debit * per)
            print(f"----- partila pay: {partial_payment}, ")
            paymentForm.paid = paid  # 200  #remove and below
            paymentForm.max =max_loan
            paymentForm.percent = f"{percent}  %"
           # all_balances["loan"] =all_balances["loan"] + partial_payment
            
            
            
            print(f"percent: {percent} ,max Loan:{max_loan}, remaining:{owing_balance}")
            
            context = { 
                    'asset_liabities':all_balances,
                    'payment': paymentForm,
                    'member_info':member_info,
                    
                }
            return render(request, 'fx/venture/payment.html', context)
                                    #---------------------end  Save New record -----------------------------------

        
          
        
def create_update_result(request,account_name,id,account_id,msg):
        model_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel"}
        model_name =model_list.get(account_name).lower()
        Model = apps.get_model('fx', model_name)
        member_info = get_member_info(id,"#create_update_result.1") #create_update_result.1
        account= get_object_or_404(Model, id=account_id)
        #Form = apps.get_form('fx', 'WalletForm')
        if account_name =="wallet":
            accountForm = WalletForm( instance=account,prefix="deposit_withdraw")
           # accountForm.wallet_id =account_id
        else:
            accountForm = SavingForm( instance=account,prefix="deposit_withdraw")
        accountForm.account_id =account_id
        accountForm.account_name = account_name
        accountForm.account = {account_name:"selected_account"}
        accountForm.requested_action = account.transaction_type
        context = { 
                'asset_liabities':get_all_balances(id),
                'post_data':True,
                'member_info':member_info, 
                'account':accountForm,
            }
        
        messages.success(request, msg)
        return render(request, 'fx/e_wallet/create_update_member_finance.html',context)


#4 cuw
def create_update_member_finance(request,account_name,member_id,account_id,transType):
        transType_description= {'D': 'Cash In', 'W': 'Cash out' }[transType] 
        model_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel"}
        model_name =model_list.get(account_name).lower()
        Model = apps.get_model('fx', model_name)
        member_info = get_member_info(member_id,"# create_update_member_finance.1") # create_update_member_finance.1
        
        running_balance = 0
        running_balance = get_running_finance_balance(account_name,"member_id",member_id)["running_balance"]
        #         No_Transaction_Yet = False
        # except  WalletTransaction.DoesNotExist:
        #         running_balance =0
          
        if request.method == 'POST':
                print(f"......... past request.method == 'POST':")
                valid =True 
                if transType == 'W': 
                        if account_id == 0:
                            temp_balance = running_balance
                            amount= request.POST.get("deposit_withdraw-debit")
                        else:
                            wallet=Model.objects.get(id=account_id)  #todo try:
                            debit =wallet.debit 
                            temp_balance = running_balance + debit
                            amount= request.POST.get("deposit_withdraw-debit")
                        
                        if  len(amount.strip()) > 0 and float(amount) > temp_balance:
                            valid = False
                            messages.error(request, f"Amount to cash out must not be more than {running_balance}")

                if account_id == 0:   #---------------------  Save New record -----------------------------------
                        print(f"......... if account_id == 0:")
                       # memberTrans = WalletTransaction.objects.get (member_id=id) # add try exception
                        if account_name == "wallet":
                            accountForm = WalletForm(request.POST,prefix="deposit_withdraw")
                           # accountForm.account_id=account_id   # extra field inserted  used in .html
                        else:
                            accountForm = SavingForm(request.POST,prefix="deposit_withdraw")
                        accountForm.account_id=account_id
                        accountForm.account = {account_name:"selected_account"}
                        accountForm.requested_action = transType
                        if valid and accountForm.is_valid():
                                if transType == 'D':
                                    debit=0
                                    credit=accountForm.cleaned_data['credit']
                                else:  # this withdrawal
                                    debit=accountForm.cleaned_data['debit']
                                    credit =0
                                category = 0 #means normal debit and credit transaction
                                date_entered =accountForm.cleaned_data['date_entered']
                                description =accountForm.cleaned_data['description']
                                #walletTransaction_id = memberTrans.id  
                                account = Model(date_entered=date_entered,transaction_type=transType ,description=description,credit=credit,debit=debit ,member_id=member_id,category=category)
                                account.save()  #todo now {uncomment}
                                
                                
                                source_id = account.id
                                if transType == 'W': 
                                    category = TX_WITHRAWAL
                                    
                                else:
                                   category = TX_DEPOSIT
                                if account_name == "wallet":
                                     account_code = ACCOUNT_WALLET
                                else:
                                     account_code = ACCOUNT_SAVINGS
                                amount = debit + credit
                                saveTransHistory(account_code,request.user.id,member_id,category,source_id,amount,NEW_RECORD)
                                print(f"tx money: {transType}")
                                
                                #print("after saving wallet id:",wallet.id)
                              #  parameters["wallet_id"] = wallet.id
                                
                                msg ="New transaction has been successfully added!"
                                return redirect(f'/success/create_update_result/{account_name}/{member_id}/{account.id}/{msg}')
                                #return render(request, 'products/e_wallet/create_update_member_wallet.html',context)
                        else:
                                print("invalid entry...")
                                messages.error(request, 'Please fill the box with red color. Thanks.')
                              #  messages.error(request, 'Error encountered while saving new record!')
                                context = {
                                        'asset_liabities':get_all_balances(member_id),
                                        'member_info':member_info, 
                                        'account': accountForm,
                                }
                                return render(request, 'fx/e_wallet/create_update_member_finance.html', context)
                                
                #--------------------- end of Save New record -----------------------------------
                else: # update existing record in  wallet database


                            #print(f"......... else of if wallet_id == 0: ")
                            account= get_object_or_404(Model, id=account_id)
                            # wallet_transaction_type =  wallet.transaction_type
                            if account_name == "wallet":
                                account_code = ACCOUNT_WALLET # used by savehistory

                                 #accountForm = WalletForm(request.POST,prefix="deposit_withdraw")
                                accountForm = WalletForm(request.POST , instance=account,prefix="deposit_withdraw")
                            else:
                                account_code = ACCOUNT_SAVINGS  # used by savehistory
                                accountForm = SavingForm(request.POST , instance=account,prefix="deposit_withdraw")
                            accountForm.account = {account_name:"selected_account"} #to mark the remaining balance of an account
                            accountForm.account_id=account_id
                            accountForm.requested_action = transType
                            if valid and accountForm.is_valid():
                               # print(f"......past <if valid and walletForm.is_valid()>:")
                                account =accountForm.save()
                                source_id = account_id
                                if transType == 'W': 
                                    category = WITHRAWAL
                                    amount =account.debit
                                else:
                                    category = DEPOSIT
                                    amount =account.credit
                                
                                if account_name == "wallet":
                                     new_account_code = ACCOUNT_WALLET
                                     
                                else:
                                     new_account_code = ACCOUNT_SAVINGS
                                data = {'amount':amount}
                                saveTransHistory(account_code,0,0,0,source_id,data,EDIT_RECORD)
                                print ("edit savetrans")
                                context = { 
                                           'asset_liabities':get_all_balances(member_id),
                                            'member_info':member_info, 
                                            'account':accountForm ,  
                                        }
                                msg ="Following record has been successfully updated!"
                                return redirect(f'/success/create_update_result/{account_name}/{member_id}/{account.id}/{msg}')
                               # messages.success(request, 'Following record has been successfully updated!.')
                                #return render(request, 'products/e_wallet/create_update_member_wallet.html',context) 
#111
                            else:
                                messages.error(request, 'Please fill the box with red color. Thanks.')

                                print("invalid form.....")
                                
                                context = {
                                        'asset_liabities':get_all_balances(member_id),
                                        'account': accountForm,
                                        'member_info':member_info,
                                        
                                }
                                return render(request, 'fx/e_wallet/create_update_member_finance.html', context)
                                #todo replace with code to go bac to form
                           # return redirect("/display_client_saving/{}".format(client.id))  #todo change to wallet from saving

                    
        else: #  GET: 'else' of if request.method == 'POST': 
                                #---------------------  create New record -----------------------------------
                
                print(f"........ create record reach..")
                if account_id == 0: # add new record
                                # client = get_object_or_404(Client,id=id)
                                    if transType =="W":
                                        debit=""
                                        credit=0
                                    else:
                                        credit=""
                                        debit =0
                                    initial_data ={'debit':debit,'credit':credit, 'transaction_type':transType, 'date_entered': date.today(),'description':transType_description} #note: not for editing data
                                    
                                    if account_name == "wallet":
                                            accountForm = WalletForm(initial =initial_data,prefix="deposit_withdraw")  #--- saving
                                         #   accountForm.account_id=account_id
                                    else:
                                        accountForm = SavingForm(initial =initial_data,prefix="deposit_withdraw")  #--- saving
                                    accountForm.account_id=account_id
                                    accountForm.account = {account_name:"selected_account"}
                                    accountForm.account_name = account_name
                                    accountForm.requested_action = transType
                                    
                                    #1111

                                    # if No_Transaction_Yet:  #   SavingTransaction.DoesNotExist:
                                    #         running_balance = 0
                                    #         qs_wallet_info = WalletTransaction(date_entered=date.today(),member_id=id)
                                    #         qs_wallet_info.save()
                                    print(f"....member_id: {member_info.id}")
                                    context = { 
                                            'asset_liabities':get_all_balances(member_id),
                                            'account': accountForm,
                                            'member_info':member_info,
                                            
                                        }
                                    return render(request, 'fx/e_wallet/create_update_member_finance.html', context)
                                    #---------------------end  Save New record -----------------------------------

                else:  #request a update for existing wallet entry
                    account= get_object_or_404(Model, id=account_id)
                    # wallet_transaction_type =  account.transaction_type
                    if account_name == 'wallet':
                        accountForm = WalletForm( instance=account,prefix ="deposit_withdraw") # instance=saving bcoz editing process, none when new record
                     
                    else:
                        accountForm = SavingForm( instance=account,prefix ="deposit_withdraw") # instance=saving bcoz editing process, none when new record
                    accountForm.account_id=account_id
                    accountForm.account = {account_name:"selected_account"}
                    accountForm.account_name = account_name
                    accountForm.requested_action = transType

                    context = {
                        'asset_liabities':get_all_balances(member_id),
                        'account': accountForm,   
                        'member_info':member_info,
                    }
                    return render(request, 'fx/e_wallet/create_update_member_finance.html', context)

 








def get_running_finance_balance(model,filter_field, filter_field_value):
       #Add try exception inside this function'''
        
        model_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel","credit_limit":"CreditLineModel"}
        transaction_balance={}
        
        
        if model == "credit_limit":
            print("-------------credit limit--------------")
            qs_deposit= CreditLineModel.objects.filter( member_id = filter_field_value)
            transaction_details_deposit=  qs_deposit.aggregate(total_line_of_credit=Sum('amount'))
            transaction_balance['running_balance']=transaction_details_deposit['total_line_of_credit']
            if  transaction_balance['running_balance'] == None:
                  transaction_balance['running_balance'] =0
                  print(f"----------------- total_line_of_credit: {type(transaction_balance['running_balance'])}")
            
            return transaction_balance
        else:
             print("------------ not--credit limit--------------")
              
        #       transaction_balance['total_withdrawal'] =transaction_details_withdrawal
        model =model_list.get(model).lower()
       
        filter_dict = {filter_field: filter_field_value}
        Model = apps.get_model('fx', model)
        
        # if model == "credit_limit":
              
        #       transaction_balance['total_withdrawal'] =transaction_details_withdrawal
        #       return transaction_balance
        #total_rows = Model.objects.filter( **filter_dict ).count()
        #qs_deposit= clientQs.wallet_set.filter(transaction_type ='D')
        qs_deposit= Model.objects.filter( **filter_dict,transaction_type ='D')
        if qs_deposit.exists():
            transaction_details_deposit=  qs_deposit.aggregate(total_deposit=Sum('credit'))
            transaction_details_deposit= transaction_details_deposit['total_deposit'] 
            transaction_balance['total_deposit'] =transaction_details_deposit
        else:
            transaction_details_deposit = 0
        #qs_withdrawal=clientQs.wallet_set.filter(transaction_type ='W') #todo count instead and retrieve debit field only as as above
        qs_withdrawal=Model.objects.filter( **filter_dict,transaction_type ='W') 
        if  qs_withdrawal.exists():
            transaction_details_withdrawal=qs_withdrawal.aggregate(total_withdrawal=Sum('debit'))
            #ransaction_details_withdrawal=  clientQs.saving_set.filter(transaction_type ='W').aggregate(total_withdrawal=Sum('amount'))
            transaction_details_withdrawal= transaction_details_withdrawal['total_withdrawal']  
            transaction_balance['total_withdrawal'] =transaction_details_withdrawal
        else:
                transaction_details_withdrawal = 0
       # print(f"model:{ model},transaction_details_deposit:{transaction_details_deposit},transaction_details_withdrawal:{transaction_details_withdrawal}")
        transaction_balance['running_balance'] = transaction_details_deposit - transaction_details_withdrawal
        return  transaction_balance  



#uup
def update_user_preference(request):
    
    if request.is_ajax and request.method == "GET":
        
         
        try:
            field_to_update = request.GET.get("field_to_update").strip().lower()

            model_list= {"wallet":"financial_transaction","saving":"financial_transaction","cc":"financial_transaction","payment":"financial_transaction","loan":"financial_transaction"}
          #  print(f"...get_running_finance_balance:model:{model}")
            temp_field_to_update =model_list.get(field_to_update)
            if  temp_field_to_update:
                field_to_update =temp_field_to_update


            field_value = int( request.GET.get("field_value"))
            fields ={field_to_update:field_value}
            print(f"...fields:{fields}")
            
            result= UserPreferenceModel.objects.filter(user = request.user.id).update( **fields)
            if result <= 0: #not update
                fields ={"user_id": request.user.id,field_to_update:field_value}
                qs =UserPreferenceModel( **fields) #add new preference
                qs.save()
                print(".....adding record to pref is success")

            return JsonResponse({"data":"Success"}, status = 200)
        except UserPreferenceModel.DoesNotExist:
           print ("Create new record..")
           return JsonResponse({}, status = 400)

        

    return JsonResponse({}, status = 400)


def get_user_preference(current_user_id):
    default = 5
    try: 
        userPreference_qs =  UserPreferenceModel.objects.get(user_id = current_user_id)
       
        return  userPreference_qs
       
     
    except Exception as e:
        
        print (f"reading user preference {e}, {type(e)}")
        userPreference_qs = UserPreferenceModel(user_id =current_user_id)
        userPreference_qs.save()
      #  return {"wallet_transaction":default,"cash_transfer_nos_of_row":default,"search_member":default,"transfer_receiver":default,"transfer_history":default,"claim_transfer":default}   
 
        return userPreference_qs
# def delete_member(request,id):

#     # note : save all records before deleting Client,Saving.Loan
#     member = Member.objects.get(id=id)
     
#     if request.method == "POST":
#         member.delete()
#         return redirect("../../member/{}".format(id))

#     context =  {
#               'member': member 
#               }

#     return render(request, 'fx/delete_member_template.html', context)


 
    
# def get_member_info(req,id):
#     try:
#        member_info  = MemberModel.objects.get(id =id) 
#        username = User.objects.get(id= member_info.user_id) #todo add separate except
#        member_info.username = username
#     except  MemberModel.DoesNotExist:
                
#                context ={'message':" Sorry. This user does not exist. Thank you."}
#                return render(req, "fx/messages/pagenotfound.html", context) 
#     return member_info


#dmi
def display_member_info(request, id):
        print(f"f....date{datetime.today()}")
        member_info  = get_member_info(id,"#display_member_info. 1") # todo add try...exception here   #display_member_info. 1
        preference = get_user_preference(request.user.id)  #todo use the staff preference not the user
        wallet_detail ="" #WalletModel.objects.raw('''select "fx_walletmodel"."id","fx_walletmodel"."transaction_type","fx_walletmodel"."description","fx_walletmodel"."credit","fx_walletmodel"."debit", sum("fx_walletmodel"."credit") over (order by "fx_walletmodel"."id" ) - sum("fx_walletmodel"."debit") over (order by "fx_walletmodel"."id")  as balance from "fx_walletmodel" where "fx_walletmodel"."member_id" = {}  order by "fx_walletmodel"."id" desc   limit {}'''.format(member_info.id, preference.financial_transaction))
        total_rows = WalletModel.objects.filter(member_id =member_info.id).count()
        wallet_transaction = myTable(data=wallet_detail,filter_field= "member_id",filter_field_value= member_info.id,total_rows=total_rows,user_prefered_nos_rows=preference.financial_transaction,model= 'wallet')
        wallet_transaction.member_id = member_info.id
        wallet_transaction.user_preference = preference
        wallet_transaction.data =""
        wallet_transaction.category={"regular_transaction":True}
        wallet_transaction.button_info ="Info"
        wallet_transaction.button_edit ="Edit"
        # ---------- cc
        preference = get_user_preference(request.user.id)  #todo use the staff preference not the user
        Cc_detail =""#CcModel.objects.raw('''select "fx_cc"."id","fx_cc"."transaction_type","fx_cc"."description","fx_cc"."credit","fx_cc"."debit", sum("fx_cc"."credit") over (order by "fx_cc"."id" ) - sum("fx_cc"."debit") over (order by "fx_cc"."id")  as balance from "fx_cc" where "fx_cc"."member_id" = {} order by "fx_cc"."id" desc  limit {}'''.format(member_info.id, preference.financial_transaction))
        total_rows = CcModel.objects.filter(member_id =member_info.id).count()
        Cc_transaction = myTable(data=Cc_detail,filter_field= "member_id",filter_field_value= member_info.id,total_rows=total_rows,user_prefered_nos_rows=preference.financial_transaction,model= 'cc')
        Cc_transaction.member_id = member_info.id
        Cc_transaction.user_preference = preference
        Cc_transaction.data =""
        Cc_transaction.button_info ="Info"
        #----------- saving
        preference = get_user_preference(request.user.id)  #todo use the staff preference not the user
        total_rows = SavingModel.objects.filter(member_id =member_info.id).count()
        Saving_transaction = myTable(data="",filter_field= "member_id",filter_field_value= member_info.id,total_rows=total_rows,user_prefered_nos_rows=preference.financial_transaction,model= 'saving')
        Saving_transaction.member_id = member_info.id
        Saving_transaction.user_preference = preference
        Saving_transaction.data =""
        Saving_transaction.category={"regular_transaction":True}
        Saving_transaction.button_info ="Info"
        Saving_transaction.button_edit ="Edit"


        #------ payment
        preference = get_user_preference(request.user.id)  #todo use the staff preference not the user
        total_rows = PaymentModel.objects.filter(member_id =member_info.id).count()
        Payment_transaction = myTable(data="",filter_field= "member_id",filter_field_value= member_info.id,total_rows=total_rows,user_prefered_nos_rows=preference.financial_transaction,model= 'payment')
        Payment_transaction.member_id = member_info.id
        Payment_transaction.user_preference = preference
        Payment_transaction.datas ="datasss"
        Payment_transaction.total_tips= {"Paid":"Total Amount Paid","Owe":"Total Loan Owing","Balance":"Outstanding Balance"}

        Payment_transaction.data =""
        Payment_transaction.category={"loan_payment":True}
        Payment_transaction.button_info ="Info"
        Payment_transaction.button_edit ="Edit"

        #-------- Loan
        preference = get_user_preference(request.user.id)  #todo use the staff preference not the user
        total_rows = PersonalLoanModel.objects.filter(member_id =member_info.id).count()
        PersonalLoan_transaction = myTable(data="",filter_field= "member_id",filter_field_value= member_info.id,total_rows=total_rows,user_prefered_nos_rows=preference.financial_transaction,model= 'loan')
        PersonalLoan_transaction.member_id = member_info.id
        PersonalLoan_transaction.user_preference = preference
        PersonalLoan_transaction.data =""
        PersonalLoan_transaction.button_info ="Info"
        PersonalLoan_transaction.button_edit ="Edit"
        print(f"...loan preference:{preference}")


     # ------- transfer history ------
        sender = id
        
        table_transfer_history = TransferReceiver_cls(filter_field="sender_id",filter_field_value=sender,model="CashTransfer2",code_name="transfer-history") 
        table_transfer_history.code_name="transfer-history"
        table_transfer_history.user_preference= get_user_preference(request.user.id) #many of 'user_preference'
        table_transfer_history.filter_dict={'sender_id':sender}
        table_transfer_history.data=""
        table_transfer_history.message ={"transfer_history":"Are you sure you want to cancel this transfer?"}
        table_transfer_history.show_data=False
        table_transfer_history.delay_filling =True
        #table_transfer_history.add_confirm_modal =True
        table_transfer_history.columns =("CODE","S-ID","RE-ID", "DATE","RECEIVER","PURPOSE","SOURCE","AMOUNT","STATUS","ACTION")
        
        #row_columns =  f"<tr {'classname'} id= {'item.id'}> <th> {'row_ctr' }</th> <td class='left' ><span id='code'>  {'item.id'}</span></td><td class='left'> {'item.date_entered'} </td> <td class='left' id='receiver'> {'fullname'} </td><td class='left'> {'item.address'}</td><td>{'item.amount'} </td><td class='{'item.status'}' ><span class='status'> {'status'} </span></td><td>{'action'}</td></tr>"
        #print("....row_col:",row_columns)
        #table.template_name = "products/member/templates/table.html"
        #member_info.isUserInfo =isUserInfo  
        receiver = id
        claim_transfer = TransferReceiver_cls(filter_field="receiver_id",filter_field_value=receiver,model="cashtransfer3") 
        claim_transfer.code_name="claim-transfer" 
        claim_transfer.message ={"claim_transfer":"Are you sure you want to reject this transfer?"}
        #claim_transfer.add_confirm_modal =True
        claim_transfer.user_preference= get_user_preference(request.user.id) #many of 'user_preference'
        claim_transfer.filter_dict={'receiver_id':receiver,'status':'W'}   #'status__in':["A","W","R"]}
        claim_transfer.setData(0,claim_transfer.user_preference.claim_transfer,False) #   qs[0:Cash_transfer_nos_of_row]
        claim_transfer.columns =("CODE","S-ID","R-ID","DATE","SENDER","PURPOSE","AMOUNT","ACTION")
        #claim_transfer.data=""
        # --------------- create card -------------
        class obj:
            pass
        table_card =obj()
        table_card.cards=[]
        
        table_card.cards.append({"name":"CM ACCT","card_name":"Cc","id":id,"model_name":"cc"})
        table_card.cards.append({"name":"WALLET ACCT","card_name":"E-Wallet","id":id,"model_name":"wallet"})
        table_card.cards.append({"name":"SAVINGS ACCT","card_name":"Saving","id":id,"model_name":"saving"})
        table_card.cards.append({"name":"LOAN BALANCE","card_name":"Payment","id":id,"model_name":"payment"})


        table_card.template_name = "fx/users/templates/card_template.html"
        has_temp_pwd =False 
        try:
            pwd = Tmp_PasswordModel.objects.get(member_id = id).pwd
            has_temp_pwd =True  
        except Exception as e:
            print (f"{e}, {type(e)}")
        #print("has_tmp_pwd:",disable_show_pwd)
        context={
             "table_card":table_card,
             "member_info":member_info,
             "wallet_transaction":wallet_transaction,
             "Cc_transaction":Cc_transaction,
             "Saving_transaction":Saving_transaction,
             "Payment_transaction":Payment_transaction,
             "Loan_transaction":PersonalLoan_transaction,
             "table_transfer_history":table_transfer_history,
             "claim_transfer_table":claim_transfer,
             "has_temp_pwd":has_temp_pwd,
            #  'State':{"finance":"active"}
         }
        return render(request, "fx/member/display_member_info.html", context)




# def claim_transferx(request):
# #CashTransfer.objects.select_related('receiver').order_by('-id').filter( **filter_dict )
#   pass

#123    model_name,amount,field,field_value,
def withdraw_from_account(amount,description,sender):
    category = 1 # code for transfer 
    try:
        wallet_qs = WalletModel(date_entered=date.today(),transaction_type='W' ,description=description,credit=0,debit=amount ,member_id=sender,category=category)
        wallet_qs.save() 
        return wallet_qs.id
    except WalletModel.DoesNotExist:
        return -1
        # add log here
    #return True

def success_transfer(request,sender,code):
        
       
        post_data  = TransferModel.objects.select_related('receiver').order_by('receiver_id').filter(Q(sender_id=sender), Q(code = code) )
        total_amount = post_data.aggregate(sum=Sum('amount'))
        member_info = MemberModel.objects.get(id =sender)
            #= CashTable(model)
        #table.paginate(page=request.GET.get("page", 1), per_page=8)
        print("....post data:",post_data)
        context={
            "post_data": post_data,
            "total_amount":total_amount,
            "member_info":member_info,
            # "info":{"sender":sender,"code":code},
        } 
        # print(f"list:{receiver_list} , wallet_transaction_id:{walletTransaction_id}")
        messages.success(request, "The following transaction has been successfully recorded.")
        return render(request, "fx/e_wallet/new_transfer.html", context)



#transfer
@login_required
def  transfer(request,account_name,sender):
    member_info = MemberModel.objects.get(id =sender)
    if request.method == "GET":
#------table-for searching  member           
                table_search =SearchMember(filter_field="",filter_field_value="")
                table_search.user_preference= get_user_preference(request.user.id)
                table_search.code_name="search-receiver"
#-----table -for searching for receiver for transfer purpose
                table_receiver = TransferReceiver_cls(filter_field="sender_id",filter_field_value=sender,model="CashTransfer",code_name="transfer-receiver") #todo user_prefered_nos_rows =?
                table_receiver.code_name="transfer-receiver"
                #        claim_transfer.filter_dict={'receiver_id':receiver,'status__in':["A","W","R"]}
                table_receiver.filter_dict={'sender_id':sender}   #add19
                table_receiver.user_preference= get_user_preference(request.user.id)
                table_receiver.setData(0,table_receiver.user_preference.transfer_receiver,True) #   qs[0:Cash_transfer_nos_of_row]
                table_receiver.show_data = True
                table_receiver.columns =("CODE","S-ID","R-ID","NAME","ADDDRESS","CONTACT NOS.","ACTION")
#-----transfer history
                table_transfer_history = TransferReceiver_cls(filter_field="sender_id",filter_field_value=sender,model="CashTransfer2",code_name="transfer-history") 
                table_transfer_history.code_name="transfer-history"
                table_transfer_history.user_preference= get_user_preference(request.user.id) #many of 'user_preference'
                table_transfer_history.filter_dict={'sender_id':sender}  #add19
                table_transfer_history.data=""
                table_transfer_history.delay_filling =True
                table_transfer_history.show_data=False
                table_transfer_history.columns =("CODE","S-ID","R-ID","DATE","RECEIVER","PURPOSE","SOURCE","AMOUNT","STATUS","ACTION")
#----- Claim Transfer


                context={
                    "member_info":member_info,
                    "table_search":table_search,
                    "table_receiver":table_receiver,
                    "table_transfer_history":table_transfer_history,
                    "info":{"sender":sender},
                    'asset_liabities':get_all_balances(sender),
                }
                #messages.error(request, "Amount to cash out must be less or equal to  none")
                return render(request, "fx/e_wallet/new_transfer.html", context)
    else:  #request.method == "POST":
                account_name = request.POST.get("sourcetype","").strip().lower()
                model_list= {"wallet":"WalletModel","saving":"SavingModel","cc":"CcModel","payment":"PaymentModel","loan":"PersonalLoanModel"}
                model =model_list.get(account_name).lower() # account_name is not written as account-name so that it doesnt affect the "for key, value in request.POST.items():" operation below
                Model = apps.get_model('fx', model)
                total_balance = get_running_finance_balance(account_name ,"member_id",sender)["running_balance"]
                print(f"....total_balance: {total_balance}, account: {account_name}")
                 
                print("post:",request.POST.items())
                store=[]
                receiver_list ={}
                for key, value in request.POST.items():
                    print(f"key: {key} , value: {value}")
                    if '_' in key:
                    
                        combine_list = key.split('_') 
                        receiver_id = int( combine_list[0])
                        field_name = combine_list[1]
                        if receiver_id in store:
                           receiver_list[receiver_id].update({field_name: value})
                        else:
                            store.append(receiver_id)
                            receiver_list[receiver_id]= {field_name: value}
                print("list:",receiver_list)
                total_amount = 0
                for key in receiver_list:
                       total_amount =total_amount+ float(receiver_list[key]['amount'])
                #todo: needs to be modified with redirecting just issue error message: total_amount >  total_balance
                if total_amount >  total_balance:  #because balance is on the user page so this is no reason for a page to be allowed when total amount exceeds the remaining balance
                    print("total_amount >  total_balance: unexpected result")
                    context ={'message':" Sorry. This page encountered internal problem. Thank you."}
                    return redirect(request, "fx/messages/pagenotfound.html", context)   
                 # ------- get and new code or transaction code number
                code = 0
                try:
                    qs = CodeGeneratorModel.objects.get(sender_id = sender)
                    code = qs.code + 1
                    qs.code =F('code')+1
                    qs.save()
                     
                except  CodeGeneratorModel.DoesNotExist:
                    codeGenerator =  CodeGeneratorModel(sender_id = sender,code =1 )
                    codeGenerator.save()
                    code = 1
                description= "Transfer (Cash Out)"
               # for client_id in receiver_list:
                account_Initial_list={"wallet":"W","saving":"S","cc":"C","cash":"K"}
                source_type = account_Initial_list.get(account_name)
                #if source_type == 'C'
                print(f"......source_type: {source_type} , {account_name}")
                
                account_id = -1 # nonexisting 
                category = 1 # code for transfer operation
                Success= True
                transfer_qs=""
                try:
                            account_qs = Model(date_entered=date.today(),transaction_type='W' ,description=description,credit=0,debit=total_amount ,member_id=sender,category=category,source_id =0 ) # 0 means failed during updating in transferModel, 1 has succesfully saved to the transferModel
                            account_qs.save() 
                            account_id = account_qs.id
                            print(f" account_id: {account_id}")
                except Exception as e:
                            Success = False
                            print (f"{e}, {type(e)}")
                if Success:
                    for key in receiver_list:
                    #note :
                            purpose =receiver_list[key]['purpose']
                            amount = receiver_list[key]['amount']
                            
                            try:
                                    transfer_init_qs = TransferModel(source_type=source_type,date_entered=date.today(),status='W',purpose=purpose ,amount=amount,sender_id =sender,receiver_id=receiver_id,code = code,source_id = account_id )
                                    transfer_init_qs.save()  #todo now {uncomment}
                            except Exception as e:
                                    Success =False
                                    print (f"{e}, {type(e)}")
                            receiver_id = key
                            if  Success:   
                                try:
                                   # print(f"date_entered:{date.today()},status='W',purpose={purpose} ,amount={amount},sender_id ={sender},receiver_id={receiver_id},code ={code}" )
                                    transfer_qs = TransferModel.objects.filter(id =transfer_init_qs.id ).update(flag= 1, source_id = account_id )  #1 accepted
                                   # print("...cash.id",transfer_qs.id)
                                except Exception as e:
                                    Success =False
                                    print (f"{e}, {type(e)}")
                            else:
                                delete_source_qs = Model.objects.get(id= account_id).delete()
                                print("....account_id deleted")
                                return #todo make unsuccess direct page
                
                    if Success:
                          Model.objects.filter(id= account_id).update(source_id =transfer_init_qs.id)
                return redirect(f'/success/transfer/{sender}/{code}/')

def ValidateUsername(username):
    codeCtr=1
    qs = User.objects.filter(username__iexact = username) 
    if qs.count() == 0:
        print ("not found...")
        return username
    else:
          qs = Tmp_UsernameModel.objects.filter(username__iexact = username)
          if qs.count() == 0:
              print("new record on code_counter:", username)
             
              Tmp_UsernameModel.objects.create(username=username,code_counter= codeCtr )
            
          else:
               
              qs = Tmp_UsernameModel.objects.filter(username__iexact = username)
              codeCtr = qs[0].code_counter + 1
              
              qs.update(code_counter = codeCtr ) #return  1 success or 0 failed
              print("code ctr must increment")
         
    
    newCodeCtr = str(codeCtr).strip()
    if len(newCodeCtr) == 1:    # convert the 1 digit value from db to 2 digits
        newCodeCtr = newCodeCtr
    username = username+ newCodeCtr
    return username
    

def gen_password():
    
    rndPwd =""
    ctr = 0
    for x in range(2):
        pwd = random.randint(1,21) * 5
        if (ctr == 0 and pwd == 0) or (ctr == 4 and pwd == 0) :
            pwd = 1
        rndPwd += str(pwd)
        ctr = ctr  + 1 
     
    lenght = len(rndPwd)
    if lenght > 4:
        rndPwd=rndPwd[0:4]
         
    else:
        if lenght < 4:
           add = 4 - lenght
           rndPwd =rndPwd + rndPwd[0:add]    
    return rndPwd

 
def create_update_member_result(request,id,msg):
        member_info = get_member_info(id,"#create_update_member_result.   1")#create_update_member_result.   1
        form = MemberForm(instance=member_info)
        
        
        context = {
            'form': form,
            'post_data':True,
            'member_info': member_info,
            'State':{"new_member":"active"}}
        messages.success(request, msg)
        return render(request, 'fx/create_update_member.html',context)

#cum
@login_required(login_url='/login/')
def create_update_member(request, id=id):
            max_loan = 0
            if id > 0 :
                  member_info = get_member_info(id,"#create_update_member.1") #create_update_member.1
            else:
                  member_info={"id":0}
            try: 
                         max_loan = tmpVariables.objects.values("max_loan").get(id = 1)["max_loan"]
                         print(f"----- max: {max_loan}")
            except Exception as e:
                                max_loan =  300
                                print(f"------ Error in reading max_loan")
                                logger.warning(f"cum,else,if ==0: e:{e}")
            if request.method == "GET":
                        if id == 0:
                            initial_data ={'member_id':'default'}
                            print(f"initial_data: {initial_data}")
                            form = MemberForm(initial=initial_data)   
                        else:

                            form = MemberForm(instance = member_info)
                        form.max_loan =max_loan
                        context = {
                            'form': form,
                            'member_info': member_info,
                            'State':{"new_member":"active"}
                        }
                        return render(request, "fx/create_update_member.html", context)
            else:     #' P O S T'
                if id == 0:
                    
                    
                    username = request.POST.get("member_id","")
                    agree = request.POST.get("agree","").strip()
                    if agree =="on":
                         agree =True
                         max_loan = request.POST.get("apply",0)
                    else:
                         agree =False
                    
                    print(f"aggree: {agree} , type:{ type(agree )}")
                    
                    # add Loan to new member initialize
                  
                                
                     
                        
                    #ed loan to new member initialize
                    memberForm = MemberForm(request.POST) 
                    if   memberForm.is_valid():
                            print('pass member form valid!')
                            firstname= memberForm.cleaned_data['firstname'].strip().lower()
                            bday= memberForm.cleaned_data['birthday']
                            gender= memberForm.cleaned_data['gender'].strip().lower()
                             
                            
                            month = bday.strftime("%m")
                            print(f"month type: {type(month)}")
                            day = bday.strftime("%d")
                            if gender == "mr.":
                                    code = 1
                            else:
                                     code = 0
                        
                            newUsername = firstname[0:2] +month+day +"-"+str(code).strip()

                            
                            print(f" new username: {newUsername}")
                            
                            newUsername = ValidateUsername(newUsername)
                            newUsername = newUsername.lower()
                            newPassword = gen_password()
                            print(f"...newpassword: {newPassword} new username:{newUsername}")
                            Success = True
                            try: #uoc
                                 
                                user = User.objects.create_user( newUsername, email = None,password= newPassword)
                            except Exception as e:
                                 Success = False
                                 print (f" Error creating user at cum: {e}") #todo here
                                 logger.warning(f"cum,uoc e:{e}")
                            print(f"newUsername:{newUsername}")
                            
                            print("saving new member(valid).......")
                            
                            if Success:
                                    try: #qsm
                                            qs = memberForm.save(commit = False)
                                            qs.user = user   #todo unquote 'user'
                                            qs.member_id = newUsername
                                            updated_Member = qs.save()  #todo uncomment
                                    except Exception as e:
                                        Success = False
                                        print (f" Error writinf temp pass at cum: {e}") #todo here
                                        logger.warning(f"cum,qsm e:{e}")
                                
                            print("---- memberid: {memberid}")
                            if Success:
                                    try:#new
                                        
                                        newPassword = newPassword.encode("utf-8")
                                        encoded = base64.b64encode(newPassword).decode("utf-8")
                                        
                                        pwd = Tmp_PasswordModel.objects.create(member_id= qs.id, pwd = encoded )
                                    except Exception as e:
                                        Success = False
                                        print (f" Error writinf temp pass at cum: {e}") #todo here
                                        logger.warning(f"cum,new e:{e}")
                                        
                           
                            print(f"---- qs.id: {qs.id}")
                            memberid = qs.id
                            ## add Loan to new member
                            
                            category = CAT_LOAN
                            if  Success and agree:  #user has agreed to receive cc
                                    try: #st
                                        source_type ="M" # additional loan
                                        payment_additional_qs = PaymentModel(source_type=source_type,source_id =0 ,date_entered=date.today(),transaction_type='D' ,credit=max_loan,debit=0 ,member_id=memberid,category=category)
                                        payment_additional_qs.save()   
                                        print(f"success in recording additional loan max:{max_loan}")
                                    except Exception as e:
                                        Success = False
                                        print (f"Error: recording additional loan (Bonus), {e}, {type(e)}")
                                        logger.warning(f"cum,st e:{e}")
                                    if Success:
                                        try:#dal
                                                    
                                                description = "Additional Loan (Bonus)"
                                                 #loan
                                                Cc_qs = CcModel(member_id = memberid, date_entered=date.today(),transaction_type='D', description=description,credit=max_loan,debit=0,category=category,source_id = payment_additional_qs.id ) #source_id =loan_qs.id 
                                                Cc_qs.save() 
                                                
                                                print(f"success Additional Loan")
                                        except Exception as e:
                                                Success= False
                                                print (f"error result in adding addional loan (bonus):{e}, {type(e)}")
                                                logger.warning(f"cum,dal e:{e}")
                                        # Add new 
                                        if  Success:
                                                try:#ll
                                                            loanSummary_qs = LoanSummaryModel (member_id = memberid, max_loan =300,date_entered = date.today())
                                                            loanSummary_qs.save() 
                                                except Exception as e:
                                                            print(f" creating new entry for new member e:{e}")
                                                            Success = False
                                                            logger.warning(f"cum,ll e:{e}")
                                            
                                         
                            ## end of loan to new member
                            
                            
                            
                            
                            msg = "New member has been successfully added!"
                            return redirect(f'/success/create_update_member_result/{qs.id}/{msg}')
                    else:
                                    print("not valid adding new member.")
                                    context = {
                                    'form': memberForm,
                                    'State':{"new_member":"active"}
                                    }
                                    return render(request,"fx/create_update_member.html", context)
                else:    #POST   SAVE UPDATE EXISTING RECORD
                        try:
                            member_info = MemberModel.objects.get(id=id)
                        except  MemberModel.DoesNotExist:
                            print('error reading Member info.')
                        old_firstname= member_info.firstname
                        old_birthday = member_info.birthday
                        old_gender = member_info.gender.strip().lower()
                        old_user_id = member_info.user_id
                        
                        firstname = request.POST.get("firstname","")
                        bday = request.POST.get("birthday","")
                        gender =  request.POST.get("gender","").strip().lower()
                        print(f"gender: {gender},old user id: {old_user_id}")
                        
                        print(f"firstname: {old_firstname},old_bday: {old_birthday}, type: {type(old_birthday)}")   
                        print(f"POST firstname: {firstname},old_bday: {bday}, type: {type(bday)}")   
                        arr_bday = bday.split("-")
                        month = old_birthday.strftime("%m")
                        day = old_birthday.strftime("%d")
                        print(f"OLD month:{month}, day: {day}")
                        print(f"farr bday:[{arr_bday},{arr_bday[1]},{arr_bday[2]}")
                        
                         
                        memberForm = MemberForm(request.POST , instance=member_info)
                        
                        HasChange =False
                        if firstname[0:2] != old_firstname[0:2]:
                            HasChange = True
                            print("change name")
                        if month != arr_bday[1] or day != arr_bday[2]:
                             HasChange = True 
                             print("change month or day")
                        if old_gender != gender:
                             HasChange = True
                             print("gender change")
                        print(f"firstname[0,2]:{firstname[0:2]}, arr_bday[0]:{arr_bday[1]}, has Changed:{HasChange}")
                        code =-1
                        if HasChange:
                                if gender == "mr.":
                                    code = 1
                                else:
                                     code = 0
                                     
                                     
                                
                        print (f" gender code: {code}") 
                        member_id = firstname[0:2] +arr_bday[1]+arr_bday[2] +"-"+str(code).strip()
                        if HasChange:
                                print(f" member id: {member_id}")
                                member_id = ValidateUsername(member_id)

                        if memberForm.is_valid():
                            if HasChange:
                                try:#uob1
                                    user = User.objects.filter( id = old_user_id).update (username = member_id)

                                except Exception as e: #todo here
                                    print(f"update user member_id error: {e}")
                                    logger.warning(f"cum,uob1 e:{e}")
                            qs = memberForm.save(commit=False)
                            if HasChange:
                                qs.member_id = member_id
                                print("saving successful while changing the user id")
                            else:
                                print("saving successful w/o changing the user id")
                            qs.save()
                            print("success editing")
                            msg ="The following has been successfully updated!"
                            return redirect(f'/success/create_update_member_result/{id}/{msg}')
                        else:  #invalid form  for existing record
                            
                            context = {
                                    'form':memberForm,  #tsomething wrong here
                                    'member_info':member_info,
                                    'State':{"new_member":"active" }
                                }
                        return render(request, "fx/create_update_member.html", context)
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    

 
 