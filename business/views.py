from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.urls import reverse_lazy
from .models import Business
from shop.models import Product, Category, OrderDetail
import datetime
from django.contrib.admin.views.decorators import staff_member_required,user_passes_test


# Create your views here.
def home(request):
    return HttpResponse("<a href='/business/productregister'>Product Register</a>")

def register(request):
    if request.method == 'POST':
        name = request.POST['business_name']
        seller = request.POST['seller_name']
        number = request.POST['contact_number']
        password = request.POST['password']
        email = request.POST['email_address']
        service = request.POST['service_area']
        service_desc = request.POST['service_description']
        home_delivery = request.POST['home_delivery_available']

        if User.objects.filter(username=number).exists():
            messages.info(request, 'Already Registered')
            return redirect('/business/register')

        else:    
            user = User.objects.create_user(username = number, password = password, email = email, first_name = name, is_staff = True)
            user.save()
            user = auth.authenticate(username = number, password=password)
            auth.login(request, user)

            business = Business(business_name = name, seller_name = seller, credential = user, business_mobile = number, business_email = email, servicable_area=service, service_discription = service_desc, delivery_avail = home_delivery)
            business.save()
            messages.info(request, 'Account Registered Successfully, Thanks for registering')
            return redirect('/business/productregister')

    else:
        return render(request, 'business/business_signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['login_contact_number']
        password = request.POST['business_login_password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Welcome!')
            return redirect('/business/registeredproduct')

        else:
            messages.info(request, 'Invailid Username or Password')
            return redirect('/business/register') 

    else:
      return redirect('business/register')

@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('register'))
def productRegister(request):
    if request.method == "POST":
        name = request.POST['cat']
        product = request.POST['product_name']
        desc = request.POST['product_description']
        price = request.POST['product_price']
        quantity = request.POST['product_quantity']
        discount = request.POST['product_discount']
        img1 = request.FILES['img1']
        img2 = request.FILES['img2']
        img3 = request.FILES['img3']
        
        catObj = Category.objects.filter(category_id = name)
        catObj = catObj[0]
        newprod = Product(product_name=product, product_category=catObj, product_desc=desc, product_price=price, product_discount=discount, product_stock=quantity, product_owner=request.user, product_img_1=img1, product_img_2=img2, product_img_3=img3)
        newprod.save()
        messages.info(request, 'Your Product Successfully Registered')
        return redirect('/business/productregister')

    else:
        return render(request, 'business/product_register.html')

@staff_member_required(login_url='/business/register')
def registerdProduct(request):
    product = Product.objects.filter(product_owner=request.user)
    param = {'prod':product}
    return render(request, 'business/seller_products.html', param)

@staff_member_required(login_url='/business/register')
def deleteProduct(request, id):
    delProd = Product.objects.get(product_id=id)
    delProd.delete()
    messages.info(request, 'Product Deleted')
    return redirect('/business/registeredproduct/')

@staff_member_required(login_url='/business/register')
def account(request):
    account = Business.objects.get(credential=request.user)
    param = {'account':account}
    return render(request, 'business/business_account.html', param)        

@staff_member_required(login_url='/business/register')
def update(request):
    if request.method == "POST":
        accUpdate = Business.objects.get(credential=request.user)
        
        accUpdate.business_name = request.POST['business_name_change']
        accUpdate.business_mobile = request.POST['contact_number_change']
        accUpdate.business_email = request.POST['email_address_change']
        accUpdate.servicable_area = request.POST['service_area']
        accUpdate.service_description_change = request.POST['service_description_change']
        accUpdate.delivery_avail = request.POST['home_delivery_change']
        accUpdate.save()

        useracc = User.objects.get(id=request.user.id)
        useracc.first_name = request.POST['business_name_change']
        useracc.save()

        messages.info(request, 'Account Updated Successfully')
        
    return redirect('/business/account/')

@staff_member_required(login_url='/business/register')
def ongoingorder(request):
    order = OrderDetail.objects.filter(product__product_owner=request.user)
    param = {'orders':order}
    return render(request, 'business/ongoing_orders.html', param)
    
@staff_member_required(login_url='/business/register')    
def pastorder(request):
    order = OrderDetail.objects.filter(product__product_owner=request.user)
    param = {'orders':order}
    return render(request, 'business/past_orders.html', param)    