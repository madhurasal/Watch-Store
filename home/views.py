from home.utils import cookieCart
from .models import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import CreateUserForm


# Create your views here.

def index(request):
    return render(request, 'ecom/index.html')

def about(request):
    return render(request, 'ecom/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name= name, phone= phone, desc= desc)
        contact.save()
    return render(request, 'ecom/contact.html')

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order ,created = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items= []
        order= {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems= order['get_cart_items']

        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}    
        print('Cart:', cart)
        items= []
        order= {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems= order['get_cart_items']

        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'image.url':product.image.url,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
                items.append(item)


                if product.digital == False:
                    order['shipping'] = True
            except:
                pass        

    products = Product.objects.all()
    context = {'products': products, 'cartItems':cartItems}
    return render(request, 'ecom/store.html', context)  

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order ,created = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}    
        print('Cart:', cart)
        items= []
        order= {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems= order['get_cart_items']

        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'image.url':product.image.url,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
                items.append(item)


                if product.digital == False:
                    order['shipping'] = True
            except:
                pass        

    context= { 'items':items, 'order':order,'cartItems':cartItems }    
    return render(request, 'ecom/cart.html', context) 

def check(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order ,created = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        #create empty cart for noon-logged in user
        order= {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        items= []
        cartItems= order['get_cart_items']

        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}    
        print('Cart:', cart)
        items= []
        order= {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems= order['get_cart_items']

        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'image.url':product.image,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
                items.append(item)


                if product.digital == False:
                    order['shipping'] = True
            except:
                pass        

    context= { 'items':items, 'order':order, 'cartItems':cartItems } 
    return render(request, 'ecom/check.html', context)   



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete() 

    return JsonResponse('Item was added', safe=False)

#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order ,created = Order.objects.get_or_create(customer= customer, complete= False)
       

          
    else:
        print('User is not logged in') 

        print('COOKIES:', request.COOKIES)
        name = data['form']['name'] 
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']  

        customer, created = Customer.objects.get_or_create(
            email=email,
        )
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer=customer,
            complete = False,

        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = item['quantity']
            )
    

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()


    if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )  
    return JsonResponse('Payment Completed...', safe=False)   



def watch_detail(request, id):
    
    product = Product.objects.get(id = id)
    print(product)
   
    return render(request, 'ecom/view.html', {'product':product})  

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'ecom/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'ecom/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

