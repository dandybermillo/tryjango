"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#from  products.views import homepage_view,client_create_view,client_update_view,saving_create_view
 
urlpatterns = [
    path('', include('fx.urls')),
   
    # path('', bases.html),
    #path('create/', client_create_view),
    path('admin/', admin.site.urls),
  
    path('accounts/', include('django.contrib.auth.urls')),
    
]
 