from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('meals/', views.meals_view, name='meals'),
    path('meals/<int:id>', views.meal_view, name='meal'),
    path('profile/', views.profile_view, name='profile'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add-to-cart'),
    path('about_us/', views.web_insurance_view, name='about_us'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),

    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
