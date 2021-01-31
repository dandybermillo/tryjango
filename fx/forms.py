from django import forms
from .models import MemberModel,SavingModel,PaymentModel
from .models import WalletModel,PersonalLoanModel,VentureModel,TradingModel
from datetime import   date
from django.contrib.auth import (
    authenticate,
    get_user_model

)
from .models import MessageModel
from fx.models import Tmp_UsernameModel

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import EmailValidator, ValidationError
User = get_user_model()

minimum_deposit = 0
maximum_deposit =10000
limits ={"minimum_deposit":minimum_deposit,"maximum_deposit": maximum_deposit}




# class LoadForm(forms.ModelForm):
#     CARRIER_CHOICES= [
    
#     ("SMART","SMART"),("GLOBE","GLOBE"),("DITO","DITO"),("TALK","TALK N TEXT"),("SUN","SUN CELLULAR"),
# ]
#     name = forms.CharField(required = True,widget=forms.TextInput(attrs={'placeholder': 'Fullname','class':'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'}))
#     phone = forms.CharField(required = True,widget=forms.TextInput(attrs={'placeholder': 'Enter your phone (e.g. +14155552675)','pattern':'\+?\d{0,3}[\s\(\-]?([0-9]{2,3})[\s\)\-]?([\s\-]?)([0-9]{3})[\s\-]?([0-9]{2})[\s\-]?([0-9]{2})',"class":'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'}))
#     carrier = forms.ChoiceField(label='', choices=CARRIER_CHOICES, widget=forms.Select(attrs={'class':'u-border-2 u-border-grey-25 u-input u-input-rectangle u-radius-5'}))
#     amount = forms.FloatField(required = True,widget=forms.NumberInput(attrs={'placeholder': 'Amount', 'step': "0.01",'class':'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'}))
#     class Meta:
#         model = ContactModel
#         fields =["name","phone","carrier","amount"]
    
