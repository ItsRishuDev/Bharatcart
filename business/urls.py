from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('register/', views.register, name='register'),
    path('productregister/', views.productRegister, name='productRegister'),
    path('registeredproduct/', views.registerdProduct, name='registerdProduct'),
    path('delete/<int:id>', views.deleteProduct, name='deleteProduct'),
    path('account/', views.account, name='account'),
    path('ongoingorder', views.ongoingorder, name='account'),
    path('pastorder', views.pastorder, name='pastorder'),
    path('update', views.update, name='update'),
    path('login',views.login, name='sellerlogin'),
]