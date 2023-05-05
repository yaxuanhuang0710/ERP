from django.urls import path

from . import views

app_name = "ship"

urlpatterns = [
    path("delivery_create/", views.delivery_create, name="delivery_create"),
    path("delivery_inquery/", views.delivery_inquery, name="delivery_inquery"),
    path("delivery_modify/<int:DelNum>", views.delivery_modify, name="delivery_modify"),
    path("delivery_detail/<int:DelNum>", views.delivery_detail, name="delivery_detail"),
    path("post/", views.post, name="post"),
    path("check_stock/", views.check_stock, name="check_stock"),
    path("check_stock_detail/<int:MatNum>", views.check_stock_detail, name="delivery_detail"),
]
