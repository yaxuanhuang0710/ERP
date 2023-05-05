from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
    path("create/", views.create, name="create"),
    path("inquery/", views.inquery, name="inquery"),
    path("modify/<int:CustNum>", views.modify, name="modify"),
    path("detail/<int:CustNum>", views.detail, name="detail"),
]
