from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg, Q

from .models import Product, Category, Review


def home(request):
    query = request.GET.get("q")
    sort = request.GET.get("sort")
    in_stock = request.GET.get("in_stock")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    # Arama veya filtre varsa tüm aktif ürünlerde ara.
    # Hiç filtre yoksa sadece featured ürünleri ana sayfada göster.
    if query or sort or in_stock or min_price or max_price:
        featured_products = Product.objects.filter(is_available=True)
    else:
        featured_products = Product.objects.filter(
            is_available=True,
            is_featured=True
        )

    # Search: ürün adı + açıklama + kategori adı içinde arar.
    if query:
        featured_products = featured_products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    if in_stock:
        featured_products = featured_products.filter(stock__gt=0)

    if min_price:
        featured_products = featured_products.filter(price__gte=min_price)

    if max_price:
        featured_products = featured_products.filter(price__lte=max_price)

    if sort == "price_low":
        featured_products = featured_products.order_by("price")

    elif sort == "price_high":
        featured_products = featured_products.order_by("-price")

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

    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
    review_count = reviews.count()

    if request.method == "POST":

        if request.user.is_authenticated:
            rating = request.POST.get("rating")
            comment = request.POST.get("comment")

            existing_review = Review.objects.filter(
                product=product,
                user=request.user
            ).exists()

            if existing_review:
                messages.warning(request, "Bu ürüne zaten yorum yaptın.")
                return redirect("products:product_detail", slug=product.slug)

            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment,
            )

            return redirect("products:product_detail", slug=product.slug)

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