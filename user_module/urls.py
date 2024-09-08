from django.urls import path
from . import views

urlpatterns = [
    # authentication:
    path('login/', views.login_page.as_view(), name='login_page'),
    path('register/', views.register_page.as_view(), name='register_page'),
    path('activate-account/<code>', views.activate_account, name='activate_page'),
    path('forget-password/', views.forget_password.as_view(), name='forget_password_page'),
    path('reset-password/<code>', views.reset_password.as_view(), name='reset_password_page'),
    path('change-password/', views.change_password.as_view(), name='change_password_page'),
    path('logout', views.logout_user, name="logout_page"),
    # api:
    path('getAdminUsers/', views.getAdminUsers.as_view()),
    path('getCurrentUser/', views.currentUserView.as_view(), name='current_user'),
]
