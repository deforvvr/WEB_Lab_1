from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Review, ContactMessage, Product
from .validators import validate_password_complexity


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя"""
    username = forms.CharField(
        max_length=150,
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Логин', 'required': True})
    )
    first_name = forms.CharField(
        max_length=150,
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'required': True})
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона', 'type': 'tel', 'required': True})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'required': True}),
        validators=[validate_password_complexity]
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль', 'required': True})
    )
    consent = forms.BooleanField(
        label='Согласен с условиями обработки персональных данных',
        required=True
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'phone', 'password']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Хеширование пароля
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя"""
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Логин', 'required': True})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'required': True})
    )


class ReviewForm(forms.ModelForm):
    """Форма для отзыва"""
    name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'required': True})
    )
    text = forms.CharField(
        label='Отзыв',
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ваш отзыв', 'required': True})
    )
    
    class Meta:
        model = Review
        fields = ['name', 'text']


class ContactForm(forms.ModelForm):
    """Форма контактов"""
    name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'required': True})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'required': True})
    )
    subject = forms.CharField(
        max_length=200,
        label='Тема',
        widget=forms.TextInput(attrs={'placeholder': 'Тема', 'required': True})
    )
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Сообщение', 'required': True})
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

