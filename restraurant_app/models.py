from django.db import models
from django.conf import settings

class Deliveries(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    working_age = models.IntegerField()
    is_free = models.BooleanField(default=True)
    image = models.ImageField(upload_to='selfies/', blank=True, null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MealType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='meal_types/', blank=True, null=True)

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=150)
    type = models.ForeignKey(MealType, on_delete=models.CASCADE, related_name='meals')
    ingredients = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='meals/')
    description = models.TextField(blank=True)
    halal = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# 🔥 ORDER SYSTEM
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    delivery = models.ForeignKey(
        Deliveries,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity
