from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard_page.as_view(), name='admin_dashboard_page')
]
