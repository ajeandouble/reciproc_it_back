
   
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import Note
from .models import MyUser

# Account management serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'date_of_birth', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = MyUser(email=self.validated_data['email'],
                      date_of_birth=self.validated_data['date_of_birth'],
                      first_name=self.validated_data['first_name'],
                      last_name=self.validated_data['first_name'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class RefreshTokenSerializer(serializers.Serializer):
    """
		Refresh token serializer used by the logout view.
    """
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is invalid or expired'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
    
# Notes serializers
class NoteSerializer(serializers.ModelSerializer):
	"""
		Used for the creation and retrieval of notes.
	"""
	class Meta:
		model = Note
		fields = ('id', 'created_by', 'description', 'created_at', 'updated_at', 'name')

class NoteUpdateSerializer(serializers.ModelSerializer):
	"""
		Used to update only the relevant fields.
	"""
	class Meta:
		model = Note
		fields = ('id', 'description', 'updated_at', 'name')
