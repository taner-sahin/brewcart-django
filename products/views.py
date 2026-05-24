from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):

    # URL'den gelen arama kelimesini alıyoruz.
    #
    # Örnek:
    # /?q=espresso
    #
    query = request.GET.get("q")

    # URL'den gelen sıralama bilgisini alıyoruz.
    #
    # Örnek:
    # /?sort=price_low
    #
    sort = request.GET.get("sort")

    # URL'den gelen stok filtresini alıyoruz.
    #
    # Örnek:
    # /?in_stock=1
    #
    in_stock = request.GET.get("in_stock")

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

    # Eğer kullanıcı sadece stokta olan ürünleri görmek isterse:
    #
    # stock > 0 olan ürünleri getir.
    #
    if in_stock:
        featured_products = featured_products.filter(stock__gt=0)

    # Sıralama sistemi
    #
    # price_low:
    # ucuzdan pahalıya
    #
    # price_high:
    # pahalıdan ucuza
    #
    if sort == "price_low":
        featured_products = featured_products.order_by("price")

    elif sort == "price_high":
        featured_products = featured_products.order_by("-price")

    # Bütün kategorileri getiriyoruz.
    categories = Category.objects.all()

    # Python verilerini HTML'e gönderiyoruz.
    context = {
        "featured_products": featured_products,
        "categories": categories,
        "query": query,
        "sort": sort,
        "in_stock": in_stock,
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