
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from .views import GroupBasedUserRegistrationView, LoginView, LogoutView

urlpatterns = [
    path('register/', GroupBasedUserRegistrationView.as_view(), name='group_based_user_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]