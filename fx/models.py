from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Group
# tutorial/models.py
 
# Create your models here.






      

  
class CodeGeneratorModel(models.Model):
      sender_id =models.IntegerField(default = 0)
      code = models.PositiveIntegerField(default =0)



class MemberModel (models.Model):
     MR,MS,MRS =("Mr.","Ms.","Mrs.")
    
     gender_status = ((MR,"Mr."),(MS,"Ms."),(MRS,"Mrs"))
     gender = models.CharField(max_length=4,blank =False, null= False,  choices= gender_status)
     user = models.OneToOneField(User,null =True, on_delete = models.CASCADE, unique =  True)
     
     
     firstname = models.CharField(max_length=50,blank =False, null =False)
     middlename = models.CharField(default="", max_length=50,blank =True, null =True )
     lastname = models.CharField(max_length=50,blank =False, null =False)

     address =  models.CharField(max_length=300,blank =True, null =True)
     telephone =models.CharField(max_length=100,blank =True, null =True)
     note =models.TextField(max_length =400,blank =True,null=True)
     email= models.EmailField(max_length=254,blank= True,null =True)
     birthday = models.DateField(  blank= True, null =True)
     active =  models.BooleanField(default= True)
     reserve =  models.BooleanField(default= False)
     member_id = models.CharField(max_length=11,blank =False, null =False,default="DA1212-1", unique =  True)

     @property
     def name(self):
        return self.gender.title() +" "+self.firstname.title() + " "+ self.lastname.title()


class ProfileModel (models.Model):   # Subject for Approval, the same as MemberModel
     MR,MS,MRS =("Mr.","Ms.","Mrs.")
    
     gender_status = ((MR,"Mr."),(MS,"Ms."),(MRS,"Mrs"))
     gender = models.CharField(max_length=4,blank =False, null= False, default =MR, choices= gender_status)
   #  user = models.OneToOneField(User,null =True, on_delete = models.CASCADE, unique =  True)
     source_id = models.IntegerField(default =0) 
     
     firstname = models.CharField(max_length=50,blank =False, null =False)
     middlename = models.CharField(default="", max_length=50,blank =True, null =True )
     lastname = models.CharField(max_length=50,blank =False, null =False)

     address =  models.CharField(max_length=300,blank =True, null =True)
     telephone =models.CharField(max_length=100,blank =True, null =True)
     note =models.TextField(max_length =400,blank =True,null=True)
     email= models.EmailField(max_length=254,blank= True,null =True)
     birthday = models.DateField( blank= True, null =True)
     active =  models.BooleanField(default= False)
      
    # member_id = models.CharField(max_length=11,blank =True, null =True,default="DA1212-1", unique =  True)

     @property
     def name(self):
            return self.gender.title() +" "+self.firstname.title() + " "+ self.lastname.title()   
class LivePostModel(models.Model):
      READY,NOT_READY,ALMOST_DONE =(0,1,2)
      STATUS_CODE = ((READY,"READY"),(NOT_READY,"NOT READY"),(ALMOST_DONE,"ALMOST DONE"))
      
      MOBILE,COMPUTER_REPAIR,MECHANIC,CONSTRUCTION,DELIVERY =(1,2,3,4,5)
      CATEGORY_CODE = ((MOBILE,"MOBILE TOP UP"),(COMPUTER_REPAIR,"COMPUTER REPAIR"),(MECHANIC,"MECHANIC"),(CONSTRUCTION,"CONSTRUCTION"),(DELIVERY,"DELIVERY"))
      
      customer = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='member' ) # todo null=False
      in_charge = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='expert' ) # todo null=False
      # incharge = models.CharField(max_length=11,blank =False, null =False,default="DA1212-0", unique =  True) # MEMBER ID also serve as username of the customer
      status =   models.CharField(max_length=50)
      remarks =  models.CharField(max_length=300,default="In Progress")
      category = models.PositiveIntegerField(default =MOBILE, choices = CATEGORY_CODE)
      active =  models.BooleanField(default= False)

      
      
