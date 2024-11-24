from rest_framework import serializers
from .models import User, Artwork, Bid, Transaction, Exhibition,Notification
from rest_framework import serializers

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','role','first_name','last_name']





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
        model = Transaction
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