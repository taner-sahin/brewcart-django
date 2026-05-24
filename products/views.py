from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Review
from django.contrib import messages
from django.db.models import Avg


def home(request):
    # URL'den arama kelimesini alır.
    query = request.GET.get("q")

    # URL'den sıralama bilgisini alır.
    sort = request.GET.get("sort")

    # URL'den stok filtresini alır.
    in_stock = request.GET.get("in_stock")

    # URL'den minimum ve maksimum fiyatı alır.
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    # Aktif ve öne çıkarılmış ürünleri getirir.
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    )

    # Ürün adına göre arama yapar.
    if query:
        featured_products = featured_products.filter(name__icontains=query)

    # Stoğu 0'dan büyük ürünleri getirir.
    if in_stock:
        featured_products = featured_products.filter(stock__gt=0)

    # Minimum fiyat filtresi.
    if min_price:
        featured_products = featured_products.filter(price__gte=min_price)

    # Maksimum fiyat filtresi.
    if max_price:
        featured_products = featured_products.filter(price__lte=max_price)

    # Fiyata göre sıralama.
    if sort == "price_low":
        featured_products = featured_products.order_by("price")

    elif sort == "price_high":
        featured_products = featured_products.order_by("-price")

    # Ana sayfa kategori kartları.
    categories = Category.objects.all()

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
    # Slug'a göre kategoriyi bulur.
    category = get_object_or_404(Category, slug=slug)

    # Kategoriye ait aktif ürünleri getirir.
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
    # Slug'a göre aktif ürünü bulur.
    product = get_object_or_404(
        Product,
        slug=slug,
        is_available=True
    )

    # Bu ürüne ait yorumları getirir.
    reviews = product.reviews.all()
    
    average_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    review_count = reviews.count()

    # Yorum formu gönderildiyse çalışır.
    if request.method == "POST":

        # Sadece giriş yapan kullanıcı yorum yapabilir.
        if request.user.is_authenticated:
            rating = request.POST.get("rating")
            comment = request.POST.get("comment")

            # Kullanıcı bu ürüne daha önce yorum yapmış mı?
            existing_review = Review.objects.filter(
                product=product,
                user=request.user
            ).exists()

            # Daha önce yorum yaptıysa ikinci yorumu oluşturma.
            if existing_review:
                messages.warning(request, "Bu ürüne zaten yorum yaptın.")
                return redirect("products:product_detail", slug=product.slug)

            # Yeni yorum oluştur.
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment,
            )

            # Yorumu kaydettikten sonra aynı ürün sayfasına dön.
            return redirect("products:product_detail", slug=product.slug)

        # Giriş yapmamış kullanıcı login sayfasına gider.
        return redirect("accounts:login")

    context = {
        "product": product,
        "reviews": reviews,
        "average_rating": average_rating,
        "review_count": review_count,
    }

    return render(request, "products/detail.html", context)

def delete_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    product_slug = review.product.slug

    review.delete()

    return redirect("products:product_detail", slug=product_slug)

def edit_review(request, review_id):
    # Sadece kendi yorumunu bulabilir.
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    product_slug = review.product.slug

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        review.rating = rating
        review.comment = comment
        review.save()

        return redirect("products:product_detail", slug=product_slug)

    context = {
        "review": review,
    }

    return render(request, "products/edit_review.html", context)