from rest_framework import serializers
from .models import User, Artwork, Bid, Transcaction, Exhibition,Notification


# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','role','first_name','last_name']


# serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User  # Apne custom User model ka import karein

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Password ko hash karein
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)



# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # User object lein
        user = self.user
        
        # Role verify karein
        if user.role == 'Customer' or user.role == 'Artist':
            data['role'] = user.role
        else:
            raise serializers.ValidationError("Invalid role. Only 'Customer' or 'Artist' can log in.")

        return data




# Serializer for Artwork model
class ArtworkSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    class Meta:
        model = Artwork
        fields = ['id','title','description','category','price','upload_date','status','uploaded_by']


# serailizer for bid model
class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)
    artwork = ArtworkSerializer(read_only=True)
    class Meta:
        model = Bid
        fields = ['id','bid_amount','bid_date','bidder','artwork']


# Serializer for Transaction model
class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    artwork = ArtworkSerializer(read_only=True)

    class Meta:
        model = Transcaction
        fields = ['id','transction_id','amount','transaction_date','payment_method','user','artwork']

# Serializer for Exhibition model
class ExhibitionSerializer(serializers.ModelSerializer):
    artwork = ArtworkSerializer(read_only=True)
    class Meta:
        model = Exhibition
        fields = ['id','title','address','start_date','end_date','artwork']

# Serializer for Notification model
class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ['id','message','date','recipient']