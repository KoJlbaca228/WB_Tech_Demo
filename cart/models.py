from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartProduct(models.Model):
    cart = models.ForeignKey(
        "cart.Cart", verbose_name="Cart", on_delete=models.CASCADE, related_name="items",)
    product = models.ForeignKey(
        "products.Product", verbose_name="Product", on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(
        verbose_name="Quantity", validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="cart_product_quantity_positive",
            ),
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_cart_product'
            )
        ]
