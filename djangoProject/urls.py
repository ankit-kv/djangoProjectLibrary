"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page, name='login_page'),
    path('home/', views.home_page, name='home_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:c_id>/', views.delete_category, name='delete_category'),
    path('update-category/<int:c_id>/', views.update_category, name='update_category'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:p_id>/', views.delete_product, name='delete_product'),
    path('update-product/<int:p_id>/', views.update_product, name='update_product'),
]
