from django.shortcuts import render,redirect
from .models import *

from cart.models import *

import random
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def DishDetailsView(request,id):
    item = MenuItemsModel.objects.get(id = id)
    
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

    # *************** check if theres session order ******************
    if session_order != None:
        order_number = request.session.get('session_order')
    else:
        ref_number = random.randrange(100, 10000)
        order_number = 'ORD' + str(ref_number)
        request.session['session_order'] = order_number


    # *************** cMake Post Method ******************
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
        return redirect("dish-details", id)



    context = {
        "data": item,
        "cartCount" : cartCount
    }

    return render(request,'dishes/dishDetails.html',context)

# Management views 
def ListMenuView(request):
    menuItems = MenuItemsModel.objects.all().order_by("-date_created")
    specials = MenuItemsModel.objects.filter(sale_status = "Sale").order_by("-date_created")
    popular_dishes = MenuItemsModel.objects.filter(popular_status = "Popular").order_by("-date_created")
    hero_dish = MenuItemsModel.objects.get(sale_status = "Hero")

    # Remove item from sale model
    if request.method == 'POST' and 'remove_special' in request.POST:
        itemID = request.POST.get('itemID')
        remove_sale = MenuItemsModel.objects.get(id = itemID)
        remove_sale.sale_status = ""
        remove_sale.sale_price = 0
        remove_sale.save()
        messages.success(request, 'item removed from sales')
        return redirect('menu-items')
    
    # create Popular Dish
    if request.method == 'POST' and 'submit_popular' in request.POST:
        itemID = request.POST.get('itemID')
        update_item = MenuItemsModel.objects.get(id = itemID)
        update_item.popular_status = "Popular"
        update_item.save()
        messages.success(request, 'Item added to popular dishes')
        return redirect('menu-items')
    
    # Remove item Popular Items
    if request.method == 'POST' and 'remove_popular' in request.POST:
        itemID = request.POST.get('itemID')
        remove_popular = MenuItemsModel.objects.get(id = itemID)
        remove_popular.popular_status = ""
        remove_popular.save()
        messages.success(request, 'item removed from popular items')
        return redirect('menu-items')

    context = {
        "menuItems" : menuItems,
        "specials" : specials,
        "popular_dishes" : popular_dishes,
        "hero_dish" : hero_dish
    }

    return render(request,'dishes/list_menu.html',context)

def AddNewItemView(request):
    # Clear the list associated with the page
    request.session['ingredients'] = []

    if request.method == 'POST' and 'submitItem' in request.POST:
        reference = random.randrange(0, 10000000)
        create_item = MenuItemsModel()
        create_item.reference = reference
        create_item.name = request.POST.get('itemName')
        create_item.description = request.POST.get('description')
        create_item.price = request.POST.get('price')
        create_item.cover_image = request.FILES.get('coverImage', None)
        create_item.save()

        # create ingredient model 
        checkedIngredients = request.POST.getlist('checkedIngredients')
        for i in checkedIngredients:
            add_ingredient = IngredientsModel()
            add_ingredient.reference = reference
            add_ingredient.name = i 
            add_ingredient.save()
            # update item model 
            create_item.item_ingredients.add(add_ingredient)
            create_item.save()


        messages.success(request, 'new menu item created')
        return redirect('menu-items')


    return render(request,'dishes/addNew_item.html')

def IngredientPartialView(request):
    if request.method == 'POST':
        # Retrieve or create a session list
        ingredients_list = request.session.get('ingredients', [])

        # Get the item from the POST request
        new_item = request.POST.get('new_item')

        # Add the new item to the session list
        ingredients_list.append(new_item)
        
        # Save the modified list back into the session
        request.session['ingredients'] = ingredients_list

        ingredients_list = request.session.get('ingredients', [])

        context = {
            "ingredients_list" : ingredients_list
        }

    return render(request,'partials/IngredientPartial.html',context)

def CreateSaleItemView(request,id):
    item = MenuItemsModel.objects.get(id = id)

    if request.method == 'POST' and 'submit_sale' in request.POST:
        item.sale_price = request.POST.get('price')
        item.sale_status = "Sale"
        item.save()
        messages.success(request, 'new sale created')
        return redirect('menu-items')

    context = {
        "item" : item
    }
    return render(request,'dishes/sale_item.html',context)


def CreateHeroDishView(request,id):
    item = MenuItemsModel.objects.get(id = id)

    if request.method == 'POST' and 'submit_sale' in request.POST:
        update_item = MenuItemsModel.objects.get(sale_status = "Hero")
        update_item.sale_status = ""
        update_item.sale_price = 0
        update_item.save()

        item.sale_price = request.POST.get('price')
        item.sale_status = "Hero"
        item.save()
        messages.success(request, 'new sale hero item created')
        return redirect('menu-items')

    context = {
        "item" : item
    }
    return render(request,'dishes/hero_dish.html',context)