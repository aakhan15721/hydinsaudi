from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.expads, name='expads'),
    path('category/<slug:slug>/', views.expads, name='expads_by_category'),
    path('expatad/<int:id>/', views.expataddetail, name='expataddetail'),
    path('<int:id>/', views.deletead, name='deletead'),
    path('update/<int:id>/', views.updatead, name='updatead'),
    path('delete/<int:id>/', views.delete_ad, name='delete_ad'),
    path('edit_ad/<int:id>/', views.edit_ad, name='edit_ad'),



    #path('<slug:slug>/', views.store, name='products_by_category'),
    #path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    #path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    #path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('addads/', views.addads, name='addads'),
    path('placeads/', views.placeads, name='placeads'),
    path('contactme/', views.contactme, name='contactme'),
    path('contactyou/', views.contactyou, name='contactyou'),
    path('contactmes/', views.contactmes, name='contactmes'),
    path('interested/<int:id>/', views.interested, name='interested'),

    path('cities/', views.cities, name='cities'),
    #path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX

]