from django.urls import path
from . import views


app_name = "products"


urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>/", views.category_products, name="category_products"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path("review/<int:review_id>/edit/", views.edit_review, name="edit_review"),
]