class JoinModel(models.Model):
    name = models.CharField(max_length=124)
    phone = models.CharField(max_length=124,blank= True,null =True)
    email= models.EmailField(max_length=254,blank= True,null =True)

    birthday = models.DateField(  blank= True, null =True)
    address =  models.CharField(max_length=300,blank =True, null =True)
    

    def __str__(self):
        return self.name

class DeliveryModel(models.Model):
    PASSPORT,DRIVER,SSS,POSTAL,TIN= (0,1,2,3,4)
    cat = ((PASSPORT,"Passport"),(DRIVER,'Driver Licence'),(SSS,'SSS/GSIS/UMID'),(POSTAL,'Postal ID'),(TIN, 'TIN ID' ))
    name = models.CharField(max_length=124,blank =False, null =False)
    phone = models.CharField(max_length=124 ,blank= True,null =True)
    address =  models.CharField(max_length=300,blank =False, null =False)
    email= models.EmailField(max_length=254,blank= True,null =True)
    recepient = models.CharField(max_length=124,blank =False, null =False)
    recepient_address = models.CharField(max_length=124,blank =False, null =False)
    recepient_phone = models.CharField(max_length=124 ,blank =True, null =True)
    message = models.CharField(max_length=300 ,blank =True, null =True)
    source_id = models.IntegerField(default =0) 
    
#     pickup =models.DateField(  blank= True, null =True)
#     identification =models.PositiveIntegerField(default = DRIVER ,choices = cat)
    
     

class MessageModel(models.Model):  #contact 
    name = models.CharField(max_length=124)
    email= models.EmailField(max_length=254,blank= True,null =True)
    message = models.CharField(max_length=300,blank= False,null =False)
    source_id = models.IntegerField(default =0) 

# ----------------  services --------------------
class ConstructionModel(models.Model):
       WORKER,MATERIAL,MASON,FOREMAN =(0,1,2,3)
       cat =((WORKER,"Worker"),(MATERIAL,"Materials"),(MASON,"Mason"),(FOREMAN,"Forman"))
       name = models.CharField(max_length=124)
       phone = models.CharField(max_length=124 ,blank= False,null =False)
       email= models.EmailField(max_length=254,blank= True,null =True)
       category = models.PositiveIntegerField(default = WORKER ,choices = cat)
       message =  models.CharField(max_length=300,blank= False,null =False)
       source_id = models.IntegerField(default =0) 

       
 
class MechanicModel(models.Model):
       AUTO,GENERAL =(0,1)
       cat =((AUTO,"AUTO MECHANIC"),(GENERAL,"GENERAL MECHANiC"))
       name = models.CharField(max_length=124)
       phone = models.CharField(max_length=124)
       email= models.EmailField(max_length=254,blank= True,null =True)
       address = models.CharField(max_length=300)
       category = models.PositiveIntegerField(default = AUTO ,choices = cat)
       description =  models.CharField(max_length=300)
       source_id = models.IntegerField(default =0) 

       

class RepairModel(models.Model):
       name = models.CharField(max_length=124)
       phone = models.CharField(max_length=124)
       email= models.EmailField(max_length=254,blank= True,null =True)
       description =  models.CharField(max_length=300)
       source_id = models.IntegerField(default =0) 
      
 
class LoadModel(models.Model):
    SMART,GLOBE,DITO,TALK,SUN =(0,1,2,3,4)
    cat =((SMART,"SMART"),(GLOBE,"GLOBE"),(DITO,"DITO"),(TALK,"TALK N TEXT"),(SUN,"SUN CELLULAR"))
    name = models.CharField(max_length=124)
    phone = models.CharField(max_length=124)
    carrier = models.PositiveIntegerField(default = SMART ,choices = cat) 
    email= models.EmailField(max_length=250,blank= True,null =True)
    amount = models.FloatField(default =0 )    
       





# ----------------  services end --------------------

