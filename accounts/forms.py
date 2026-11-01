from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class AdminUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = '__all__'


class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'
