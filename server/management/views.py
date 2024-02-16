from django.shortcuts import render,redirect

from django.contrib import messages
from cart.models import *

# Create your views here.
def DashboardView(request):
    pending_orders = CartModel.objects.filter(status = "Pending").order_by("-date_created")
    pendingCount = pending_orders.count()
    deliveries_orders = CartModel.objects.filter(status = "Delivery").order_by("-date_created")
    deliveriesCount = deliveries_orders.count()
    complete_orders = CartModel.objects.filter(status = "Complete").order_by("-date_created")
    completeCount = complete_orders.count()

    context = {
        "pending_orders" : pending_orders,
        "pendingCount" : pendingCount,
        "deliveries_orders" : deliveries_orders,
        "deliveriesCount" : deliveriesCount,
        "complete_orders" : complete_orders,
        "completeCount" : completeCount
    }

    return render(request,'management/dashboard.html',context)

def ViewOrder(request,id):
    order = CartModel.objects.get(id = id)
    order_items = order.items.all()

    if request.method == 'POST' and 'submit_delivery' in request.POST:
        order.status = "Delivery"
        order.save()
        messages.success(request, 'order out for delivery')
        return redirect("order", id)
    
    if request.method == 'POST' and 'submit_complete' in request.POST:
        order.status = "Complete"
        order.save()
        messages.success(request, 'Order Delivered')
        return redirect("order", id)

    context = {
        "order" : order,
        "order_items" : order_items
    }
    return render(request,'orders/view_order.html',context)

def ManagementOrdersView(request):
    orders = CartModel.objects.all().exclude(status="Cart").order_by("-date_created")

    context = {
        "orders" : orders
    }
    
    return render(request,'management/list_orders.html',context)