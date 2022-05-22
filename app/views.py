from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import ( RegisterForm, LoginForm )
import requests

# This app has solely been added for test-purposes of the register/login process.
# I found the pdf instructions to be a bit ambiguous about whether I should add an actual
# registration form.
# In typical production setup I do believe we would either:
#  - another front consuming the API authorized authorized by the CORS policy
#  - re-implement views or use them directly from the front main app
# I have tested all entry points on postman and it seems to work fine

def homePageView(request):
	# if request.method == 'POST':
	# 	form = LoginForm(request.POST)
	# 	print(request.POST)
	# 	print(form.is_valid())
	# 	response = request.post('localhost:')
	# 	if form.is_valid():
	# 		return HttpResponseRedirect('/notes')

	# else:
	form = LoginForm()
	return render(request, 'index.html', {'form': form})

def RegisterView(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RegisterForm(request.POST)
		# check whether it's valid:
		print(request.POST)
  		# if form.is_valid():
		# 	return HttpResponseRedirect('/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = RegisterForm()

	return render(request, 'register.html', {'form': form})


def NotesView(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')
	# MOVE MODELS/VIEWS here
	# CHECK IF USER IS AUTHENTICATED IN THE API
	# ADD A FIELD IN THE TEMPLATE TO ADD A NEW N OTE
	return render(request, 'notes.html')

