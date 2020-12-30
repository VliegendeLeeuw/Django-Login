from django import forms


class UserRegistration(forms.Form):
    username = forms.CharField(label='Username:', max_length=32)
    email = forms.EmailField(label='Email:', max_length=100)
    firstname = forms.CharField(label='First name', max_length=100)
    lastname = forms.CharField(label='Last name', max_length=100)
    password = forms.CharField(
        label='Password', max_length=32, widget=forms.PasswordInput)
    confirmation = forms.CharField(
        label='Confirm password', max_length=32, widget=forms.PasswordInput)
