from django.urls import path
from app.controllers.cartController import CartView

urlpatterns = [
path('',CartView.create_cart),
path('all',CartView .list_carts),
path('<int:id>', CartView.retrieve_cart),
path('<int:id>/update',CartView.update_cart),
path('<int:id>/delete', CartView.delete_cart),
]