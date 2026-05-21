from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem


@login_required
def checkout(request):
    # Giriş yapan kullanıcının sepetteki ürünlerini alıyoruz.
    cart_items = CartItem.objects.filter(user=request.user)

    # Sepet boşsa checkout sayfasına izin vermiyoruz.
    # Kullanıcıyı tekrar sepet sayfasına gönderiyoruz.
    if not cart_items.exists():
        return redirect("cart:cart_detail")

    # Sepetteki her ürünün subtotal değerlerini toplayıp genel toplamı buluyoruz.
    total_price = sum(item.subtotal() for item in cart_items)

    # Kullanıcı checkout formunu gönderirse POST çalışır.
    if request.method == "POST":

        # Son stok kontrolü.
        # Sepetteki adet, ürün stoğundan fazlaysa sipariş oluşturma.
        # Bu backend güvenlik katmanıdır.
        for item in cart_items:
            if item.quantity > item.product.stock:
                return redirect("cart:cart_detail")

        # Formdan gelen müşteri bilgilerini alıyoruz.
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Ana sipariş kaydını oluşturuyoruz.
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=total_price,
        )

        # Sepetteki her ürünü sipariş satırına çeviriyoruz.
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity,
                subtotal=item.subtotal(),
            )

            # Siparişten sonra ürün stoğunu düşürüyoruz.
            item.product.stock -= item.quantity
            item.product.save()

        # Sipariş tamamlanınca sepeti temizliyoruz.
        cart_items.delete()

        # Kullanıcıyı başarı sayfasına gönderiyoruz.
        return redirect("orders:success")

    # Sayfa ilk açıldığında checkout.html'e sepet ve toplam bilgisi gönderiyoruz.
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }

    return render(request, "orders/checkout.html", context)


@login_required
def success(request):
    # Sipariş başarılı olunca gösterilecek sayfa.
    return render(request, "orders/success.html")

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    context = {
        "orders": orders,
    }

    return render(request, "orders/my_orders.html", context)

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    context = {
        "order": order,
    }

    return render(request, "orders/order_detail.html", context)