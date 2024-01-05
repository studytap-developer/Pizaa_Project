"""pizza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app import views
from django.conf import settings
# from django.conf.urls.static import staticurl
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path("add_cart/<pizza_uid>/", views.add_cart,name="add_cart"),
    path("cart/", views.cart,name="cart"),
    path("", views.index),
    path("login/", views.login_page,name="login_page"),
    path("logout/", views.logout_view,name="logout_view"),
    path("register/", views.register_page,name="register_page"),
    path("remove_cart_items/<cart_item_uid>/", views.remove_cart_items,name="remove_cart_items"),
     path("orders/", views.orders,name="orders"),
     path("success/", views.success,name="success"),
    path('invoice/<uuid:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('accounts/', include('allauth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns +=staticfiles_urlpatterns()