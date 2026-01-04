from decimal import Decimal
import random

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST
from django.db import transaction
from django.urls import reverse_lazy

from allauth.account.views import LoginView, SignupView, LogoutView

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from .models import MealType, Meal, Deliveries, Order, OrderItem


# ----------------- HOME -----------------
class HomeView(View):
    def get(self, request):
        all_types = MealType.objects.all()
        all_deliveries = Deliveries.objects.all()
        all_meals = Meal.objects.all()
        checked_employees = [d for d in all_deliveries if d.working_age >= 3]

        return render(request, "home.html", {
            "all_meals": all_meals,
            "all_types": all_types,
            "staged_employees": checked_employees,
        })


# ----------------- ABOUT US -----------------
def web_insurance_view(request):
    return render(request, "about_us.html")


# ----------------- MEALS -----------------
def meals_view(request):
    meals = Meal.objects.all()
    return render(request, "meals.html", {"meals": meals})


def meal_view(request, id):
    meal = get_object_or_404(Meal, id=id)
    return render(request, "meal.html", {"meal": meal})


# ----------------- CART -----------------
@require_POST
def add_to_cart(request, id):
    meal = get_object_or_404(Meal, id=id)
    cart = request.session.get("cart", {})
    meal_id = str(meal.id)

    if meal_id in cart:
        cart[meal_id]["qty"] += 1
    else:
        cart[meal_id] = {
            "name": meal.name,
            "price": float(meal.price),
            "qty": 1,
            "image": meal.image.url if meal.image else "",
        }

    request.session["cart"] = cart
    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER", "/meals/"))


@login_required
def cart_view(request):
    cart = request.session.get("cart", {})
    total = sum(Decimal(item["price"]) * item["qty"] for item in cart.values())
    deliveries = Deliveries.objects.filter(is_free=True)

    if request.method == "POST":
        delivery_id = request.POST.get("delivery")
        if delivery_id:
            delivery = get_object_or_404(Deliveries, id=delivery_id, is_free=True)
            request.session["chosen_delivery"] = {
                "id": delivery.id,
                "name": f"{delivery.first_name} {delivery.last_name}",
            }
            return redirect("cart")

    return render(request, "cart.html", {
        "cart": cart,
        "total": total,
        "deliveries": deliveries,
    })


# ----------------- CHECKOUT / ORDER -----------------
def get_random_free_delivery():
    deliveries = Deliveries.objects.filter(is_free=True)
    return random.choice(list(deliveries)) if deliveries.exists() else None

@login_required
def order_success(request):
    cart = request.session.get('cart', {})
    delivery = 5.00
    total = 0.00
    
    # Calculate total
    for item in cart.values():
        item_price = float(item["price"])
        item_qty = item["qty"]
        item["total"] = item_price * item_qty
        total += item["total"]
    
    # Add delivery fee
    total += delivery
    
    context = {
        'cart': cart,
        'delivery': delivery,
        'total': total,
    }
    
    return render(request, 'order_success.html', context)
# ----------------- AUTH (ALLAUTH) -----------------
class CustomLoginView(LoginView):
    template_name = "account/login.html"

class CustomSignupView(SignupView):
    template_name = "account/register.html"

class CustomLogoutView(LogoutView):
    template_name = "account/logout.html"
    next_page = reverse_lazy("home")

def profile_view(request):
    return render(request, "profile.html")
# ----------------- AUTH (ALLAUTH) -----------------
class CustomPasswordResetView(PasswordResetView):
    template_name = "account/password_reset.html"
    next_page = reverse_lazy("password_reset_done")

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    next_page = reverse_lazy("password_reset_complete")

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"