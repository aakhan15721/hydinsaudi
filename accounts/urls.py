from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),


    path('agent/', views.agent, name='agent'),
    path('Agent/', views.Agent, name='Agent'),    
    path('contactus/', views.contactus, name='contactus'),

    
#    path('custDashboard/', views.custDashboard, name='custDashboard'),
#    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('contactusactivate/<uidb64>/<token>/', views.contactusactivate, name='contactusactivate'),
    


    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('sendmail', views.sendmail, name='sendmail'),

    path('vendor/', include('vendor.urls')),
#    path('customer/', include('customers.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)