from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from decimal import Decimal


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="User",
        on_delete=models.PROTECT,
        related_name="orders"
    )

    class Status(models.TextChoices):
        CREATED = 'created', 'Создан'
        PAID = 'paid', 'Оплачен'
        CANCELLED = 'cancelled', 'Отменён'
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )
    total_amount = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total_amount__gte=Decimal("0.01")),
                name="order_total_amount_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    status__in=("created", "paid", "cancelled")
                ),
                name="order_status_valid",
            ),
        ]


class OrderProduct(models.Model):
    order = models.ForeignKey(
        "orders.Order", verbose_name="Order", on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(
        "products.Product",
        verbose_name="Product",
        null=True,
        on_delete=models.SET_NULL,
        related_name="order_products"
    )
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(
        max_digits=13, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    quantity = models.PositiveIntegerField(
        verbose_name="Quantity", validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(unit_price__gte=Decimal("0.01")),
                name="order_product_unit_price_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="order_product_quantity_positive",
            ),
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_order_product",
            ),
        ]
