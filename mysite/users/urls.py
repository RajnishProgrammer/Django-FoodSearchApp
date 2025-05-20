from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, UserProfileUpdateView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='edit_profile'),
]