class dayTransactionModel(models.Model):
   TX_PAYMENT,TX_LOAN_PAYMENT,TX_VENTURE,TX_TRANSACTION,TX_DEPOSIT,TX_WITHRAWAL,TX_GROCERY,TX_SERVICES=(0,1,2,3,4,5,6,7)
   cat =((TX_TRANSACTION,"REGULAR TRANSACTION"),(TX_PAYMENT,"PAYMENT"),(TX_VENTURE,"VENTURE"),(TX_DEPOSIT,"DEPOSIT"),(TX_WITHRAWAL,'WITHRAWAL'),(TX_GROCERY,'GROCERY'),(TX_SERVICES,'SERVICES'),(TX_LOAN_PAYMENT,"LOAN PAYMENT"))
   CASH,WALLET,SAVING=(0,1,2)
   source_type_cat =((CASH,"CASH"),(WALLET,"WALLET ACCOUNT"),(SAVING,"SAVING ACCOUNT"))
   ACCOUNT_SAVINGS,ACCOUNT_WALLET,ACCOUNT_CC,ACCOUNT_VENTURE,ACCOUNT_PAYMENT =(0,1,2,3,4)
   account_cat =((ACCOUNT_SAVINGS,"SAVING ACCOUNT"),(ACCOUNT_WALLET,"WALLET ACCOUNT"),(ACCOUNT_CC,"CC ACCOUNT"),(ACCOUNT_VENTURE,"VENTURE ACCOUNT"),(ACCOUNT_PAYMENT,"PAYMENT ACCOUNT"))

#    account_cat = source_type_cat =((CASH,"CASH"),(WALLET,"WALLET ACCOUNT"),(SAVING,"SAVING ACCOUNT"))
   category = models.PositiveIntegerField(default = 1 ,choices = cat)   
   customer = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='venture_customer' ) # todo null=False
   in_charge = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='venture_in_charge' ) # todo null=False

   date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
   source_type = models.IntegerField(default =CASH,choices = source_type_cat)  #c: cash,A Additional Loan, M max loan  
   amount = models.FloatField(default =0 )       
   source_id = models.IntegerField(default =0) 
   account_code =    models.PositiveIntegerField(default = 1 ,choices = account_cat)   

                                                                                                                                        


   

      

class IdRepositoryModel(models.Model):
    code =  models.CharField(max_length=8,unique =  True, blank =True, null =True)
    counter =  models.IntegerField(default =0) 

class LoanSummaryModel(models.Model):
    member = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL) # todo null=False
    date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
    max_loan = models.FloatField(verbose_name ="Max Loan", default =300 )
    percent = models.PositiveIntegerField(default =25)
    


    
class CcModel(models.Model):
  # amount,date_entered,description,transaction_type,Client
   REG_TRANSACTION,TRANSFER,GROCERY,SAVING_INTEREST,EARNED,LOAN,VENTURE,TRADE=(0,1,2,3,4,5,6,7)
   cat =((REG_TRANSACTION,"REGULAR TRANSACTION"),
        (TRANSFER,"TRANSFER"),(GROCERY,"GROCERY"),
        (SAVING_INTEREST,"SAVING_INTEREST"),(EARNED,"EARNED"),(LOAN,"LOAN"),(VENTURE,"VENTURE"),(TRADE,"TRADING"))
   DEPOSIT,WITHRAW =('D','W')
   t_type = ((DEPOSIT,"DEPOSIT"),(WITHRAW,"WITHRAW"))
   member = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL) # todo null=False
   description =models.CharField(max_length = 50, blank =True, null =True)
   date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
   transaction_type = models.CharField(max_length=1,blank =True,default = 'D', choices =t_type)  #Todo: false here
   debit = models.FloatField(verbose_name ="Amount to Cash Out", default =0 )
   credit = models.FloatField(verbose_name ="Amount to Cash In",default =0 )
   category = models.PositiveIntegerField(default = 0 ,choices = cat)  
   source_id = models.IntegerField(default =0) 
   class Meta:
      ordering = ['-id']
