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
from django.contrib.auth import views as auth_views

from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),

    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:c_id>/', views.delete_category, name='delete_category'),
    path('update-category/<int:c_id>/', views.update_category, name='update_category'),

    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:p_id>/', views.delete_product, name='delete_product'),
    path('update-product/<int:p_id>/', views.update_product, name='update_product'),

    path('add-section/', views.add_section, name='add_section'),
    path('delete-section/<int:sec_id>/', views.delete_section, name='delete_section'),
    path('update-section/<int:sec_id>/', views.update_section, name='update_section'),
    path('section-detail/<int:sec_id>/', views.section_details, name='section_details'),

    path('add-staff/', views.add_staff, name='add_staff'),
    path('delete-staff/<int:s_id>/', views.delete_staff, name='delete_staff'),
    path('update-staff/<int:s_id>/', views.update_staff, name='update_staff'),
    path('staff-detail/<int:s_id>/', views.staff_details, name='staff_details'),

    path('receive-item/',views.receive_items, name='receive_items'),
    path('issue-item/',views.issue_items, name='issue_items'),
    path('all-items/', views.list_all_items, name='list_all_items'),
    path('all-transactions/', views.all_transaction, name='all_transaction'),
    path('list-issued/', views.list_issued_transaction, name='list_issued_transaction'),
    path('list-received/', views.list_received_transaction, name='list_received_transaction'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
