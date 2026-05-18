from django.shortcuts import render, get_object_or_404
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

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(
        category=category,
        is_available=True
    )

    context = {
        "category": category,
        "products": products,
    }

    return render(request, "products/category.html", context)

def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_available=True
    )

    context = {
        "product": product
    }

    return render(request, "products/detail.html", context)