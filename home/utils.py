from functools import total_ordering
import json
from .models import *


def cookieCart(request):
    #order= {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    #items= []
    #cartItems= order['get_cart_items']
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart:', cart)
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

            def __getitem__(self, items):
                print(type(items), items)

            if product.digital == False:
                order['shipping'] = True

        except:
             pass  
    return{'cartItems':cartItems, 'order':order, 'items':items}                 

    
               