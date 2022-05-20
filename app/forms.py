from django import forms

# TODO: required fields
class RegisterForm(forms.Form):
	email = forms.EmailField(label='Email', max_length=100)
	first_name = forms.CharField(label='Firstname', max_length=100, )
	last_name = forms.CharField(label='Lastname', max_length=100, )
	date_of_birth = forms.DateField()
	password = forms.CharField()
	password2 = forms.CharField()

class LoginForm(forms.Form):
	password = forms.EmailField(label='Email')
	your_name = forms.PasswordInput()
