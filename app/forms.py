from django import forms

# TODO: required fields

class RegisterForm(forms.Form):
	email = forms.EmailField(label='Email', max_length=100)
	first_name = forms.CharField(label='Firstname', max_length=100, )
	last_name = forms.CharField(label='Lastname', max_length=100, )
	date_of_birth = forms.DateField()
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

class LoginForm(forms.Form):
	email = forms.EmailField(label='Email')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
