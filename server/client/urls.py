
from django.urls import path
from .import views

urlpatterns = [
    path('',views.IndexView,name='index'),
    path('customer-orders',views.CustomerOrdersView,name='customer-orders'),
    path('specials',views.SpecialsPageView,name='specials'),
]

