from django.shortcuts import render,redirect
from dishes.models import *
from cart.models import *

import random
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def IndexView(request):
    menuItems = MenuItemsModel.objects.all()
    specials = MenuItemsModel.objects.filter(sale_status = "Sale")
    popular_dishes = MenuItemsModel.objects.filter(popular_status = "Popular")
    hero_dish = MenuItemsModel.objects.get(sale_status = "Hero")

    currentUser = request.session.get('currentUser')
    if currentUser != "":
        cartOrders = CartModel.objects.filter(Q(currentUser = currentUser) & Q(status = "Cart"))
        cartCount = 0
        for i in cartOrders:
            cartItems = i.items.all().count()
            cartCount = cartCount + cartItems
    else:
        cartCount = 0
    
    session_order = request.session.get('session_order')

    if session_order != None:
        order_number = request.session.get('session_order')
    else:
        ref_number = random.randrange(100, 10000)
        order_number = 'ORD' + str(ref_number)
        request.session['session_order'] = order_number


    if request.method == 'POST' and 'add_to_cart' in request.POST:
        quantity = int(request.POST.get('quantity'))
        itemID = request.POST.get('itemID')
        menuItem = MenuItemsModel.objects.get(id = itemID)
        item_ingredients = menuItem.item_ingredients.all()

        # cart item views start 
        if menuItem.sale_status in ["Sale", "Hero"]:
            price = menuItem.sale_price
        else:
            price = menuItem.price

        # ******************* check if user has items in cart ***********************************
        currentUser = request.POST.get('currentUser')
        request.session['currentUser'] = currentUser
        
        if CartModel.objects.filter(Q(currentUser = currentUser) & Q(status = "Cart")).exists():
            updateCart = CartModel.objects.get(orderNumber = order_number )

            # create Cart Item
            subTotal = 0 
            for _ in range(quantity):
                save_item = CartItemsModel()
                save_item.orderNumber = order_number
                save_item.item = menuItem
                save_item.sold_price = price 
                save_item.save() 
                
                for ingredient in item_ingredients:
                    save_ingredient = ItemIngredientsModel()
                    save_ingredient.orderNumber = order_number
                    save_ingredient.item = ingredient
                    save_ingredient.save()
                    save_item.item_ingredients.add(save_ingredient)
                    save_item.save()
                # update cart items many to many 
                updateCart.items.add(save_item)
                subTotal = subTotal + save_item.sold_price

            updateCart.sub_total = updateCart.sub_total + subTotal
            updateCart.total = updateCart.sub_total + updateCart.delivery_fee
            updateCart.save()

        else:
            ref_number = random.randrange(100, 10000)
            new_order = 'ORD' + str(ref_number)
            request.session['session_order'] = new_order
            

             # user order views start
            addCart = CartModel()
            addCart.currentUser = currentUser
            addCart.orderNumber = new_order
            addCart.delivery_fee = 50
            addCart.status = "Cart" 
            addCart.save()

            # create Cart Item
            subTotal = 0 
            for _ in range(quantity):
                save_item = CartItemsModel()
                save_item.orderNumber = new_order
                save_item.item = menuItem
                save_item.sold_price = price 
                save_item.save() 

                for ingredient in item_ingredients:
                    save_ingredient = ItemIngredientsModel()
                    save_ingredient.orderNumber = new_order
                    save_ingredient.item = ingredient
                    save_ingredient.save()
                    save_item.item_ingredients.add(save_ingredient)
                    save_item.save()
                    
                addCart.items.add(save_item)
                subTotal = subTotal + save_item.sold_price

            addCart.sub_total = subTotal
            addCart.total = subTotal + addCart.delivery_fee
            addCart.save()



        # request.session['currentUser'] = currentUser

        messages.success(request, 'Item added to cart')
        return redirect("index")

    context = {
        "specials" : specials,
        "menuItems" : menuItems,
        "popular_dishes" : popular_dishes,
        "hero_dish" : hero_dish,
        "cartCount" : cartCount
    } 
    return render(request,'client/index.html',context)


def CustomerOrdersView(request):
    currentUser = request.session.get('currentUser')

    if currentUser == "":
        sessionUser = "No"
    else:
        sessionUser = "Yes"

    orders = CartModel.objects.filter(currentUser=currentUser).exclude(status="Cart").order_by("-date_created")
    hero_dish = MenuItemsModel.objects.get(sale_status = "Hero")

    if request.method == 'POST' and 'reload_user' in request.POST:
        userID = request.POST.get('userID')
        request.session['currentUser'] = userID
        return redirect("customer-orders")
    
    if currentUser != "":
        cartOrders = CartModel.objects.filter(Q(currentUser = currentUser) & Q(status = "Cart"))
        cartCount = 0
        for i in cartOrders:
            cartItems = i.items.all().count()
            cartCount = cartCount + cartItems
    else:
        cartCount = 0


    context = {
        "orders" : orders,
        "hero_dish" : hero_dish,
        "sessionUser" : sessionUser,
        "cartCount" : cartCount
    }

    return render(request,'customer/customer_order.html',context)

def SpecialsPageView(request):
    specials = MenuItemsModel.objects.filter(sale_status = "Sale")
    popular_dishes = MenuItemsModel.objects.filter(popular_status = "Popular")

    currentUser = request.session.get('currentUser')
    if currentUser != "":
        cartOrders = CartModel.objects.filter(Q(currentUser = currentUser) & Q(status = "Cart"))
        cartCount = 0
        for i in cartOrders:
            cartItems = i.items.all().count()
            cartCount = cartCount + cartItems
    else:
        cartCount = 0

    context = {
        "specials" : specials,
        "popular_dishes" : popular_dishes,
        "cartCount" : cartCount
    }
    return render(request,'client/specialsPage.html',context)
