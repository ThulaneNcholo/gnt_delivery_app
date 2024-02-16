from django.urls import path
from .import views

urlpatterns = [
    path('dish-details/<int:id>',views.DishDetailsView,name='dish-details'),
    path('menu-items',views.ListMenuView,name='menu-items'),
    path('add-new-item',views.AddNewItemView,name='add-new-item'),
    path('create-sale/<int:id>',views.CreateSaleItemView,name='create-sale'),
    path('create-hero/<int:id>',views.CreateHeroDishView,name='create-hero'),


    # htmx views 
    path('add-ingredient',views.IngredientPartialView,name='add-ingredient'),

]