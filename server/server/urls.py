from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('client.urls')),
    path('dishes',include('dishes.urls')),
    path('cart',include('cart.urls')),
    path('management',include('management.urls')),

]
