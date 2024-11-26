from django.urls import path
from .views import (
    ArtistArtworkView, ArtistBidsView,
    CustomerGalleryView, CustomerBidView,
    WinningBidNotificationView, PlaceBidView, DetermineWinnerView,
    ArtworkBidsView
)

urlpatterns = [
    path('artist/artworks/', ArtistArtworkView.as_view(), name='artist-artworks'),
    path('artist/bids/', ArtistBidsView.as_view(), name='artist-bids'),
    path('customer/gallery/', CustomerGalleryView.as_view(), name='customer-gallery'),
    path('customer/bid/', CustomerBidView.as_view(), name='customer-bid'),
    path('customer/notification/<int:artwork_id>/', WinningBidNotificationView.as_view(), name='winning-notification'),
    path('bids/winner/<int:artwork_id>/', DetermineWinnerView.as_view(), name='determine-winner'),
    path('bids/place/', PlaceBidView.as_view(), name='place-bid'),
    path('artworks/<int:artwork_id>/bids/', ArtworkBidsView.as_view(), name='artwork-bids'),

    # path('payment/stripe/', StripePaymentView.as_view(), name='stripe-payment'),
]
