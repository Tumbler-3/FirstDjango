"""Djsite URL Configuration

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
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products.views import main, products_view, product_detail_view, all_categories_view, product_create_view
from users.views import login_view, registration_view, logout_view
from django.conf.urls.static import static
from Djsite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('products/', products_view),
    path('products/create/', product_create_view),
    path('products/<int:id>/', product_detail_view),
    path('categories/', all_categories_view),

    path('login/', login_view),
    path('registration/', registration_view),
    path('logout/', logout_view)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
