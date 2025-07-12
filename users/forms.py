from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100, validators=[validate_email], help_text='Required')
    birth_date = forms.DateField(widget=DateInput)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            customer = Customer.objects.create(
                user=user, birth_date=self.cleaned_data.get('birth_date'))
            customer.save()
        return user

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            customer = Customer.objects.create(
                user=user, birth_date=self.cleaned_data.get('birth_date'))
            customer.save()
        return user


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100, validators=[validate_email], help_text='Required')
    field = forms.ChoiceField(choices=(('Air Conditioner', 'Air Conditioner'),
                                      ('All in One', 'All in One'),
                                      ('Carpentry', 'Carpentry'),
                                      ('Electricity', 'Electricity'),
                                      ('Gardening', 'Gardening'),
                                      ('Home Machines', 'Home Machines'),
                                      ('House Keeping', 'House Keeping'),
                                      ('Interior Design', 'Interior Design'),
                                      ('Locks', 'Locks'),
                                      ('Painting', 'Painting'),
                                      ('Plumbing', 'Plumbing'),
                                      ('Water Heaters', 'Water Heaters')))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            company = Company.objects.create(
                user=user, field=self.cleaned_data.get('field'))
            company.save()
        return user

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            company = Company.objects.create(
                user=user, field=self.cleaned_data.get('field'))
            company.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email', 'autocomplete': 'off'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
