from rest_framework import serializers
from .models import User, Artwork, Bid, Transcaction, Exhibition

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','role','first_name','last_name']