# class SignUpModelForm(forms.ModelForm):
#     name = forms.CharField(required = True,widget=forms.TextInput(attrs={'placeholder': 'Fullname','class':'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'}))
#     phone = forms.CharField(required = True,widget=forms.TextInput(attrs={'placeholder': 'Enter your phone (e.g. +14155552675)','pattern':'\+?\d{0,3}[\s\(\-]?([0-9]{2,3})[\s\)\-]?([\s\-]?)([0-9]{3})[\s\-]?([0-9]{2})[\s\-]?([0-9]{2})',"class":'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'}))
#     address = forms.CharField(
#         label='Address',required =True,
#         widget=forms.TextInput(attrs={'placeholder': 'Current Address','class':'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'})
#     )
#     birthday = forms.DateField(required = True,widget=forms.DateInput(attrs={'type':'date','placeholder': 'MM/DD/YY',"class":'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'}))    #, 'min':"1920-01-01", 'max':"2010-12-31"}))
#     class Meta:
#         model = ContactModel
#         fields =["name","phone","address","birthday"]
class MessageForm(forms.ModelForm):
    name = forms.CharField(required = True,widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Name','class':'u-input u-input-rectangle u-white'}))

    email = forms.EmailField(required = True,widget=forms.TextInput(attrs={'type':'email','placeholder': 'Enter a valid email address','class':'u-input u-input-rectangle u-white'}))
    message = forms.CharField(
        label='Message',required =True,
        widget=forms.Textarea(attrs={"rows":3,"cols":20,'placeholder': 'Enter your message','class':'u-input u-input-rectangle u-white'})
    )      #description= forms.CharField(required =True,widget=forms.Textarea(attrs={"rows":1,"cols":20}))

    
    class Meta:
        model = MessageModel
        fields =["name","email","message"]
    def clean_email(self,*args, **kwargs):
                print(".....clean_emaill")
                email = self.cleaned_data.get('email')
                validator = EmailValidator()
                email =email.strip()
                if(len(email )> 0):
                        try:
                            validator(email)
                        except ValidationError:
                            print("Please enter valid email address.")
                            raise forms.ValidationError("Please enter valid email address.")
                
                return email

class UserLoginForm(AuthenticationForm):
    user = None

    def get_user(self):
       return self.user


    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password')
       
        if username and password:
                self.user = authenticate(username=username, password=password)
                print(f"....self.user:{self.user}, username:{username}")
                if self.user is None:
                    
                    try:
                        print("try.....")
                        # User.objects.get(username__exact=username)
                        self.user = User.objects.get(username__exact=username)
                        res=self.user.check_password(password)
                        print(f"....password:{password} , check: {res}")
                        if not self.user.check_password(password):
                            raise forms.ValidationError('Incorrect password')
                        if not self.user.is_active:
                            raise forms.ValidationError('This user is not active')
                    except ObjectDoesNotExist:

                        raise forms.ValidationError('This user does not exist')
                
                   
        return super(UserLoginForm, self).clean(*args, **kwargs)
    


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered")
        return super(UserRegisterForm, self).clean(*args, **kwargs)



class MemberForm(forms.ModelForm):
   MR,MS,MRS =("Mr.","Ms.","Mrs.")
    
   gender_status = (("","Select Gender"), (MR,"Mr."),(MS,"Ms."),(MRS,"Mrs"))
   
   gender = forms.ChoiceField(required =True,choices=gender_status)

   email = forms.CharField(required = False,widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
   
   telephone = forms.CharField(required = False,widget=forms.TextInput(attrs={'placeholder': 'telephone'}))
   firstname = forms.CharField(required = True,widget=forms.TextInput(attrs={'placeholder': 'First name'}))
   lastname = forms.CharField(required = True,widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
   middlename = forms.CharField(required = False,widget=forms.TextInput(attrs={'placeholder': 'Middle name'}))
   member_id = forms.CharField(required = True,widget=forms.TextInput())
   address = forms.CharField(
        label='Address',required =True,
        widget=forms.TextInput(attrs={'placeholder': 'Current Address'})
    )
   class Meta:
      model = MemberModel
      fields =["member_id","gender","firstname","middlename","lastname","email","address","telephone","active","birthday"]

   def clean_email(self,*args, **kwargs):
        print(".....clean_emaill")
        email = self.cleaned_data.get('email')
        validator = EmailValidator()
        email =email.strip()
        if(len(email )> 0):
                try:
                    validator(email)
                except ValidationError:
                     print("Please enter valid email address.")
                     raise forms.ValidationError("Please enter valid email address.")
        
        return email
   def ValidateUsername(self,username):
    print("validating-------------")
    codeCtr=1
    qs = User.objects.filter(username__iexact = username) 
    if qs.count() == 0:
        print (f"not found... username:{username}")
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
    
   def clean_member_id(self,*args, **kwargs):
        print(".....clean_ member_id")
        member_id = self.cleaned_data.get('member_id').strip().lower()
        if member_id == "default":
              member_id = self.ValidateUsername(member_id)
            
        
        
        
       
        # validator = EmailValidator()
        # email =email.strip()
        # if(len(email )> 0):
        #         try:
        #             validator(email)
        #         except ValidationError:
        #              print("Please enter valid email address.")
        #              raise forms.ValidationError("Please enter valid email address.")
        print(f"clean_member_id: {member_id}")
        return member_id



class DateInput(forms.DateInput):
   input_type = 'date' 

 

class PersonalLoanForm(forms.ModelForm):
   
   # DEPOSIT ,WITHRAWAL =("D","W")
   # trans_type =((DEPOSIT,"DEPOSIT"),(WITHRAWAL , "WITHDRAW"))
   #date_entered = forms.DateField(initial=date.today())
   
    class Meta:
      model = PersonalLoanModel
      fields=["cc_loan","saving","percent","date_entered","source_type","note_id","cc_id","source_id","flag","saving_id"]   


    def clean_saving(self,*args, **kwargs):

        #transType =self.cleaned_data.get('transaction_type')
        amount = self.cleaned_data.get('saving')
       # if    transType == "D":
        if amount == None or  amount <= 0:
               raise forms.ValidationError("Please enter an amount that is more than zero.")
        return amount 

class WalletForm(forms.ModelForm):
   
   # DEPOSIT ,WITHRAWAL =("D","W")
   # trans_type =((DEPOSIT,"DEPOSIT"),(WITHRAWAL , "WITHDRAW"))
   #date_entered = forms.DateField(initial=date.today())
   
    class Meta:
      model = WalletModel
      fields=["transaction_type","credit","debit","date_entered","description"]
      #description= forms.CharField(required =True,widget=forms.Textarea(attrs={"rows":1,"cols":20}))
      transaction_type = forms.CharField(widget=forms.HiddenInput())
      #middlename = forms.CharField(required = False,widget=forms.TextInput(attrs={'placeholder': 'Middle name'}))
      #credit== forms.CharField(widget=forms.TextInput(attrs={'class':'form-control})))
    #   credit== forms.CharField(required = False,widget=forms.TextInput(attrs={'min': '1','type':'number'}))

    def __init__(self, *args, **kwargs):
        super(WalletForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['date_entered'].widget.attrs['readonly'] = True
     # widgets= {'date_entered': DateInput() }
    
    def clean_credit(self,*args, **kwargs):

        transType =self.cleaned_data.get('transaction_type')
        amount = self.cleaned_data.get('credit')
        if    transType == "D":
            if amount == None or  amount < 1:
               raise forms.ValidationError("Amount must be greater than zero.")
        return amount
        
    def clean_debit(self,*args, **kwargs):
       
        transType =self.cleaned_data.get('transaction_type')
        amount = self.cleaned_data.get('debit')
        print(f"clean debit pasts, amount:{amount}, type: {transType}")
        if transType == "W":
           
            if amount == None or  amount < 1:
                  raise forms.ValidationError("Amount must be greater than zero.")
        return amount



    def clean_description(self,*args, **kwargs):
        description = self.cleaned_data.get('description')
        print("len of description",len(description))
        if len(description) < 7:
             raise forms.ValidationError("Description  must be greater than  6 characters.")
         
        return description

 
class PaymentForm(forms.ModelForm):
   
   # DEPOSIT ,WITHRAWAL =("D","W")
   # trans_type =((DEPOSIT,"DEPOSIT"),(WITHRAWAL , "WITHDRAW"))
   #date_entered = forms.DateField(initial=date.today())
   
    class Meta:
      model = PaymentModel
      fields=["transaction_type","credit","debit","date_entered","source_type"]
      #description= forms.CharField(required =True,widget=forms.Textarea(attrs={"rows":1,"cols":20}))
      transaction_type = forms.CharField(widget=forms.HiddenInput())
      #middlename = forms.CharField(required = False,widget=forms.TextInput(attrs={'placeholder': 'Middle name'}))
      #credit== forms.CharField(widget=forms.TextInput(attrs={'class':'form-control})))
    #   credit== forms.CharField(required = False,widget=forms.TextInput(attrs={'min': '1','type':'number'}))

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['date_entered'].widget.attrs['readonly'] = True
     # widgets= {'date_entered': DateInput() }
    
    # def clean_credit(self,*args, **kwargs):

    #     transType =self.cleaned_data.get('transaction_type')
    #     amount = self.cleaned_data.get('credit')
    #     if    transType == "D":
    #         if amount == None or  amount < 1:
    #            raise forms.ValidationError("Amount must be greater than zero.")
    #     return amount
        
    def clean_debit(self,*args, **kwargs):
       
        transType =self.cleaned_data.get('transaction_type')
        amount = self.cleaned_data.get('debit')
        print(f"clean debit pasts, amount:{amount}, type: {transType}")
        if transType == "W":
            if amount == None or  amount < 1:
                  raise forms.ValidationError("Amount must be greater than zero.")
        return amount

class SavingForm(forms.ModelForm):
   
   # DEPOSIT ,WITHRAWAL =("D","W")
   # trans_type =((DEPOSIT,"DEPOSIT"),(WITHRAWAL , "WITHDRAW"))
   #date_entered = forms.DateField(initial=date.today())
   
    class Meta:
      model = SavingModel
      fields=["transaction_type","credit","debit","date_entered","description"]
      #description= forms.CharField(required =True,widget=forms.Textarea(attrs={"rows":1,"cols":20}))
      transaction_type = forms.CharField(widget=forms.HiddenInput())
      #middlename = forms.CharField(required = False,widget=forms.TextInput(attrs={'placeholder': 'Middle name'}))
      #credit== forms.CharField(widget=forms.TextInput(attrs={'class':'form-control})))
    #   credit== forms.CharField(required = False,widget=forms.TextInput(attrs={'min': '1','type':'number'}))

    def __init__(self, *args, **kwargs):
        super(SavingForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['date_entered'].widget.attrs['readonly'] = True
     # widgets= {'date_entered': DateInput() }
    
    def clean_credit(self,*args, **kwargs):

        transType =self.cleaned_data.get('transaction_type')
        amount = self.cleaned_data.get('credit')
        if    transType == "D":
            if amount == None or  amount < 1:
               raise forms.ValidationError("Amount must be greater than zero.")
        return amount
        
    def clean_debit(self,*args, **kwargs):
       
        transType =self.cleaned_data.get('transaction_type')
        amount = self.cleaned_data.get('debit')
        print(f"clean debit pasts, amount:{amount}, type: {transType}")
        if transType == "W":
           
            if amount == None or  amount < 1:
                  raise forms.ValidationError("Amount must be greater than zero.")
        return amount



    def clean_description(self,*args, **kwargs):
        description = self.cleaned_data.get('description')
        print("len of description",len(description))
        if len(description) < 7:
             raise forms.ValidationError("Description  must be greater than  6 characters.")
         
        return description


class VentureForm(forms.ModelForm):
    class Meta:
      model = VentureModel
      fields=['customer',"in_charge",'transaction_type','date_entered','source_type','amount','cc','category','percent']  

    def clean_amount(self,*args, **kwargs):
        amount = self.cleaned_data.get('amount')
        if amount == None or  amount <= 0:
               raise forms.ValidationError("Please enter an amount that is more than zero.")
        return amount 
    def clean_cc(self,*args, **kwargs):
        cc = self.cleaned_data.get('cc')
        print(f">---- cc: {cc}")
        if cc == None:
            raise forms.ValidationError("Please enter an Community Coin (CC) that is more than zero.")
        if cc < minimum_deposit or cc >  maximum_deposit:
               raise forms.ValidationError(f"Please enter an Community Coin (CC) between {minimum_deposit} and {maximum_deposit}")
        return cc 
    def clean_percent(self,*args, **kwargs):
        percent = self.cleaned_data.get('percent')
        if percent == None:
            raise forms.ValidationError("Please enter percentage(%) between 1 and 100")
        if percent <= 0 or percent >  100:
               raise forms.ValidationError(f"Please choose percentage(%) between 1 and 100")
        return percent 
    def clean_source_type(self,*args, **kwargs):
        source_type = self.cleaned_data.get('source_type')
        if source_type == None:
            raise forms.ValidationError("Please select the source of funds.")
        if source_type not in ['W','K']:
            raise forms.ValidationError(f"Please select the source of funds.")
        return source_type 

class TradeForm(forms.ModelForm):
    class Meta:
      model = TradingModel
      fields=['seller','customer','transaction_type','date_entered','source_type','amount','customer_source_id','role_type','seller_source_id','cc','category','percent']  

    def clean_amount(self,*args, **kwargs):
        amount = self.cleaned_data.get('amount')
        if amount == None or  amount <= 0:
               raise forms.ValidationError("Please enter an amount that is more than zero.")
        return amount 
    def clean_cc(self,*args, **kwargs):
        cc = self.cleaned_data.get('cc')
        if cc == None:
            raise forms.ValidationError("Please enter an Community Coin (CC) that is more than zero.")
        if cc < minimum_deposit or cc >  maximum_deposit:
               raise forms.ValidationError(f"Please enter an Community Coin (CC) between {minimum_deposit} and {maximum_deposit}")
        return cc 
    def clean_percent(self,*args, **kwargs):
        percent = self.cleaned_data.get('percent')
        if percent == None:
            raise forms.ValidationError("Please enter percentage(%) between 1 and 100")
        if percent <= 0 or percent >  100:
               raise forms.ValidationError(f"Please choose percentage(%) between 1 and 100")
        return percent 
    def clean_source_type(self,*args, **kwargs):
        source_type = self.cleaned_data.get('source_type')
        if source_type == None:
            raise forms.ValidationError("Please select the source of funds.")
        if source_type not in ['W','K']:
            raise forms.ValidationError(f"Please select the source of funds.")
        return source_type 