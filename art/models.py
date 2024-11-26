from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        # ('Admin', 'Admin'),
        ('Customer', 'Customer'),
        ('Artist', 'Artist'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')

      # Fixing the conflict
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Unique related name
        blank=True
    )


class Artwork(models.Model):
    STATUS_CHOICES = [
        ('Auction', 'Auction'),
        ('Fixed', 'Fixed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='artworks')

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_date = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='bids')

    def save(self, *args, **kwargs):
        # Get the highest bid for this artwork
        highest_bid = Bid.objects.filter(artwork=self.artwork).order_by('-bid_amount').first()

        if highest_bid:
            # Ensure the new bid is higher than the current highest bid
            if self.bid_amount <= highest_bid.bid_amount:
                raise ValueError("Your bid must be higher than the current highest bid.")
        else:
            # Ensure the first bid is higher than the artwork price
            if self.bid_amount <= self.artwork.price:
                raise ValueError("Your bid must be higher than the artwork's price.")

        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.bidder.username} + ' - ' + {self.artwork.title}"
    
class Transaction(models.Model):
    Payment_Method_Choices = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Net Banking', 'Net Banking'),
    ]


    transaction_id = models.CharField(max_length=100,unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=Payment_Method_Choices)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='transactions')
    artwork = models.OneToOneField(Artwork,on_delete=models.CASCADE,related_name='transactions')

    def __str__(self):
        return f"{self.user.username} + ' by ' + {self.artwork.title}"
    

class Exhibition(models.Model):
    title = models.CharField(max_length=200)
    address = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    artwork = models.ForeignKey(Artwork,on_delete=models.CASCADE,related_name='exhibitions')

    def __str__(self):
        return self.title

class Notification(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')

    def __str__(self):
        return self.message 