
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('account/<int:account_id>/', views.account_details, name='account_details'), # this is for the account details, used to illustrate the third flaw (broken access control)
    
]