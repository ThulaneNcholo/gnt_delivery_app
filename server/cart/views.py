from django.shortcuts import render,redirect

from cart.models import *
from client.models import *
from django.db.models import Q

# Create your views here.
def CartItemsView(request):
    currentUser = request.session.get('currentUser')
    show_bottom_navbar = "False"  # Set this based on your condition

    if currentUser != "":
        cartOrders = CartModel.objects.filter(Q(currentUser = currentUser) & Q(status = "Cart"))
        cartCount = 0
        for i in cartOrders:
            cartItems = i.items.all().count()
            cartCount = cartCount + cartItems
    else:
        cartCount = 0

    if CartModel.objects.filter(Q(currentUser = currentUser) & Q(status = "Cart")).exists():
        userCart = CartModel.objects.get(Q(currentUser = currentUser) & Q(status = "Cart"))
        cartItems = userCart.items.all()

        context = {
            "userCart" : userCart,
            "cartItems" : cartItems,
            "cartCount" : cartCount,
            "show_bottom_navbar" : show_bottom_navbar
        }

    else:
        userCart = None

        context = {
            "userCart" : userCart,
            "cartCount" : cartCount,
            "show_bottom_navbar" : show_bottom_navbar
        }

    


    # ******* remove item from cart ***********
    if request.method == 'POST' and 'remove_item' in request.POST:
        item_id = request.POST.get('item_id')
        remove_item = CartItemsModel.objects.get(id = item_id)
        # update cart
        userCart.sub_total = userCart.sub_total - remove_item.sold_price
        userCart.total =  userCart.total - remove_item.sold_price
        userCart.save()
        # delete item 
        remove_item.delete()
        return redirect("basket-items")
    
    # ******* remove item ingredient ************
    if request.method == 'POST' and 'remove_ingredient' in request.POST:
        itemID = request.POST.get('itemID')
        itemIngredients = CartItemsModel.objects.get(id = itemID)
        ingredientProfile = itemIngredients.item_ingredients.all()
        for item in ingredientProfile:
            reset_status = ItemIngredientsModel.objects.get(id = item.id)
            reset_status.status = "on"
            reset_status.save()

        ingredients = request.POST.getlist('ingredients') 
        for i in ingredients:
            updateIngredient = ItemIngredientsModel.objects.get(id = i)
            updateIngredient.status = "off"
            updateIngredient.save()
        return redirect("basket-items")
    
    # ********* processed to payment  *************
    if request.method == 'POST' and 'check_out' in request.POST:
        userCart.notes = request.POST.get('notes')
        userCart.save()
        return redirect("payment",userCart.id)
    
        

    return render(request,'cart/cart_items.html',context)

def PaymentMethod(request,id):
    currentUser = request.session.get('currentUser')
    show_bottom_navbar = "False"  # Set this based on your condition

    if currentUser != "":
        cartOrders = CartModel.objects.filter(Q(currentUser = currentUser) & Q(status = "Cart"))
        cartCount = 0
        for i in cartOrders:
            cartItems = i.items.all().count()
            cartCount = cartCount + cartItems
    else:
        cartCount = 0

    userCart = CartModel.objects.get(id = id)

    if request.method == 'POST' and 'submit_payment' in request.POST:
        payment_method = request.POST.get('payment_method')

        # create user details 
        create_customer = CustomerModel()
        create_customer.customer = currentUser
        create_customer.firstName = request.POST.get('firstName')
        create_customer.contact = request.POST.get('contact')
        create_customer.street = request.POST.get('street')
        create_customer.suburb = request.POST.get('suburb')
        create_customer.city  = request.POST.get('city')
        create_customer.postal_code = request.POST.get('postal_code')
        create_customer.save()

        # update cart 
        userCart.customer = create_customer
        userCart.status = "Pending"
        if payment_method == "online":
            userCart.payment_status = "Paid"
            userCart.payment_method = "Online"
        else:
            userCart.payment_status = "Unpaid"
            userCart.payment_method = "Cash"

        userCart.save()
        return redirect("successful",id)

    context = {
        "userCart" : userCart,
        "cartCount" : cartCount,
        "show_bottom_navbar" : show_bottom_navbar
    }

    return render(request,'cart/payment.html',context)

def SuccessPageView(request,id):
    userCart = CartModel.objects.get(id = id)
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
        "userCart" : userCart,
        "cartCount" : cartCount
    }
    return render(request,'cart/successPage.html',context)

def OrderStatusView(request,id):
    currentUser = request.session.get('currentUser')
    userCart = CartModel.objects.get(id = id)
    cartItems = userCart.items.all()

    if currentUser != "":
        cartOrders = CartModel.objects.filter(Q(currentUser = currentUser) & Q(status = "Cart"))
        cartCount = 0
        for i in cartOrders:
            cartItems = i.items.all().count()
            cartCount = cartCount + cartItems
    else:
        cartCount = 0

    context = {
        "userCart" : userCart,
        "cartItems" : cartItems,
        "cartCount" : cartCount
    }

    return render(request,'cart/order_status.html',context)


    

    