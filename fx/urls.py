from django.urls import path,include
from . import views,user_views
from  . views import AjaxHandlerView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = 'fx'
urlpatterns = [
   # ------------- jquery ajax call ------------------
 
     path('reset_show_password/', views.reset_show_password, name = "reset_show_password_url"),
     path('search_receiver/', views.search_receiver, name = "search_receiver_url"),
     path('update_user_preference/', views.update_user_preference, name = "update_user_preference_url"),
     path('Transfer_check_balance/', views.Transfer_check_balance, name = "Transfer_check_balance_url"),
     path('update_transfer_status/', views.update_transfer_status, name = "update_transfer_status_url"),
     path('get_balances/', views.get_balances, name = "get_balances_url"),
     
     path('get_loan_details/', views.get_loan_details, name = "get_loan_details_url"),
     path('get_source_details/', views.get_source_details, name = "get_source_details_url"),
     path('get_transfer_details/', views.get_transfer_details, name = "get_transfer_details_url"),
     path('get_payment_details/', views.get_payment_details, name = "get_payment_details_url"),
     #path('get_customer_details/', views.get_customer_details, name = "get_customer_details_url"),
     path('get_customer_details/', views.get_customer_details, name = "get_customer_details_url"),
     path('check_user/', views.check_user, name = "check_user_url"),#must be removed


     

     path('finance_load_more/', views.finance_load_more, name = "finance_load_more_url"),
     path('Transfer_load_more/', views.Transfer_load_more, name = "Transfer_load_more_url"),
     path('data_load_more/', views.data_load_more, name = "data_load_more_url"),
   ## --------- RECEIVER ----------------
    
  path('transfer/<str:account_name>/<int:sender>/',views.transfer, name = 'transfer_url'),
  path("dashboard/", views.dashboard, name="dashboard_url"),
  path("dash/<str:message>", views.dash, name="dash_url"),
  
      ## -------------------- SERVICES --------------------
  path("services/<int:id>/", views.services, name="services_url"),

  

  path('',views.my_home_page,name= "home_page_url"),

 # path("person_list/", views.person_list,name ="person_list"),

       # ------ user authentication-----
  path('fx/accounts/', include('django.contrib.auth.urls')),
  path('login/', views.login_request, name="login"),
  path("logout/", LogoutView.as_view(), name="logout"),
  path("staff_logout/",views.staff_logout_request, name="staff_logout_url"),
  path("staff_admin/",views.admin, name="staff_admin_url"),
  path("user_logout/",views.user_logout_request, name="user_logout_url"),

  
   # --------------- store authentication staff -----------------
  path('venture_login/', views.venture_login_request, name="venture_login_url"),

   #------------------- Loan ------------------------- 
  path('loan_application/<int:member_id>/<int:loan_id>/', views.loan_application, name = "loan_application_url"), #0 - new,1 edit
  
      #  -------------------------redirect-------------------------

  path('success/transfer/<int:sender>/<int:code>/', views.success_transfer, name="success_transfer_url"),
  path('success/create_update_result/<str:account_name>/<int:id>/<int:account_id>/<str:msg>', views.create_update_result, name="create_update_result_url"),
  path('success/create_update_member_result/<int:id>/<str:msg>', views.create_update_member_result, name="create_update_member_result_url"),
  path('success/create_update_loan_result/<int:id>/<int:loan_id>/<str:msg>', views.create_update_loan_result, name="create_update_loan_result_url"),
  path('success/create_update_payment_result/<str:account_name>/<int:id>/<int:payment_id>/<str:msg>', views.create_update_payment_result, name="create_update_payment_result_url"),
  path('success/payment_venture_result/<str:account_name>/<int:id>/<int:payment_id>/<str:msg>', views.payment_venture_result, name="payment_venture_result_url"),
  path('success/create_update_venture_result/<int:member_id>/<int:venture_id>/<str:msg>/<str:request_action>/', views.create_update_venture_result, name="create_update_venture_result_url"),
  path('success/finance_venture_result/<str:account_name>/<int:id>/<int:account_id>/<str:msg>', views.finance_venture_result, name="finance_venture_result_url"),
  
  # -------------------------------- user ----------------------------
  path('index/', views.main_page_request, name = "main_page_url"), 

  # path('success/payment_venture_result/<int:member_id>/<int:venture_id>/<str:msg>/<str:request_action>/', views.payment_venture_result, name="payment_venture_result_url"),


  #test
    path('demo/',AjaxHandlerView.as_view(), name='AjaxHandlerView_url'),
    path('create/',views.create_post, name='create_url'),
    
    



#user login or sign in
  path('sign-in/', views.LoginView.as_view(), name="sign_in"), 
  path('user/<int:id>/', views.user_login_success, name="user_login_success_url"), 
  
  
  path('post_test/', views.pos_test.as_view(), name = "post_test_url"), 

  path('po/', views.po, name = "po_url"), 

  path('process-form/', views.Process_Data_View.as_view(), name="process_form_url"), 
  # path('mobile/', views.MobileView.as_view(), name="mobile_url"), 
  # path('message/', views.MessageView.as_view(), name="message_url"), 


  path('live/<int:id>/<int:code>/', views.livePost, name="live_url"), 
  path('live_services/', views.livePost_services, name="live_services_url"), 

  
  path('my_task/<int:id>/', views.worker_task, name="worker_task_url"), 

   
  #end test


       # -------------- user profiles -------------------
  path("unauthorized_user/", views.unauthorized_user, name="unauthorized_user_url"),
  path('member/<int:id>/', views.display_member_info, name='display_member_info_url'),
  path('create_update/<int:id>/',views.create_update_member, name='create_update_member_url'),
  
  path("services/", user_views.services, name="services_url"),
  path("contact/", user_views.contact, name="contact_url"),
 # path("join/", user_views.join, name="join_url"),
  path("about/", user_views.about, name="about_url"),
  
  path('join/', user_views.join, name='join_url'),
  
  
  path("user_dashboard/<int:id>/", user_views.user_dashboard, name="user_dashboard_url"),

  
  #--------WALLET------------ 
  path('create_update_member_finance/<str:account_name>/<int:member_id>/<int:account_id>/<str:transType>/',views.create_update_member_finance, name='create_update_member_finance_url'),
  
  #---------PAYMENT--------------
  path('payment/<int:member_id>/<int:payment_id>/',views.create_update_payment, name='create_update_payment_url'),

  #-------------------- VENTURE ------------------------
  path('pos/<int:customer_id>/<int:venture_id>/', views.create_update_venture, name = "create_update_venture_url"), 
  
  path('pos1/<int:customer_id>/<int:venture_id>/', views.create_update_venture1, name = "create_update_venture_url1"), 

  path('post_test/', views.pos_test.as_view(), name = "post_test_url"), 
  path('get_pos/', views.get_pos, name = "get_pos_url"),   #ajax call to get  pos transactions

  path('delete_venture/<int:member_id>/<int:venture_id>/<str:request_action>/', views.delete_venture, name = "delete_venture_url"), 
  path('venture_main_request/', views.venture_main_request, name = "venture_main_request_url"), 
  path('payment/<int:member_id>/<int:payment_id>/',views.payment_venture, name='payment_venture_url'),
  path('finance/<str:account_name>/<int:member_id>/<int:account_id>/<str:transType>/',views.finance_venture, name='finance_venture_url'),


# athenticate  user
path(
        'change_password/',
        auth_views.PasswordChangeView.as_view(
            template_name='fx/users/main/change_password.html',
            success_url = '/'
        ),
        name='change_password_url'
    ),
  
]