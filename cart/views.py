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

    # STOCK GUARD
    # stok 0 ise sepete ekleme

    if product.stock <= 0:
        return redirect(
            "products:product_detail",
            slug=product.slug
        )

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    # ürün zaten sepette varsa
    # quantity artır

    if not created:

        # STOCK LIMIT CONTROL
        # stoktan fazla artırma

        if cart_item.quantity < product.stock:

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

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    # Eğer ürün artık satışta değilse veya stok 0 ise artırma
    if not cart_item.product.is_available or cart_item.product.stock <= 0:
        return redirect("cart:cart_detail")

    # Stoktan fazla artırma
    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart:cart_detail")

def decrease_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()

    return redirect("cart:cart_detail")


def remove_item(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    cart_item.delete()

    return redirect("cart:cart_detail")