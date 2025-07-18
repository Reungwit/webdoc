from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='อีเมล',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    full_name = forms.CharField(
        max_length=150,
        label='ชื่อ-นามสกุล',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'ชื่อผู้ใช้'
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

        self.fields['password1'].label = 'รหัสผ่าน'
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})

        self.fields['password2'].label = 'ยืนยันรหัสผ่าน'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})



class LoginForm(forms.Form):
    email = forms.EmailField(
        label='อีเมล',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'กรอกอีเมล'})
    )
    password = forms.CharField(
        label='รหัสผ่าน',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'กรอกรหัสผ่าน'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data

    def get_user(self):
        return self.user
