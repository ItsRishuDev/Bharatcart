from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='AboutUs'),
    path('contact/', views.contact, name='ContactUs'),
    path('useraccount/', views.useraccount, name='useraccount'), 
    path('userorders/', views.userorder, name='userorder'), 
    path('search/', views.search, name='Search'), 
    path('product/', views.product, name='Product'), 
    path('productdetail/<int:id>', views.productdetail, name='ProductView'),
    path('category/<int:id>', views.catProduct, name='catProduct'),
    path('checkout', views.checkout, name='Checkout'),
    path('addcart/<int:id>', views.addcart, name='addCart'),
    path('cart/', views.cart, name='cart'),
    path('remove/<int:id>', views.remove, name='remove'),
    path('payment/', views.payment, name = 'payment'),
    path('success/<str:order_id>', views.success, name = 'success'),
    path('cod', views.cod, name='cod'),
    path('deleteuser', views.deleteuser, name='deleteuser')
]