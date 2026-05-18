from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import CartItem


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart:cart_detail")

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total_price = 0

    for item in cart_items:
        total_price += item.subtotal()

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }

    return render(request, "cart/detail.html", context)