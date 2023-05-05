from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("create/", views.create, name="create"),
    path("inquery/", views.inquery, name="inquery"),
    path("modify/<int:OrdNum>", views.modify, name="modify"),
    path("detail/<int:OrdNum>", views.detail, name="detail"),
]
