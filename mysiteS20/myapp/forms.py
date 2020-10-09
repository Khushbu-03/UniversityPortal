
from django import forms
from django.contrib.auth.forms import _unicode_ci_compare
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from myapp.models import Order, Student, User
from django.contrib.auth import (
    password_validation,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'order_date', 'course', 'levels']
        widgets = {'student': forms.RadioSelect,
                   'order_type': forms.DateTimeInput
                   }
        labels = {'student': 'Student name',
                  'Order_type': 'Order Date',
                  'course': 'Course name',
                  'levels': 'levels'}

class InterestForm(forms.Form):
    CHOICES = [('Yes', 1), ('No', 0)]
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True)
    levels = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, required=False)
    labels = {'interested': 'interested',
              'levels': 'levels',
              'comments': 'Additional Comments'}



class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'password','first_name', 'last_name', 'email', 'city', 'interested_in']
        widgets= {'city': forms.RadioSelect}
        labels = {'username': 'User Name', 'password': 'Password', 'email':'Email','first_name': 'First Name',
                  'last_name': 'Last Name', 'city': 'City', 'interested_in': 'Enter the topics you are interested in'}

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class AccountForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['picture']

