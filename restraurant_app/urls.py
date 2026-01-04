from django.urls import path
from .views import (
    HomeView,
    meals_view,
    meal_view,
    cart_view,
    add_to_cart,
    order_success,    
    web_insurance_view,
    profile_view,

    CustomLoginView,
    CustomSignupView,
    CustomLogoutView,

    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    # ----------------- MAIN -----------------
    path("", HomeView.as_view(), name="home"),
    path("about_us/", web_insurance_view, name="about_us"),

    # ----------------- MEALS -----------------
    path("meals/", meals_view, name="meals"),
    path("meals/<int:id>/", meal_view, name="meal"),

    # ----------------- CART & ORDER -----------------
    path("cart/", cart_view, name="cart"),
    path("cart/add/<int:id>/", add_to_cart, name="add-to-cart"),
    path("order-success/", order_success, name="order_success"),
    path("profile/", profile_view, name="profile"),

    # ----------------- AUTH (ALLAUTH) -----------------
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", CustomSignupView.as_view(), name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    # ----------------- PASSWORD RESET -----------------
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset/confirm/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
