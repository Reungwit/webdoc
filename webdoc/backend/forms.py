from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='อีเมล',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'กรอกอีเมลของคุณ',
            'autocomplete': 'email'
        })
    )
    full_name = forms.CharField(
        max_length=150,
        label='ชื่อ-นามสกุล',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'กรอกชื่อ-นามสกุล',
            'autocomplete': 'name'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'ชื่อผู้ใช้'
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'กรอกชื่อผู้ใช้',
            'autocomplete': 'username'
        })

        self.fields['password1'].label = 'รหัสผ่าน'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'กรอกรหัสผ่าน',
            'autocomplete': 'new-password'
        })

        self.fields['password2'].label = 'ยืนยันรหัสผ่าน'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'ยืนยันรหัสผ่าน',
            'autocomplete': 'new-password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("อีเมลนี้ถูกใช้งานแล้ว")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("ชื่อผู้ใช้นี้ถูกใช้งานแล้ว")
        return username



class LoginForm(forms.Form):
    email = forms.EmailField(
        label='อีเมล',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'กรอกอีเมลของคุณ',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        label='รหัสผ่าน',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'กรอกรหัสผ่าน',
            'autocomplete': 'current-password'
        })
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("อีเมลหรือรหัสผ่านไม่ถูกต้อง")
        return self.cleaned_data

    def get_user(self):
        return self.user
