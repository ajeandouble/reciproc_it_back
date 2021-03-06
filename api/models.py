from django.db import models
import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
import uuid

# Authentication API

class MyUserManager(BaseUserManager):
	"""
		Overrides default django user model.
	"""
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
			first_name=date_of_birth,
			last_name=date_of_birth,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, email, date_of_birth, first_name, last_name, password):
		user = self.create_user(
			email,
			password=password,
			date_of_birth=date_of_birth,
			first_name=first_name,
			last_name=last_name,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
	"""
		User account model.
		DB fields:	email, date_of_birth, firstname, lastname, password
	"""
	email = models.EmailField(
		max_length=255,
		unique=True,
	)
	date_of_birth = models.DateField()
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	objects = MyUserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['date_of_birth', 'password', 'password2', 'first_name', 'last_name']

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		return True

# Note API

class BaseNote(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	created_by = models.CharField(max_length=100)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	class Meta:
		abstract = True
  
class Note(BaseNote):
	"""
 		Inherits from abstract base class.
		DB fields:
			id (primarey key, uuid type, unique with auto-increment)
			created_by (id of the user)
			created_at (time stamp for creation time)
			updated_at (time stamp for update time)
			name (note title)
			description (note content)
	"""
	name = models.CharField(max_length=50)
	description = models.TextField()

	def __str__(self):
		return self.title
