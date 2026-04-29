from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.check, name='checkout'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('process_Order/', views.processOrder, name='process_Order'),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('watch/<int:id>/', views.watch_detail, name='watch_detail'),
    
    
]
