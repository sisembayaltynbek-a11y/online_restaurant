# import random
# from django.shortcuts import get_object_or_404, redirect, render
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
# from django.views import View
# from django.db import transaction
# from decimal import Decimal

# from allauth.account.views import LoginView as AllauthLoginView
# from allauth.account.views import SignupView as AllauthSignupView
# from allauth.account.views import LogoutView as AllauthLogoutView

# from .models import MealType, Meal, Deliveries, Order, OrderItem



# # ----------------- HOME -----------------
# class HomeView(View):
#     def get(self, request):
#         return render(request, 'home.html', {
#             'all_types': MealType.objects.all(),
#             'staged_employees': Deliveries.objects.filter(working_age__gte=3)
#         })


# def web_insurance_view(request):
#     return render(request, 'about_us.html')


# # ----------------- PROFILE -----------------
# @login_required
# def profile_view(request):
#     google_account = request.user.socialaccount_set.filter(provider='google').first()

#     return render(request, 'profile.html', {
#         'user': request.user,
#         'google_account': google_account
#     })


# # ----------------- MEALS -----------------
# def meals_view(request):
#     return render(request, 'meals.html', {
#         'meals': Meal.objects.all()
#     })


# def meal_view(request, id):
#     return render(request, 'meal.html', {
#         'meal': get_object_or_404(Meal, id=id)
#     })


# # ----------------- CART -----------------
# @require_POST
# def add_to_cart(request, id):
#     meal = get_object_or_404(Meal, id=id)
#     cart = request.session.get('cart', {})
#     meal_id = str(meal.id)

#     if meal_id in cart:
#         cart[meal_id]['qty'] += 1
#     else:
#         cart[meal_id] = {
#             'name': meal.name,
#             'price': float(meal.price),
#             'qty': 1,
#             'image': meal.image.url if meal.image else ''
#         }

#     request.session['cart'] = cart
#     request.session.modified = True
#     return redirect(request.META.get('HTTP_REFERER', '/meals/'))

# def cart_view(request):
#     cart = request.session.get('cart', {})
#     total = sum(item['price'] * item['qty'] for item in cart.values())

#     free_deliveries = Deliveries.objects.filter(is_free=True)
#     preview_delivery = random.choice(free_deliveries) if free_deliveries.exists() else None

#     return render(request, 'cart.html', {
#         'cart': cart,
#         'total': total,
#         'delivery': preview_delivery,
#     })
# # ----------------- CHECKOUT / ORDER -----------------
# def get_random_free_delivery():
#     free_deliveries = Deliveries.objects.filter(is_free=True)

#     if not free_deliveries.exists():
#         return None

#     return random.choice(list(free_deliveries))

# @login_required
# def checkout_view(request):
#     cart = request.session.get('cart', {})

#     if not cart:
#         return redirect('cart')

#     with transaction.atomic():
#         delivery = get_random_free_delivery()
    
#         total_price = sum(
#             Decimal(item['price']) * item['qty']
#             for item in cart.values()
#         )

#         order = Order.objects.create(
#             user=request.user,
#             delivery=delivery,
#             total_price=total_price
#         )

#         for meal_id, item in cart.items():
#             OrderItem.objects.create(
#                 order=order,
#                 meal_id=int(meal_id),
#                 quantity=item['qty'],
#                 price=Decimal(item['price'])
#             )

#         if delivery:
#             delivery.is_free = False
#             delivery.save()

#         request.session['cart'] = {}
#         request.session.modified = True

#     return redirect('order_success', order_id=order.id)


# @login_required
# def order_success(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)

#     return render(request, 'order_success.html', {
#         'order': order
#     })


# # ----------------- AUTH -----------------
# class LoginView(AllauthLoginView):
#     template_name = 'account/login.html'
#     success_url = '/'


# class SignupView(AllauthSignupView):
#     template_name = 'account/signup.html'
#     success_url = '/'


# class LogoutView(AllauthLogoutView):
#     template_name = 'account/logout.html'
#     success_url = '/'



from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView as AllauthLoginView
from allauth.account.views import SignupView as AllauthSignupView
from allauth.account.views import LogoutView as AllauthLogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views import View
from django.views.decorators.http import require_POST
from .models import MealType, Meal, Deliveries

# -----------------main section---------------------
class HomeView(View):
    def get(self, request):
        all_types = MealType.objects.all()
        all_deliveries = Deliveries.objects.all()
        checked_employees = [d for d in all_deliveries if d.working_age >= 3]

        return render(request, 'home.html', {
            'all_types': all_types,
            'staged_employees': checked_employees
        })

    def post(self, request):
        all_types = MealType.objects.all()
        all_deliveries = Deliveries.objects.all()
        checked_employees = [d for d in all_deliveries if d.working_age >= 3]

        return render(request, 'home.html', {
            'all_types': all_types,
            'staged_employees': checked_employees
        })

# -----------------web insurance/about_us-----------------
def web_insurance_view(request):
    return render(request, 'about_us.html')

# -----------------personal section-----------------
@login_required
def profile_view(request):
    user = request.user
    google_account = None
    if user.socialaccount_set.exists():
        google_account = user.socialaccount_set.filter(provider='google').first()

    return render(request, 'profile.html', {
        'user': user,
        'google_account': google_account,
    })

# -----------------meal section-----------------
def meals_view(request):
    meals = Meal.objects.all()
    return render(request, 'meals.html', {'meals': meals})

def meal_view(request, id):
    selected_meal = get_object_or_404(Meal, id=id)
    return render(request, 'meal.html', {'meal': selected_meal})

# -----------------cart section-----------------
@require_POST
def add_to_cart(request, id):
    meal = get_object_or_404(Meal, id=id)
    cart = request.session.get('cart', {})
    meal_id_str = str(meal.id)  # use string for JSON serialization

    price = float(meal.price)  # convert Decimal to float

    if meal_id_str in cart:
        cart[meal_id_str]['qty'] += 1
    else:
        cart[meal_id_str] = {
            'name': meal.name,
            'price': price,
            'qty': 1,
            'image': meal.image.url if meal.image else '',
        }

    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', '/meals/'))

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['qty'] for item in cart.values())
    deliveries = Deliveries.objects.filter(is_free=True)

    if request.method == 'POST':
        delivery_id = request.POST.get('delivery')
        if delivery_id:
            delivery = get_object_or_404(Deliveries, id=delivery_id, is_free=True)
            request.session['chosen_delivery'] = {
                'id': delivery.id,
                'name': f"{delivery.first_name} {delivery.last_name}"
            }
            return redirect('cart')  # can later redirect to checkout

    return render(request, 'cart.html', {
        'cart': cart,
        'total': total,
        'deliveries': deliveries
    })

# -----------------authorization section-----------------
class LoginView(AllauthLoginView):
    template_name = 'account/login.html'
    success_url = '/'

class SignupView(AllauthSignupView):
    template_name = 'account/signup.html'
    success_url = '/'

class LogoutView(AllauthLogoutView):
    template_name = 'account/logout.html'
    success_url = '/'

# -----------------authorization password section-----------------
class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html' 
    success_url = '/account/password-reset-done/'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = '/account/password-reset-complete/'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'