class VentureCcModel(models.Model):
  # amount,date_entered,description,transaction_type,Client
   REG_TRANSACTION,TRANSFER,GROCERY,SAVING_INTEREST,EARNED,LOAN =(0,1,2,3,4,5)
   cat =((REG_TRANSACTION,"REGULAR TRANSACTION"),
        (TRANSFER,"TRANSFER"),(GROCERY,"GROCERY"),
        (SAVING_INTEREST,"SAVING_INTEREST"),(EARNED,"EARNED"),(LOAN,"LOAN"))
   DEPOSIT,WITHRAW =('D','W')
   t_type = ((DEPOSIT,"DEPOSIT"),(WITHRAW,"WITHRAW"))
   member = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL) # todo null=False
   description =models.CharField(max_length = 50, blank =True, null =True)
   date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
   transaction_type = models.CharField(max_length=1,blank =True,default = 'D', choices =t_type)  #Todo: false here
   debit = models.FloatField(verbose_name ="Amount to Cash Out", default =0 )
   credit = models.FloatField(verbose_name ="Amount to Cash In",default =0 )
   category = models.PositiveIntegerField(default = 0 ,choices = cat)  
   source_id = models.IntegerField(default =0) 
   class Meta:
      ordering = ['-id']
 
class SavingModel(models.Model):
  # amount,date_entered,description,transaction_type,Client
   TRANSFER,LOAN,PAYMENT =(1,5,6)

   cat = ((TRANSFER,"TRANSFER"),(LOAN,"LOAN") ,(PAYMENT,"PAYMENT"))
   DEPOSIT,WITHRAW =('D','W')
   t_type = ((DEPOSIT,"DEPOSIT"),(WITHRAW,"WITHRAW"))
   member = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL) # todo null=False
   description =models.CharField(max_length = 50, blank =True, null =True)
   date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
   transaction_type = models.CharField(max_length=1,blank =True,default = 'D', choices =t_type)  #Todo: false here
   debit = models.FloatField(verbose_name ="Amount to Cash Out", default =0 )
   credit = models.FloatField(verbose_name ="Amount to Cash In",default =0 )
   category = models.PositiveIntegerField(default = 0 ,choices = cat) # 0 means  debit or
   source_id = models.IntegerField(default =0) 
   class Meta:
      ordering = ['-id']
class PaymentModel(models.Model):
  # amount,date_entered,description,transaction_type,Client
   LOAN,PAYMENT =(5,6)
   cat = ((LOAN,"LOAN") ,(PAYMENT,"PAYMENT"))
   DEPOSIT,WITHRAW =('D','W')
   t_type = ((DEPOSIT,"DEPOSIT"),(WITHRAW,"WITHRAW"))
   
   member = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL) # todo null=False
   #description =models.CharField(max_length = 50, blank =True, null =True)
   date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
   transaction_type = models.CharField(max_length=1,blank =True,default = 'D', choices =t_type)  #Todo: false here
   debit = models.FloatField(verbose_name ="Amount", default =0 )
   credit = models.FloatField(verbose_name ="Amount to Cash In",default =0 )
   category = models.PositiveIntegerField(default = 0 ,choices = cat) # 0 means  debit or
   source_id = models.IntegerField(default =0) 
   source_type = models.CharField(max_length=1,blank =True,default = 'C')  #c: cash,A Additional Loan, M max loan                                                                                                                                                 
   class Meta:
      ordering = ['-id']

class tmpVariables(models.Model):
       max_loan = models.FloatField(verbose_name ="Max loan allowrd",default =300) 
       
      
      

class PersonalLoanModel(models.Model):
   UNACCEPTED,ACCEPTED,BEING_EDITED,DONE_EDITING =(0,1,2,3)
   cat = ((UNACCEPTED,"UNACCEPTED") ,(ACCEPTED,"ACCEPTED"),(BEING_EDITED,"BEING_EDITED") ,(DONE_EDITING,"DONE_EDITING"))
   member = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL)  
   cc_loan = models.FloatField(verbose_name ="Community Coin(CC)",default =0) # or cc
   saving = models.FloatField(verbose_name ="Saving(Deposit)",default =0) 
  # description = models.CharField(max_length = 50, blank =True, null =True)
   percent = models.PositiveIntegerField(default =0)
   source_type = models.CharField(max_length=1,blank =True,default = 'C')  #c: cash
   source_id = models.IntegerField(default =0) # 0 - cash
   cc_id = models.IntegerField(default =0) # 0 - cash
   saving_id = models.IntegerField(default =0) # 0 - cash
   date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
   note_id = models.IntegerField(default =0) 
   flag = models.PositiveIntegerField(default = 0 ,choices = cat)
   class Meta:
      ordering = ['-id']
   
