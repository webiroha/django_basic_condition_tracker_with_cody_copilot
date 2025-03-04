"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.supplement_record, name='supplement_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('edit/<int:record_id>/', views.edit_record, name='edit_record'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='supplement_record'), name='logout'),
    path('sync-data/', views.sync_data, name='sync_data'),
]