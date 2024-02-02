from django.urls import path
from app.controllers.companyController import CompanyView

urlpatterns = [
path('',CompanyView.create_company),
path('all',CompanyView.list_companies),
path('<int:id>', CompanyView.retrieve_company),
path('<int:id>/update',CompanyView.update_company),
path('<int:id>/delete', CompanyView.delete_company),
]