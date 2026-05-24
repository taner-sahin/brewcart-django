from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    # URL'den arama kelimesini alır.
    # Örnek: /?q=espresso
    query = request.GET.get("q")

    # URL'den sıralama bilgisini alır.
    # Örnek: /?sort=price_low
    sort = request.GET.get("sort")

    # URL'den stok filtresini alır.
    # Örnek: /?in_stock=1
    in_stock = request.GET.get("in_stock")

    # URL'den minimum fiyatı alır.
    # Örnek: /?min_price=300
    min_price = request.GET.get("min_price")

    # URL'den maksimum fiyatı alır.
    # Örnek: /?max_price=500
    max_price = request.GET.get("max_price")

    # İlk olarak aktif ve öne çıkarılmış ürünleri getirir.
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    )

    # Arama varsa ürün adına göre filtreler.
    if query:
        featured_products = featured_products.filter(
            name__icontains=query
        )

    # Stok filtresi varsa stoğu 0'dan büyük ürünleri getirir.
    if in_stock:
        featured_products = featured_products.filter(
            stock__gt=0
        )

    # Minimum fiyat girildiyse bu fiyattan büyük/eşit ürünleri getirir.
    if min_price:
        featured_products = featured_products.filter(
            price__gte=min_price
        )

    # Maksimum fiyat girildiyse bu fiyattan küçük/eşit ürünleri getirir.
    if max_price:
        featured_products = featured_products.filter(
            price__lte=max_price
        )

    # Ürünleri fiyata göre sıralar.
    if sort == "price_low":
        featured_products = featured_products.order_by("price")

    elif sort == "price_high":
        featured_products = featured_products.order_by("-price")

    # Ana sayfadaki kategori kartları için kategorileri getirir.
    categories = Category.objects.all()

    # Python verilerini HTML sayfasına gönderir.
    context = {
        "featured_products": featured_products,
        "categories": categories,
        "query": query,
        "sort": sort,
        "in_stock": in_stock,
        "min_price": min_price,
        "max_price": max_price,
    }

    return render(request, "home.html", context)


def category_products(request, slug):
    # Slug'a göre kategoriyi bulur, yoksa 404 verir.
    category = get_object_or_404(Category, slug=slug)

    # Seçilen kategoriye ait aktif ürünleri getirir.
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
    # Slug'a göre aktif ürünü bulur, yoksa 404 verir.
    product = get_object_or_404(
        Product,
        slug=slug,
        is_available=True
    )

    context = {
        "product": product,
    }

    return render(request, "products/detail.html", context)