class PendingLoanModel(models.Model):
   loan_id = models.IntegerField(default =0) # 0 - cash
   cc_loan = models.FloatField(default =0) # or cc
   saving = models.FloatField(default =0) 
   percent = models.FloatField(default =0)
   source_type = models.CharField(max_length=1,blank =True,default = 'C')  #c: cash
   source_id = models.IntegerField(default =0) # 0 - cash
    
class NoteModel(models.Model):
   REG_TRANSACTION,LOAN,GROCERY,PAYMENT,TRADING =(0,1,2,3,7)
   cat = ((REG_TRANSACTION,"REGULAR TRANSACTION") ,(LOAN,"LOAN"),(GROCERY,"GROCERY"),(PAYMENT,"PAYMENT"),(TRADING,"TRADING"))
   source_id = models.IntegerField(default =0)
   note = models.TextField(max_length =300,blank =True,null=True,help_text='Enter note when necessary. Thank you')
   category = models.PositiveIntegerField(default = 0 ,choices = cat)
class WalletModel(models.Model):  
    
    REG_TRANSACTION,TRANSFER,GROCERY,LOAN,VENTURE,TRADE =(0,1,2,5,6,7)
    cat =((REG_TRANSACTION,"REGULAR TRANSACTION"),
        (TRANSFER,"TRANSFER"),(GROCERY,"GROCERY"),(LOAN,"LOAN"),(VENTURE,"VENTURE"),(TRADE,"TRADING"))
   #code: R - Refund, T- transfer,
    DEPOSIT,WITHRAW =('D','W')
    t_type =( (DEPOSIT,"DEPOSIT"),(WITHRAW,"WITHRAW"))
    member = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL)
    description =models.CharField( max_length = 50, blank =False, null =False)
    date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
    transaction_type = models.CharField(max_length=1,blank =True,choices=t_type)  #Todo: false here
   # code = models.CharField(max_length=1,default =' ')   #' ' means regular trans(cash in, out)   Todo: false here  
    debit = models.FloatField(verbose_name ="Amount to Cash Out", default =0 )
    credit = models.FloatField(verbose_name ="Amount Cash In",default =0 )
    category = models.PositiveIntegerField(default = 0 ,choices = cat) # 0 means  debit or credit in general
    source_id = models.IntegerField(default = 0) # > 0 linking to transfer,loan 
    
    class Meta:
      ordering = ['-id']
class VentureWalletModel(models.Model):  
    
    REG_TRANSACTION,TRANSFER,GROCERY,LOAN,VENTURE,TRADE =(0,1,2,5,6,7)
    cat =((REG_TRANSACTION,"REGULAR TRANSACTION"),
        (TRANSFER,"TRANSFER"),(GROCERY,"GROCERY"),(LOAN,"LOAN"),(VENTURE,"VENTURE"),(TRADE,"TRADING"))
   #code: R - Refund, T- transfer,
    DEPOSIT,WITHRAW =('D','W')
    t_type =( (DEPOSIT,"DEPOSIT"),(WITHRAW,"WITHRAW"))
    member = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL)
    
    description =models.CharField( max_length = 50, blank =False, null =False)
    date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
    transaction_type = models.CharField(max_length=1,blank =True,choices=t_type)  #Todo: false here
   # code = models.CharField(max_length=1,default =' ')   #' ' means regular trans(cash in, out)   Todo: false here  
    debit = models.FloatField(verbose_name ="Amount to Cash Out", default =0 )
    credit = models.FloatField(verbose_name ="Amount Cash In",default =0 )
    category = models.PositiveIntegerField(default = 0 ,choices = cat) # 0 means  debit or credit in general
    source_id = models.IntegerField(default = 0) # > 0 linking to transfer,loan

    class Meta:
      ordering = ['-id']
   

class UserPreferenceModel(models.Model):
      financial_transaction = models.PositiveIntegerField(default =5)
      user = models.ForeignKey(User,null =True, on_delete = models.SET_NULL)
      cash_transfer_nos_of_row = models.PositiveIntegerField(default =5)
      search_member = models.PositiveIntegerField(default =5)  #search member in general
      search_receiver = models.PositiveIntegerField(default =5) #use to search the member receiver
      transfer_receiver = models.PositiveIntegerField(default =5)
      transfer_history = models.PositiveIntegerField(default =5)
      claim_transfer = models.PositiveIntegerField(default =5)
