from django.urls import path
from .import views

urlpatterns = [
    path('basket-items',views.CartItemsView,name='basket-items'),
    path('payment/<int:id>',views.PaymentMethod,name='payment'),
    path('successful/<int:id>',views.SuccessPageView,name='successful'),
    path('order-status/<int:id>',views.OrderStatusView,name='order-status'),
]