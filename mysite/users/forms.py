from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'phone']
        widgets = {
            'city': forms.TextInput(attrs={'placeholder': 'Your city'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your phone number'}),
        }
