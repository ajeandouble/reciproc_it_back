from rest_framework import generics
from .models import Note
from .serializers import NoteSerializer, NoteUpdateSerializer
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, RefreshTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime	
from django.conf import settings
from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets

def get_tokens_for_user(user):
	refresh = RefreshToken.for_user(user)

	return {
		'refresh': str(refresh),
		'access': str(refresh.access_token),
	}

# Account management views

class RegistrationView(APIView):
	"""
		Checks for invalid form and duplicate accounts.
		Add new account to users database.
	"""
	def post(self, request):
		serializer = RegistrationSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
	"""
		Login and returns a response with the jwt access and refresh tokens.
	"""
	def post(self, request):
		if 'email' not in request.data or 'password' not in request.data:
			return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=email, password=password)
		if user is not None:
			login(request, user)
			auth_data = get_tokens_for_user(request.user)
			return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
		return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(generics.GenericAPIView):
	"""
		Logout the current authenti and blacklist the provided refresh token.
	"""
	serializer_class = RefreshTokenSerializer
	permission_classes = [IsAuthenticated, ]
	def post(self, request, *args):
		sz = self.get_serializer(data=request.data)
		sz.is_valid(raise_exception=True)
		sz.save()
		return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


# Notes CRUD operations views
class NotesList(generics.ListCreateAPIView):
	"""
		Returns the list of notes for the current authenticated user.
	"""
	permission_classes = [IsAuthenticated, ]
	queryset = Note.objects.all()
	serializer_class = NoteSerializer
	def get_queryset(self):
		user = self.request.user
		return Note.objects.filter(created_by=user)

class NoteDetail(generics.RetrieveAPIView):
	"""
		Returns note corresponding to provided ID for the current authenticated user.
	"""
	permission_classes = [IsAuthenticated, ]
	queryset = Note.objects.all()
	serializer_class = NoteSerializer
	lookup_url_kwarg = "pk"
	def get_queryset(self):
		id = self.kwargs.get(self.lookup_url_kwarg)
		user = self.request.user
		return Note.objects.filter(created_by=user, id=id)

# PATCH/DELETE note
class NoteUpdate(generics.RetrieveUpdateDestroyAPIView):
	"""
		Delete or update a note for the current authenticated user.
		In case of update, change the updated_at field accordingly.
	"""
	permission_classes = [IsAuthenticated, ]
	serializer_class = NoteUpdateSerializer
	queryset = Note.objects.all()
	serializer_class = NoteUpdateSerializer
	lookup_field = 'pk'
	def update(self, request, *args, **kwargs):
		print(request.data)
		# check if good user
		request.data._mutable = True
		request.data['updated_at'] = datetime.now()
		response = super().update(request, *args, **kwargs)
		return Response({
			'status': 200,
			'msg': 'Note updated',
			'data': response.data
		})


# POST/ create note
class NoteAdd(generics.CreateAPIView):
	"""
		Add a note for the current authenticated user.
		Populate created_at, updated_at and created_by fields automatically.
	"""
	permission_classes = [IsAuthenticated, ]
	model = Note
	queryset = Note.objects.all()
	serializer_class = NoteSerializer
	def create(self, request, *args, **kwargs):
		print(request.data)
		request.data._mutable = True
		request.data['created_at'] = datetime.now()
		request.data['updated_at'] = datetime.now()
		request.data['created_by'] = str(request.user)
		response = super().create(request, *args, **kwargs)
		return Response({
			'status': 200,
			'msg': 'Note created',
			'data': response.data
		})