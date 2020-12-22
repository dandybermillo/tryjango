from django.contrib.auth.decorators import login_required


from fx.models import WalletModel,MemberModel
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MemberForm  
from django.contrib import messages
from .views import get_user_preference
from .tables import myTable


def services(request):
         context ={'message':" Services offered"}
         return render(request, "fx/users/Services.html", context) 
def contact(request):
         context ={'message':" Contact US"}
         return render(request, "fx/users/Contact.html", context) 


