from decimal import Decimal
import random

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.db import transaction

# from allauth.account.views import LoginView,LogoutView,SignupView
from allauth.socialaccount.models import SocialAccount

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    LoginView, LogoutView
)

from django.urls import reverse_lazy

from .models import MealType, Meal, Deliveries, Order, OrderItem


# ----------------- HOME -----------------
class HomeView(View):
    def get(self, request):
        all_types = MealType.objects.all()
        all_deliveries = Deliveries.objects.all()
        checked_employees = [d for d in all_deliveries if d.working_age >= 3]

        return render(request, 'home.html', {
            'all_types': all_types,
            'staged_employees': checked_employees
        })


# ----------------- ABOUT US -----------------
def web_insurance_view(request):
    return render(request, 'about_us.html')


# ----------------- PROFILE -----------------
@login_required
def profile_view(request):
    user = request.user
    google_account = SocialAccount.objects.filter(user=user, provider='google').first()

    return render(request, 'profile.html', {
        'user': user,
        'google_account': google_account,
    })


# ----------------- MEALS -----------------
def meals_view(request):
    meals = Meal.objects.all()
    return render(request, 'meals.html', {'meals': meals})


def meal_view(request, id):
    selected_meal = get_object_or_404(Meal, id=id)
    return render(request, 'meal.html', {'meal': selected_meal})


# ----------------- CART -----------------
@require_POST
def add_to_cart(request, id):
    meal = get_object_or_404(Meal, id=id)
    cart = request.session.get('cart', {})
    meal_id_str = str(meal.id)

    price = float(meal.price)

    if meal_id_str in cart:
        cart[meal_id_str]['qty'] += 1
    else:
        cart[meal_id_str] = {
            'name': meal.name,
            'price': price,
            'qty': 1,
            'image': meal.image.url if meal.image and hasattr(meal.image, 'url') else ''
        }

    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', '/meals/'))


@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    total = sum(Decimal(item['price']) * item['qty'] for item in cart.values())
    deliveries = Deliveries.objects.filter(is_free=True)

    if request.method == 'POST':
        delivery_id = request.POST.get('delivery')
        if delivery_id:
            delivery = get_object_or_404(Deliveries, id=int(delivery_id), is_free=True)
            request.session['chosen_delivery'] = {
                'id': delivery.id,
                'name': f"{delivery.first_name} {delivery.last_name}"
            }
            return redirect('cart')

    return render(request, 'cart.html', {
        'cart': cart,
        'total': total,
        'deliveries': deliveries
    })


# ----------------- CHECKOUT / ORDER -----------------
def get_random_free_delivery():
    free_deliveries = Deliveries.objects.filter(is_free=True)
    if not free_deliveries.exists():
        return None
    return random.choice(list(free_deliveries))


@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('cart')
    
    with transaction.atomic():
        delivery = get_random_free_delivery()
        
        total_price = sum(
            Decimal(item['price']) * item['qty']
            for item in cart.values()
        )

        order = Order.objects.create(
            user=request.user,
            delivery=delivery,
            total_price=total_price
        )

        for meal_id, item in cart.items():
            OrderItem.objects.create(
                order=order,
                meal_id=int(meal_id),
                quantity=item['qty'],
                price=Decimal(item['price'])
            )

        if delivery:
            delivery.is_free = False
            delivery.save()

        request.session['cart'] = {}
        request.session.modified = True

    return redirect('order_success', order_id=order.id)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {
        'order': order
    })


# ----------------- AUTH -----------------
class CustomLoginView(LoginView):
    template_name = "account/login.html"
    success_url = reverse_lazy("home")

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('account_login'))
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required
def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
    return render(request, 'account/logout.html')
# ----------------- PASSWORD RESET -----------------
class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'
