from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from .utils import cartData,cookieCart,guestOrder
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

# Create your views here.


def store(request):

   
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products,'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem , created= Order_item.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse("Item was added", safe=False)



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
         customer,order = guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
            order.complete = True
    order.save()

    if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city= data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
    return JsonResponse('Payment submitted....',safe=False)

# def register(request):
#     try:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             password = request.POST.get('password')

#         try:
#             if User.objects.filter(username=username).first():
#                 messages.success(request,'Username is taken')
#                 return redirect('store')
#             if User.objects.filter(email=email).first():
#                 messages.success(request,'Email is already taken')
#                 return redirect ('login')

#             user_obj = User(username = username,password=password)
#             user_obj.set_password(password)
#             user_obj.save()

#             profile_obj = Profile.objects.create(user = user_obj)
#             profile_obj.save()
#             return redirect('store')

#         except Exception as e:
#             print(e)
#     except Exception as e:
#         print(e)
#     return render(request,'store/register.html')

# def loginpage(request):
#     if request.user.is_authenticated:
#         return redirect('store')
#     else:
#         if request.method  == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             print(username)
#             print(password)
#             user = authenticate(request,username=username,password=password)


#             if user is not None:
#                 login(request,user)
#                 return redirect('store')
#             else:
#                 messages.info(request,'Username and password incorrect')

#     context  = {}
#     return render(request,'store/login.html',context)

