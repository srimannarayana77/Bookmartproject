from django.urls import path
from app.controllers.orderController import OrderView

urlpatterns = [
path('',OrderView.create_order),
path('all',OrderView.list_orders),
path('<int:id>', OrderView.retrieve_order),
path('<int:id>/update',OrderView.update_order),
path('<int:id>/delete',OrderView.delete_order),
]