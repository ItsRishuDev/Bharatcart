from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from shop.models import Product, Category, Cart, Address, OrderDetail, Contact
from django.contrib.auth.decorators import login_required
import razorpay

# Create your views here.

def index(request):
    category = Category.objects.all()
    product = Product.objects.all()
    allProds=[]
    catprods = Product.objects.values('product_category', 'product_id')
    cats = {item['product_category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_category=cat)
        allProds.append(prod)   
    param = {'product':product, 'allProduct':allProds, 'category':category}
    return render(request, 'shop/index.html', param)

def searchMatch(query, item):
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.product_category.category_name.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search').lower()
    allProds=[]
    catprods = Product.objects.values('product_category', 'product_id')
    cats = {item['product_category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(product_category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        if len(prod)!=0:    
            allProds.append(prod)

    param = {'allProduct':allProds}
    if len(allProds) == 0:
        messages.info(request, 'Product not found. Please try another.')

    return render(request, 'shop/search.html', param)

def login(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            username = request.POST['mob_number']
            password = request.POST['login_password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.info(request, 'Welcome!')
                return redirect('/')

            else:
                messages.info(request, 'Invailid Username or Password')
                return redirect('/login') 

        else:
            return render(request, 'shop/login.html')
    else:
        messages.info(request, 'Already Login')
        return redirect('/')                   

def signup(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            name = request.POST['signup_name']
            number = request.POST['signup_mobile_number']
            email = request.POST['signup_email_address']
            password = request.POST['signup_password']

            if User.objects.filter(username=number).exists():
                messages.info(request, 'Already Registered')
                return redirect('/signup')

            else:    
                user = User.objects.create_user(username = number, password = password, email = email, first_name = name)
                user.save()
                print('User added')
                messages.info(request, 'Account Created Successfully')
                return redirect('/login')

        else:
            return render(request, 'shop/register.html')
    else:
        return redirect('/logout')          

def logout(request):
    auth.logout(request)
    messages.info(request, 'Thank You, Come Again')
    return redirect('/login')

def deleteuser(request):
    userdata = User.objects.filter(id = request.user.id)
    userdata.delete()
    return redirect('/signup')

def productdetail(request, id):
    product = Product.objects.get(product_id=id)
    cat = product.product_category
    prodcat = Product.objects.all().filter(product_category=cat)
    param = {'product':product, 'prodcat':prodcat}
    return render(request, 'shop/productdetail.html', param)

def product(request):
    category = Category.objects.all()
    product = Product.objects.all()
    param = {'product':product, 'category':category}
    return render(request, 'shop/products.html', param)

def catProduct(request, id):
    cat = Category.objects.get(category_id=id)
    catProd = Product.objects.filter(product_category=cat)
    param = {'product':catProd, 'category':cat.category_name}
    return render(request, 'shop/category.html', param)

@login_required(login_url='/login')
def cart(request):
    item = Cart.objects.all().filter(user_id=request.user)
    price = 0
    for products in item:
        price += products.prod_id.product_price * products.quantity

    tax = (price/100)*10
    price = price - tax
    total = price + tax
    param = {'cartitem' : item, 'subtotal':price, 'tax':tax, 'total':total}
    return render(request, 'shop/cart.html', param)

@login_required(login_url='/login')
def addcart(request, id):
    prod = Product.objects.filter(product_id = id)
    addprod = prod[0]
    productavail = Cart.objects.filter(user_id=request.user, prod_id=addprod.product_id)
    if productavail.exists():
        prodincrease = productavail[0].quantity
        prodincrease += 1
        productavail.update(quantity= prodincrease)
    else:    
        add = Cart(prod_id=addprod, user_id=request.user)
        add.save()
    messages.info(request, 'Product Added to the cart')    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def remove(request, id):
    removeitem = Cart.objects.filter(cart_id = id)
    if removeitem[0].quantity > 1:
        quant = removeitem[0].quantity
        removeitem.update(quantity= quant-1)
    else:
        removeitem.delete()
    messages.info(request, 'Cart Updated')     
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def useraccount(request):
    userdetail = request.user
    addressdetail = Address.objects.filter(user=userdetail)

    if request.method == "POST":
        name = request.POST['user_name']
        email = request.POST['user_email']
        street = request.POST['address_street']
        city = request.POST['address_city']
        state = request.POST['address_state']
        pincode = request.POST['address_zip']

        userdetail = User.objects.filter(id= request.user.id)
        userdetail.update(first_name=name, email=email)
        if addressdetail.exists():
            addressdetail.update(address=street, city=city, state=state, pincode=pincode)
        else:
            newaddress = Address(user=userdetail, address=street, state=state, city=city, pincode=pincode)

        messages.info(request, 'Account Updated Successfully')    
        return redirect('/useraccount')

    if addressdetail.exists():
        param = {'user':userdetail, 'address':addressdetail[0]}
        return render(request, 'shop/user_account.html', param)
    else:
        param = {'user':userdetail}
        return render(request, 'shop/user_account.html', param)    

@login_required(login_url='/login')
def userorder(request):
    orders = OrderDetail.objects.all().filter(user=request.user)
    for order in orders:
        print('The order we get from the order table :', order.product_id)
        print('The order type we get from the order table :', type(order.product_id))
    param = {'orders': orders}
    return render(request, 'shop/user_orders.html', param)

@login_required(login_url='/login')
def checkout(request):
    cartitem = Cart.objects.filter(user_id=request.user)
    total = 0
    
    for item in cartitem:
        price = item.prod_id.product_price * item.quantity
        total += price

    address = Address.objects.filter(user=request.user)
    if address.exists():
        print(address[0])
        param = {'cartitem':cartitem, 'itemprice':price, 'total':total, 'address':address[0]}
        return render(request, 'shop/checkout.html', param)
   
    param = {'cartitem':cartitem, 'itemprice':price, 'total':total}
    return render(request, 'shop/checkout.html', param)

@login_required(login_url='/login')
def payment(request):
    if request.method == 'POST':
        name = request.POST['name']
        address_info = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        email = request.POST['email']
        phone = request.POST['number']

        addressdetail = Address.objects.filter(user=request.user)
        if addressdetail.exists():
            addressdetail.update(address=address_info, pincode=pincode, city=city, state=state)
        else:
            newaddress = Address(address=address_info, pincode=pincode, city=city, state=state, user=request.user)
            newaddress.save()

        address = Address.objects.get(user=request.user)
        cartitem = Cart.objects.filter(user_id=request.user)
        total = 0    
        for item in cartitem:
            price = item.prod_id.product_price * item.quantity
            total += price 
        payable = total * 100
        client = razorpay.Client(auth = ('rzp_test_6iZwqZQC0lQyam', 'v7T4GZUKDvHpT6ctGR61Da6J'))
        order_amount = payable
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        payment = client.order.create({'amount':order_amount, 'currency':order_currency, 'receipt':order_receipt})
        identity = payment['id']
        print(payment)
        for item in cartitem:
            addedprod = Product.objects.filter(product_id = item.prod_id.product_id)
            print('Data we entered in the order table : ', addedprod[0])
            print('Data type we entered in the order table : ', type(addedprod[0]))
            newOrder = OrderDetail(product= addedprod[0], payment_id=payment['id'] ,user=item.user_id, address=address, name=name, phone=phone, email=email, quantity=item.quantity)
            newOrder.save()
        cartitem.delete()
        param = {'itemprice':price, 'payable':payable, 'payment':payment, 'identity':identity, 'name':name, 'email':email, 'phone': phone}
        return render(request, 'shop/payment.html', param)
     
    else:
        return redirect('/')
           
@login_required(login_url='/login')
def success(request, order_id):
    users = OrderDetail.objects.filter(payment_id=order_id)
    for order in users:
        order.paid = True
        order.save()   
    return render(request, 'shop/thankyou.html')
    
def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['visitor_name']
        email = request.POST['visitor_email']
        number = request.POST['visitor_number']
        subject = request.POST['visitor_subject']
        message = request.POST['visitor_message']

        detail = Contact(contact_name=name, contact_email=email, contact_number=number, contact_subject=subject, contact_message=message)
        detail.save()
        messages.info(request, 'Thank You for Contacting Us. We will reach you soon.')
        return redirect('/') 

    return render(request, 'shop/contact.html')

@login_required(login_url='/login')
def cod(request):
    return render(request, 'shop/thankyou.html')
