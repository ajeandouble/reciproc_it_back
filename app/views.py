from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import ( RegisterForm, LoginForm )

def homePageView(request):
	return render(request, 'index.html')

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
	return render(request, 'notes.html')

