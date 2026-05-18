from django.db import models
from django.contrib.auth.models import User
from products.models import Product


# CartItem = Sepetteki tek ürün satırı
# English: Cart Item
# Türkçe: Sepet ürünü / sepet satırı
class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    # Hangi kullanıcıya ait sepet ürünü?

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    # Sepete hangi ürün eklendi?

    quantity = models.PositiveIntegerField(default=1)
    # Bu üründen kaç adet var?

    created_at = models.DateTimeField(auto_now_add=True)
    # Sepete ne zaman eklendi?

    def subtotal(self):
        return self.product.price * self.quantity
    # Bu ürün satırının ara toplamı:
    # ürün fiyatı x adet

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"