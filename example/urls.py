# example/urls.py
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('login/', views.login_user, name='login_user'),
    path('home/', views.home, name='home'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('razorpay/webhook/', views.razorpay_webhook, name='razorpay_webhook'),  # Add this line for webhook
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)