class TransferModel(models.Model):
      UNACCEPTED,ACCEPTED,BEING_EDITED,DONE_EDITING =(0,1,2,3)
      cat = ((UNACCEPTED,"UNACCEPTED") ,(ACCEPTED,"ACCEPTED"),(BEING_EDITED,"BEING_EDITED") ,(DONE_EDITING,"DONE_EDITING"))
      WALLET,CC,SAVING =('W','C','S')
      sources =((WALLET,"WALLET"),
        (CC,"CC"),(SAVING,"SAVING"))
      sender = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='Cash_sender' ) # todo null=False
      receiver = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='Cash_receiver' ) # todo null=False
      status = models.CharField(max_length=1,blank =True,default ='W')  # W-wating,A - accepted , C - cancel #Todo: false here
      date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
      amount = models.FloatField(verbose_name ="Amount",blank =False,null =False)
      code = models.PositiveIntegerField(default =0)
      purpose =models.CharField(max_length=100,blank =True)
      source_type = models.CharField(max_length=1,default = 'W',choices = sources)  #c: cash
      source_id = models.IntegerField(default = 0)
      date_accounted = models.DateField(verbose_name ="Date", blank= True, null =True)
      flag = models.PositiveIntegerField(default = 0 ,choices = cat)

class NonCashTransferModel(models.Model):

      WALLET,CC,SAVING =(1,2,3)
      sources =((WALLET,"WALLET"),
        (CC,"CC"),(SAVING,"SAVING"))
      sender = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='Non_Cash_sender' ) # todo null=False
      receiver = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='Non_Cash_receiver' ) # todo null=False
      status = models.CharField(max_length=1,blank =True,default ='W')  # W-wating,A - accepted , C - cancel #Todo: false here
      date_entered = models.DateField(verbose_name ="Date", blank= True, null =True) #auto_now_add = True
      amount = models.FloatField(verbose_name ="Amount",blank =False,null =False)
      code = models.PositiveIntegerField(default =0)
      purpose =models.CharField(max_length=100,blank =True)
      source_type = models.PositiveIntegerField(default = 1,choices = sources)  #c: cash

class VentureModel(models.Model):
      REG_TRANSACTION,TRANSFER,GROCERY,LOAN,TRADE =(0,1,2,5,7)
      cat =((REG_TRANSACTION,"REGULAR TRANSACTION"),
        (TRANSFER,"TRANSFER"),(GROCERY,"GROCERY"),(LOAN,"LOAN"),(TRADE,"TRADE"))
      DEPOSIT,WITHRAW =('D','W')
      t_type =( (DEPOSIT,"DEPOSIT"),(WITHRAW,"WITHRAW"))
      UNACCEPTED,ACCEPTED,BEING_EDITED,DONE_EDITING =(0,1,2,3)
      flag_type = ((UNACCEPTED,"UNACCEPTED") ,(ACCEPTED,"ACCEPTED"),(BEING_EDITED,"BEING_EDITED") ,(DONE_EDITING,"DONE_EDITING"))
      CASH,WALLET,SAVING =('K','W','S')
      sources =((WALLET,"WALLET ACCOUNT"),
        (CASH,"CASH"),(SAVING,"SAVINGS ACCOUNT"))
      seller = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='Trading_Seller' ) # todo null=False
      customer = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='Trading_Customer' ) # todo null=False
      in_charge = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='in_charge' ) # todo null=False
      transaction_type = models.CharField(max_length=1,blank =True,choices=t_type)  #Todo: false here
      category = models.PositiveIntegerField(default = 2 ,choices = cat) # 0 means  debit or credit in general
      amount = models.FloatField(verbose_name ="PHP",blank =False,null =False)
      cc = models.FloatField(verbose_name ="CO. MONEY",default =0)
      percent = models.FloatField(default =95)
      source_type = models.CharField(max_length=1,default = 'K',choices = sources)  #c: cash
      customer_source_id = models.IntegerField(default = 0)
      seller_source_id = models.IntegerField(default = 0)
      customer_cc_id = models.IntegerField(default = 0)
      seller_cc_id = models.IntegerField(default = 0)
      date_entered = models.DateField(verbose_name ="Date", blank= True, null =True)
      flag = models.PositiveIntegerField(default = 0 ,choices = flag_type)
      note_id = models.IntegerField(default =0)
      @property
      def total_cost(self):
          return self.amount + self.cc
