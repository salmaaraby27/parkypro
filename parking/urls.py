from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'register', UserRegistrationViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'garages', GarageViewSet)
router.register(r'parking-slots', ParkingSlotViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'cards', CardViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'notifications', ParkingNotificationViewSet)
# router.register(r'families', FamilyCommunityViewSet)
# router.register(r'family-members', FamilyMemberViewSet)
# router.register(r'family-invitations', FamilyInvitationViewSet)
router.register(r'favorite-garages', FavoriteGarageViewSet)
router.register(r'subscriptions', ParkingSubscriptionViewSet)
router.register(r'sensors', ParkingSensorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('password-reset/', RequestPasswordResetEmail.as_view(), name='password-reset'),
     # path('login/', login, name='login'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]


