from django.urls import path
from app.controllers.customerController import Customerview

urlpatterns = [
path('',Customerview.create_customer),
path('all', Customerview.list_customers),
path('<int:id>',Customerview.retrieve_customer),
path('<int:id>/update',Customerview.update_customer),
path('<int:id>/delete', Customerview.delete_customer),
path('signin', Customerview.signinview),

]