from django.shortcuts import render
from .models import Product, Category


def home(request):
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    )

    categories = Category.objects.all()

    context = {
        "featured_products": featured_products,
        "categories": categories,
    }

    return render(request, "home.html", context)