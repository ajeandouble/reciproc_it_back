
   
from rest_framework import serializers
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
    
# Notes serializers
class NoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Note
		fields = ('id', 'created_by', 'description', 'created_at', 'updated_at', 'name')

class NoteUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Note
		fields = ('id', 'description', 'updated_at', 'name')
