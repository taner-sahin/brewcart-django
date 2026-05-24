from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# =========================
# CATEGORY MODEL
# Amaç:
# Ürünleri kategorilere ayırmak.
# =========================
class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(
        max_length=120,
        unique=True
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# =========================
# PRODUCT MODEL
# Amaç:
# Kahve ürünlerini veritabanında saklamak.
# =========================
class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=150)

    slug = models.SlugField(
        max_length=170,
        unique=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    is_available = models.BooleanField(default=True)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


# =========================
# REVIEW MODEL
# Amaç:
# Kullanıcıların ürünlere yorum yapması.
# =========================
class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.PositiveIntegerField(
        choices=[
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        ]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.user} - {self.product}"