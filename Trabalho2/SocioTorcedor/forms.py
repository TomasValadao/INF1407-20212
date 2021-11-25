from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from .models import UserProfile

class UserProfileCreateForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('email', 'cpf')

    def save(self, user, commit=True):
        if commit:
            user_profile = UserProfile(user=user, email=self.cleaned_data['email'], cpf=self.cleaned_data['cpf'])
            user_profile.save()

            return user_profile