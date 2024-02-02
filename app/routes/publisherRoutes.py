from django.urls import path
from app.controllers.publisherController import Publisherview

urlpatterns = [
path('',Publisherview.create_publisher),
path('all', Publisherview.list_publishers),
path('<int:id>', Publisherview.retrieve_publisher),
path('<int:id>/update',Publisherview.update_publisher),
path('<int:id>/delete', Publisherview.delete_publisher),
# path('fake', Publisherview.publisher_bulk_create)
path('signin', Publisherview.signinview)
]
