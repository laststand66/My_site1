from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import MainUser, user_registrated, Comment



class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Your e-mail')

    class Meta:
        model = MainUser
        fields = ('username', 'email', 'displayed_email', 'first_name', 'last_name', 'about_me')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password_first = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
    password_again = forms.CharField(label='Пароль (Повторно)', widget=forms.PasswordInput, help_text='Введите пароль повторно')

    def clean_password(self):
        password_first = self.cleaned_data['password_first']
        if password_first:
            password_validation.validate_password(password_first)
        return password_first

    def clean(self):
        super().clean()
        password_first = self.cleaned_data['password_first']
        password_again = self.cleaned_data['password_again']
        if password_first and password_again != password_again:
            errors = {'password_again': ValidationError('Пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_first'])
        user.is_active = True
        if commit:
                user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = MainUser
        fields = ('username', 'email', 'password_first', 'password_again',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