class Change_Table(models.Model):
      
       
      change = models.FloatField(verbose_name ="PHP",blank =False,null =False)
      destination_acct_id = models.IntegerField(default = 0) # > 0 linking to transfer,loan 
      venture = models.ForeignKey(VentureModel,null =True, on_delete =models.SET_NULL ) # todo null=False
      date_entered = models.DateField(verbose_name ="Date", blank= True, null =True)
      destination_acct_code = models.CharField(max_length=1,blank =True,default ='') #W wallet S:Saving
      #flag = models.PositiveIntegerField(default = 0 ,choices = flag_type)
      
      
    
class TradingModel(models.Model):
      BUYER_ROLE,SELLER_ROLE =('B','S')
      roles =((BUYER_ROLE,"BUYER"),(SELLER_ROLE,"SELLER"))
      REG_TRANSACTION,TRANSFER,GROCERY,LOAN,TRADE =(0,1,2,5,7)
      cat =((REG_TRANSACTION,"REGULAR TRANSACTION"),
        (TRANSFER,"TRANSFER"),(GROCERY,"GROCERY"),(LOAN,"LOAN"),(TRADE,"TRADE"))
      DEPOSIT,WITHRAW =('D','W')
      t_type =( (DEPOSIT,"DEPOSIT"),(WITHRAW,"WITHRAW"))
      UNACCEPTED,ACCEPTED,BEING_EDITED,DONE_EDITING =(0,1,2,3)
      flag_type = ((UNACCEPTED,"UNACCEPTED") ,(ACCEPTED,"ACCEPTED"),(BEING_EDITED,"BEING_EDITED") ,(DONE_EDITING,"DONE_EDITING"))
      CASH,WALLET,SAVING =('K','W','S')
      sources =((WALLET,"WALLET ACCOUNT"),
        (CASH,"CASH"),(SAVING,"SAVINGS ACCOUNT"))
      seller = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='Seller' ) # todo null=False
      customer = models.ForeignKey(MemberModel,null =True, on_delete =models.SET_NULL,related_name='Customer' ) # todo null=False
      transaction_type = models.CharField(max_length=1,blank =True,choices=t_type)  #Todo: false here
      role_type =models.CharField(max_length=1,default = BUYER_ROLE,choices = roles) 
      category = models.PositiveIntegerField(default = TRADE ,choices = cat) # 0 means  debit or credit in general
      amount = models.FloatField(verbose_name ="AMOUNT",blank =False,null =False)
      customer_source_id = models.IntegerField(default = 0)
      seller_source_id = models.IntegerField(default = 0)
      cc = models.FloatField(verbose_name ="CC",default =0)
      percent = models.FloatField(default =95)
      source_type = models.CharField(max_length=1,default = CASH,choices = sources)  #c: cash
      customer_cc_id = models.IntegerField(default = 0)
      seller_cc_id = models.IntegerField(default = 0)
      date_entered = models.DateField(verbose_name ="Date", blank= True, null =True)
      flag = models.PositiveIntegerField(default = 0 ,choices = flag_type)
      note_id = models.IntegerField(default =0)
      @property
      def total_cost(self):
          return self.amount + self.cc
      
class Tmp_UsernameModel(models.Model):
   username =models.CharField(max_length=50,blank= True, null =True)
   code_counter = models.PositiveIntegerField()


class Tmp_PasswordModel(models.Model):
    pwd = models.CharField(max_length=12,blank =False, null =False)
    qrcode_pwd = models.CharField(max_length=12, null =False,default="")
    member_id =models.IntegerField()
    date_entry =models.DateField(auto_now_add = True)

 



 









