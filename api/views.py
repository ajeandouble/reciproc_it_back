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
from .serializers import RegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime	
from django.conf import settings
from django.middleware import csrf
import copy
import json
from rest_framework import viewsets

def get_tokens_for_user(user):
	refresh = RefreshToken.for_user(user)

	return {
		'refresh': str(refresh),
		'access': str(refresh.access_token),
	}

# Account management views
class RegistrationView(APIView):
	def post(self, request):
		serializer = RegistrationSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
	def post(self, request):
		print(request)
		if 'email' not in request.data or 'password' not in request.data:
			return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
		email = request.POST['email']
		password = request.POST['password']
		print(email, password)
		user = authenticate(username=email, password=password)
		if user is not None:
			login(request, user)
			auth_data = get_tokens_for_user(request.user)
			print(auth_data)
			return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
		return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
	def post(self, request):
		logout(request)
		return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


# Notes CRUD operations views
class NotesList(generics.ListCreateAPIView):
	permission_classes = [IsAuthenticated, ]
	queryset = Note.objects.all()
	serializer_class = NoteSerializer
	def get_queryset(self):
		user = self.request.user
		return Note.objects.filter(created_by=user)

class NoteDetail(generics.RetrieveAPIView):
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