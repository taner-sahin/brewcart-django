from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):

    # URL'den gelen arama kelimesini alıyoruz.
    #
    # Örnek:
    #
    # /?q=espresso
    #
    # Buradaki:
    #
    # q = espresso
    #
    query = request.GET.get("q")

    # İlk başta:
    #
    # aktif VE featured ürünleri getiriyoruz.
    #
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    )

    # Eğer kullanıcı arama yaptıysa:
    #
    # ürün adında geçen kelimeyi filtrele.
    #
    if query:
        featured_products = featured_products.filter(
            name__icontains=query
        )

    # Bütün kategorileri getiriyoruz.
    categories = Category.objects.all()

    # Python verilerini HTML'e gönderiyoruz.
    context = {
        "featured_products": featured_products,
        "categories": categories,
        "query": query,
    }

    # home.html sayfasını render ediyoruz.
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