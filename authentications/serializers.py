from rest_framework import serializers
from art.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

class GroupBasedUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_role(self, value):
        # Sirf "Customer" aur "Artist" roles ko allow karein
        if value not in ['Customer', 'Artist']:
            raise serializers.ValidationError("Invalid role. Choose either 'Customer' or 'Artist'.")
        return value

    def create(self, validated_data):
        # Password hash karein
        validated_data['password'] = make_password(validated_data['password'])
        
        # User create karein
        user = super().create(validated_data)
        
        # Role ke hisaab se group assign karein
        group_name = user.role  # Role ka naam group ka naam hai
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['Customer', 'Artist'])

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        role = attrs.get('role')

        # User authenticate karein
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if user.role != role:
            raise serializers.ValidationError(f"User does not have the role: {role}.")

        # Agar sab kuch sahi hai, to user return karein
        attrs['user'] = user
        return attrs

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            # Refresh token blacklist karein
            refresh = RefreshToken(self.token)
            refresh.blacklist()
        except Exception as e:
            raise serializers.ValidationError("Invalid or expired refresh token.")

