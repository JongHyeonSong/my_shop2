from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields="__all__"
        exclude = ['user']
        labels = {
            'name': '닉네임',
            'phone': '휴대전화 번호',
            'email': '이메일',
             'profile_pic': '프로필사진',
        }
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields="__all__"

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username', 'email', 'password1', 'password2']