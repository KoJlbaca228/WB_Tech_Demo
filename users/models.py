from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class MyUser(AbstractUser):
    balance = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte=0),
                name="user_balance_non_negative",
            ),
        ]


class BalanceTransaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="balance_transactions",
    )
    amount = models.DecimalField(
        max_digits=13,
        decimal_places=2,
    )

    class Type(models.TextChoices):
        CREDITING = 'crediting', 'Зачисление'
        DEBITING = 'debiting', 'Списание'
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
    )
    order = models.ForeignKey(
        "orders.Order",
        verbose_name="Order",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="balance_transactions",
    )
    balance_after = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(type="crediting", amount__gt=0)
                    | models.Q(type="debiting", amount__lt=0)
                ),
                name="transaction_type_matches_amount_sign",
            ),
            models.CheckConstraint(
                condition=models.Q(balance_after__gte=0),
                name="transaction_balance_after_non_negative",
            ),
        ]
