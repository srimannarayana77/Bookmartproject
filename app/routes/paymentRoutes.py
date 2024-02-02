from django.urls import path
from app.controllers.paymentController import PaymentView

urlpatterns = [
path('',PaymentView.create_payment),
path('all', PaymentView.list_payments),
path('<int:id>', PaymentView.retrieve_payment),
path('<int:id>/delete', PaymentView.delete_payment),

]
