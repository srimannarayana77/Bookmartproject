from django.urls import path
from app.controllers.bookController import BookView

urlpatterns = [
path('',BookView.create_book),
path('all', BookView.list_books),
path('<int:id>', BookView.retrieve_book),
path('<int:id>/update',BookView.update_book),
path('<int:id>/delete', BookView.delete_book),
# path('fake', BookView.book_bulk_create)
]