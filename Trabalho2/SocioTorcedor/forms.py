from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import EmailField, TextInput, ModelForm
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    email = EmailField(required=True)
    first_name = TextInput()
    last_name = TextInput()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileCreateForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('cpf',)

    def save(self, user, commit=True):
        if commit:
            user_profile = UserProfile(user=user, cpf=self.cleaned_data['cpf'])
            user_profile.save()

            return user_profile