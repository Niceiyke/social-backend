from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import myUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = myUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = myUser
        fields = ('email',)