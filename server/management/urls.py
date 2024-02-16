from django.urls import path
from .import views

urlpatterns = [
    path('dashboard',views.DashboardView,name='dashboard'),
    path('order/<int:id>',views.ViewOrder,name='order'),
    path('list-orders',views.ManagementOrdersView,name='list-orders'),
]