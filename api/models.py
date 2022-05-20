from django.db import models
import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Authentication API

class MyUserManager(BaseUserManager):
	def create_user(self, email, date_of_birth, first_name, last_name, password):
		if not email:
			raise ValueError('Users must have an email address')
		if not password:
			raise ValueError('Users must have a password')
		if not date_of_birth:
			raise ValueError('Users must have a birth date')
		if not first_name:
			raise ValueError('Users must have a first name')
		if not last_name:
			raise ValueError('Users must have a last name')

		user = self.model(
			email=self.normalize_email(email),
			date_of_birth=date_of_birth,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	# def create_superuser(self, email, date_of_birth, password=None):
	# 	"""
	# 	Creates and saves a superuser with the given email, date of
	# 	birth and password.
	# 	"""
	# 	user = self.create_user(
	# 		email,
	# 		password=password,
	# 		date_of_birth=date_of_birth,
	# 	)
	# 	user.is_admin = True
	# 	user.save(using=self._db)
	# 	return user


class MyUser(AbstractBaseUser):
	email = models.EmailField(
		max_length=255,
		unique=True,
	)
	date_of_birth = models.DateField()
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['date_of_birth', 'email', 'password', 'password2', 'first_name', 'last_name']

	def __str__(self):
		return self.email

	# def has_perm(self, perm, obj=None):
	# 	"Does the user have a specific permission?"
	# 	# Simplest possible answer: Yes, always
	# 	return True

	# def has_module_perms(self, app_label):
	# 	"Does the user have permissions to view the app `app_label`?"
	# 	# Simplest possible answer: Yes, always
	# 	return True

# Note API


class Note(models.Model):
	id = models.UUIDField(primary_key=True)
	userId = models.UUIDField()
	createdAt = models.DateTimeField()
	updatedAt = models.DateTimeField()
	title = models.CharField(max_length=50)
	text = models.TextField()

	def __str__(self):
		return self.title
