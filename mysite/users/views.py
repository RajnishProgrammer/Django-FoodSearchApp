from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileForm
from django.urls import reverse_lazy


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('restaurant_list')

    # override for edit only the logged-in user's profile
    def get_object(self):
        return self.request.user.profile