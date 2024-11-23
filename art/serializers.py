from rest_framework import serializers
from .models import User, Artwork, Bid, Transcaction, Exhibition,Notification
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken

# Serializer for User model
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','username','email','role','first_name','last_name']




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


# # Serializer for Artwork model
# class ArtworkSerializer(serializers.ModelSerializer):
#     uploaded_by = UserSerializer(read_only=True)
#     class Meta:
#         model = Artwork
#         fields = ['id','title','description','category','price','upload_date','status','uploaded_by']


# # serailizer for bid model
# class BidSerializer(serializers.ModelSerializer):
#     bidder = UserSerializer(read_only=True)
#     artwork = ArtworkSerializer(read_only=True)
#     class Meta:
#         model = Bid
#         fields = ['id','bid_amount','bid_date','bidder','artwork']


# # Serializer for Transaction model
# class TransactionSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     artwork = ArtworkSerializer(read_only=True)

#     class Meta:
#         model = Transcaction
#         fields = ['id','transction_id','amount','transaction_date','payment_method','user','artwork']

# # Serializer for Exhibition model
# class ExhibitionSerializer(serializers.ModelSerializer):
#     artwork = ArtworkSerializer(read_only=True)
#     class Meta:
#         model = Exhibition
#         fields = ['id','title','address','start_date','end_date','artwork']

# # Serializer for Notification model
# class NotificationSerializer(serializers.ModelSerializer):
#     recipient = UserSerializer(read_only=True)
#     class Meta:
#         model = Notification
#         fields = ['id','message','date','recipient']