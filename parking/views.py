from .serializers import *
from rest_framework import serializers, viewsets, permissions
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Create your views here.
from django.shortcuts import redirect

def redirect_to_api(request):
    return redirect('/api/')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer


class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ParkingNotificationViewSet(viewsets.ModelViewSet):
    queryset = ParkingNotification.objects.all()
    serializer_class = ParkingNotificationSerializer


# class FamilyCommunityViewSet(viewsets.ModelViewSet):
#     queryset = FamilyCommunity.objects.all()
#     serializer_class = FamilyCommunitySerializer


# class FamilyMemberViewSet(viewsets.ModelViewSet):
#     queryset = FamilyMember.objects.all()
#     serializer_class = FamilyMemberSerializer

class ParkingSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = ParkingSubscription.objects.all()
    serializer_class = ParkingSubscriptionSerializer


class ParkingSensorViewSet(viewsets.ModelViewSet):
    queryset = ParkingSensor.objects.all()
    serializer_class = ParkingSensorSerializer


class UserRegistrationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 6. Login View
# class LoginViewSet(viewsets.ViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserLoginSerializer
#     permission_classes = [AllowAny]

#     def create(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response({"message": "Login endpoint"})



class FavoriteGarageViewSet(viewsets.ModelViewSet):
    queryset = FavoriteGarage.objects.all()
    serializer_class = FavoriteGarageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# Favorite Garage

# class FamilyInvitationViewSet(viewsets.ModelViewSet):
#     queryset = FamilyInvitation.objects.all()
#     serializer_class = FamilyInvitationSerializer


#     def create(self, request, *args, **kwargs):
#         email = request.data.get("email")
#         family_id = request.data.get("family_id")
#         try:
#             invitee = User.objects.get(email=email)
#             family = FamilyCommunity.objects.get(id=family_id)
#             invitation = FamilyInvitation.objects.create(
#                 inviter=request.user,
#                 invitee=invitee,
#                 family=family
#             )
#             return Response({"message": "Invitation sent."})
#         except User.DoesNotExist:
#             return Response({"message": "User not found"}, status=404)
#         except FamilyCommunity.DoesNotExist:
#             return Response({"message": "Family not found"}, status=404)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         accepted = request.data.get("accepted")
#         instance.accepted = accepted
#         instance.save()

#         if accepted:
#             FamilyMember.objects.create(family=instance.family, user=instance.invitee)
#             return Response({"message": "Invitation accepted and user added to family."})
#         else:
#             return Response({"message": "Invitation declined. Notification sent."})
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# parking/views.py

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class RequestPasswordResetEmail(APIView):
    def get(self, request):
        return Response({"email": ""})  # عشان يبان في browsable API

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"http://localhost:3000/reset-password-confirm/{uid}/{token}/"

            send_mail(
                subject="Reset Your Password",
                message=f"Click the link to reset your password: {reset_link}",
                from_email=None,
                recipient_list=[email],
            )
        return Response({"message": "If the email exists, a reset link has been sent."})
from django.utils.http import urlsafe_base64_decode
from rest_framework import status

User = get_user_model()

class PasswordResetConfirmView(APIView):
    def get(self, request, uidb64, token):
        # ده علشان يظهرك الفورم في browsable API
        serializer = PasswordResetSerializer()
        return Response(serializer.data)

    def post(self, request, uidb64, token):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except:
                return Response({"error": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

            if default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"message": "Password reset successful."})
            else:
                return Response({"error": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Sum, Avg


class DashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        dashboard, created = Dashboard.objects.get_or_create(id=1)
        dashboard.update_dashboard()

        data = {
            "total_users": User.objects.count(),
            "total_vehicles": Vehicle.objects.count(),
            "total_garages": Garage.objects.count(),
            "total_reservations": Reservation.objects.count(),
            "total_active_reservations": Reservation.objects.filter(status='Reserved').count(),
            "total_income": dashboard.total_income,
            "top_garages": dashboard.top_garages,
            "average_garage_rating": Garage.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
            "today_reservations": Reservation.objects.filter(start_time__date=now().date()).count(),
            "new_users_this_month": User.objects.filter(Registration_Date__gte=now() - timedelta(days=30)).count(),
            "last_updated": dashboard.last_updated,
        }

        return Response(data)
