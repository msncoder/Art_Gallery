from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from .models import Artwork, Bid, Notification
from .serializers import ArtworkSerializer, BidSerializer
from .Custom_Permissions import IsArtist, IsCustomer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class BaseListView(ListAPIView):
    """
    Base List View to handle common configurations.
    """
    permission_classes = []
    serializer_class = None


class BaseCreateView(CreateAPIView):
    """
    Base Create View to handle common configurations.
    """
    permission_classes = []
    serializer_class = None


class BaseListCreateView(ListCreateAPIView):
    """
    Base List and Create View to handle common configurations.
    """
    permission_classes = []
    serializer_class = None




# Artist Artwork View
class ArtistArtworkView(BaseListCreateView):
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = ArtworkSerializer

    def get_queryset(self):
        return Artwork.objects.filter(uploaded_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


# Artist Bids View
class ArtistBidsView(BaseListView):
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = BidSerializer

    def get_queryset(self):
        return Bid.objects.filter(artwork__uploaded_by=self.request.user)


# Customer Gallery View
class CustomerGalleryView(BaseListView):
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = ArtworkSerializer

    def get_queryset(self):
        return Artwork.objects.all()


# Customer Bid View
class CustomerBidView(BaseCreateView):
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = BidSerializer

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)



# API for placing a bid
class PlaceBidView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can bid

    def post(self, request):
        artwork_id = request.data.get('artwork_id')
        bid_amount = request.data.get('bid_amount')

        try:
            artwork = Artwork.objects.get(id=artwork_id)
            artwork = Artwork.objects.get(id=artwork_id)

            # Save the bid
            bid = Bid(
                bid_amount=bid_amount,
                artwork=artwork,
                bidder=request.user
            )
            bid.save()

            # Response with artwork price and highest bid
            highest_bid = Bid.objects.filter(artwork=artwork).order_by('-bid_amount').first()
            return Response({
                "message": "Bid placed successfully!",
                "artwork_price": artwork.price,
                "highest_bid": highest_bid.bid_amount
            }, status=201)

        except Artwork.DoesNotExist:
            return Response({"error": "Artwork not found."}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)



#API to Fetch Highest Bid and Price
class ArtworkBidsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, artwork_id):
        try:
            artwork = Artwork.objects.get(id=artwork_id)

            # Get highest bid for the artwork
            highest_bid = Bid.objects.filter(artwork=artwork).order_by('-bid_amount').first()
            highest_bid_amount = highest_bid.bid_amount if highest_bid else None

            return Response({
                "artwork_title": artwork.title,
                "artwork_price": artwork.price,
                "highest_bid": highest_bid_amount
            }, status=200)

        except Artwork.DoesNotExist:
            return Response({"error": "Artwork not found."}, status=404)



# API for determining the winner
class DetermineWinnerView(APIView):
    permission_classes = [IsAuthenticated]  # Authenticated users can check

    def get(self, request, artwork_id):
        try:
            artwork = Artwork.objects.get(id=artwork_id)

            # Get the highest bid; in case of a tie, earliest bid wins
            highest_bid = Bid.objects.filter(artwork=artwork).order_by('-bid_amount', 'bid_date').first()

            if highest_bid:
                # Notify the winner
                Notification.objects.create(
                    recipient=highest_bid.bidder,
                    message=f"Congratulations! You have won the bid for '{artwork.title}' with a bid of ${highest_bid.bid_amount}."
                )
                return Response({
                    "winner": highest_bid.bidder.username,
                    "bid_amount": highest_bid.bid_amount,
                    "artwork": artwork.title
                }, status=200)
            return Response({"message": "No bids found for this artwork."})

        except Artwork.DoesNotExist:
            return Response({"error": "Artwork not found."}, status=404)




# Winning Bid Notification
class WinningBidNotificationView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, artwork_id):
        try:
            bid = Bid.objects.get(artwork_id=artwork_id, bidder=request.user)
            # Logic to determine winning bid
            is_winner = True  # Replace with actual logic

            if is_winner:
                Notification.objects.create(
                    recipient=request.user,
                    message=f"You have won the bid for {bid.artwork.title}."
                )
                return Response({"message": "You have won the bid!"})
            else:
                return Response({"message": "You did not win this bid."})
        except Bid.DoesNotExist:
            return Response({"error": "Bid not found."}, status=404)





# Stripe Payment View
# Uncomment and configure settings before using this view
# import stripe
# stripe.api_key = settings.STRIPE_SECRET_KEY
# 
# class StripePaymentView(APIView):
#     permission_classes = [IsAuthenticated, IsCustomer]
# 
#     def post(self, request):
#         amount = request.data.get('amount')
#         try:
#             # Stripe Payment Intent
#             intent = stripe.PaymentIntent.create(
#                 amount=int(float(amount) * 100),  # Convert to cents
#                 currency='usd',
#                 payment_method_types=['card'],
#             )
#             return Response({
#                 "client_secret": intent['client_secret']
#             })
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)
