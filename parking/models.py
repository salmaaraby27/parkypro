from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from pyexpat.errors import messages


# Create your models here.
from django.contrib.auth.models import BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, national_id=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not username:
            raise ValueError("Username must be provided")
        if not national_id:
            raise ValueError("National ID must be provided for regular users")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, national_id=national_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if not username:
            raise ValueError("Username must be provided for superusers")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

def validate_national_id(value):
    if not value.isdigit() or len(value) != 14:
        raise ValidationError("National ID must be exactly 14 digits.")

class User(AbstractBaseUser, PermissionsMixin):
    class Nationality(models.TextChoices):
        EGYPT = 'EGY', 'Egypt'
        USA = 'USA', 'United States of America'
        CANADA = 'CAN', 'Canada'
        UK = 'UK', 'United Kingdom'
        INDIA = 'IN', 'India'
        AUSTRALIA = 'AU', 'Australia'
        GERMANY = 'DE', 'Germany'
        FRANCE = 'FR', 'France'
        OTHER = 'OT', 'Other'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default=False)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True ,  unique=True)
    password = models.CharField(max_length=255, null=False )
    DOB = models.DateField(default=now)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')],default='Male')
    national_id = models.CharField(max_length=20, null=True, blank=True)
    nationality = models.CharField(max_length=3,choices=Nationality.choices,default=Nationality.OTHER)
    subscription_type  = models.CharField(max_length=20, choices=[('standard', 'standard'), ('VIP', 'VIP')],default='standard')
    license_id = models.ImageField(upload_to='', blank=True, null=False)
    Registration_Date = models.DateTimeField(default=now)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='parking_user_set',  # Change related_name to avoid conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='parking_user_permissions',  # Change related_name to avoid conflict
        blank=True,
    )
# Garage model
class Garage(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    location = models.CharField(max_length=255)  # Can be an address or coordinates
    total_capacity = models.PositiveIntegerField()  # Total number of parking spots in the garage
    available_capacity = models.PositiveIntegerField()  # Number of available parking spots
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()
    no_of_floors = models.CharField(max_length=255, default=1)
    photo = models.ImageField(upload_to='', blank=True, null=True)
    price_per_hour = models.CharField(max_length=100, default='80')
    price_per_month = models.CharField(max_length=100 , default='80')
    rating =models.CharField(max_length=100 , default='5')

    def __str__(self):
        return f"Garage: {self.name} at {self.location}"

    # def update_available_capacity(self):
    #     # Logic to update available capacity based on occupied parking slots
    #     self.available_capacity = self.total_capacity - self.parkingzone_set.aggregate(models.Sum('total_slots'))['total_slots__sum']
    #     self.save()

class ParkingSlot(models.Model):
    garage = models.ForeignKey('Garage', on_delete=models.CASCADE, related_name='slots')
    slot_number = models.CharField(max_length=20)
    is_occupied = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Slot {self.slot_number} "

    def occupy(self, vehicle):
        self.is_occupied = True
        self.vehicle = vehicle
        self.save()

    def vacate(self):
        self.is_occupied = False
        self.vehicle = None
        self.save()

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=15, unique=True)
    vehicle_type = models.CharField(max_length=20)  # e.g., Car, Bike, Truck
    user = models.ForeignKey('parking.User',on_delete=models.CASCADE)
    car_model = models.CharField(max_length=20, default=False)
    vehicle_color = models.CharField(max_length=20,default=False)

    def __str__(self):
        return f"{self.vehicle_type} - {self.license_plate}"


class Reservation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='Reserved',
                              choices=[('Reserved', 'Reserved'),
                                       ('cancelled', 'cancelled'),
                                       ('Pending', 'Pending')])
    total_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # New field
    # family = models.ForeignKey('FamilyCommunity', on_delete=models.SET_NULL, null=True, blank=True)  # Link reservation to family

    def calculate_total_cost(self):
        garage = self.parking_slot.garage
        try:
            price_per_hour = float(garage.price_per_hour)
        except ValueError:
            price_per_hour = 0.0

        duration = self.end_time - self.start_time
        duration_in_hours = duration.total_seconds() / 3600
        self.total_cost = round(price_per_hour * duration_in_hours, 2)
        # Do not call self.save() here!

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.total_cost is None:
            self.calculate_total_cost()

    def __str__(self):
        return f"Reservation for {self.vehicle.license_plate} in Slot {self.parking_slot.slot_number}"


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    cardholder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=14)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Card for {self.user.username} - {self.card_number}"

class Transaction(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    payment_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=20,
        choices=[('charge','charge'),('spend','spend')],
        default='charge'
    )
    card = models.ForeignKey('Card', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    def __str__(self):
        return f"transaction type : {self.type}- Amount: {self.amount} "

class Message(models.Model):
    type = models.CharField(max_length=100,
                            choices=[('Reservation Reminder','Reservation Reminder'),
                                      ('Payment Reminder','Payment Reminder'),
                                      ('General Alert', 'General Alert')])
    message = models.TextField()

    def __str__(self):
        return f"message : {self.message}"

class ParkingNotification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    notification_time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message.type}"

# class FamilyCommunity(models.Model):
#     name = models.CharField(max_length=100, unique=True)  # Family name
#     created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="family_creator")  # Admin of the family
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Family Community: {self.name}"

# class FamilyMember(models.Model):
#     family = models.ForeignKey(FamilyCommunity, on_delete=models.CASCADE, related_name="members")
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=[('Admin', 'Admin'), ('Member', 'Member')], default='Member')
#     joined_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.role} in {self.family.name}"

# class FamilyInvitation(models.Model):
#     inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
#     invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
#     family = models.ForeignKey(FamilyCommunity, on_delete=models.CASCADE)
#     accepted = models.BooleanField(null=True, blank=True)  # None = pending, True = accepted, False = rejected
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Invitation from {self.inviter} to {self.invitee} for {self.family.name}"

class FavoriteGarage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_garages')
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'garage')

    def __str__(self):
        return f"{self.user.username}'s Favorite Garage: {self.garage.name}"

class ParkingSubscription(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE)  # Which zone the subscription is for
    start_date = models.DateField()
    end_date = models.DateField()
    subscription_type = models.CharField(max_length=20, choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly')])
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s {self.subscription_type} Subscription for {self.parking_slot.slot_number}"

class ParkingSensor(models.Model):
    parking_slot = models.OneToOneField('ParkingSlot', on_delete=models.CASCADE)
    sensor_status = models.CharField(max_length=20,
                                     choices=[('Active', 'Active'), ('Inactive', 'Inactive')],
                                     default='Active')
    last_maintenance = models.DateTimeField(null=True, blank=True)
    last_check = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sensor for Slot {self.parking_slot.slot_number} - {self.sensor_status}"

from django.db.models import Count, Sum, Avg


from django.db import models
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from datetime import timedelta
from django.utils.timezone import now

from .models import User, Vehicle, Garage, Reservation, Transaction


from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

class Dashboard(models.Model):
    # Only fields here – no `.objects.count()` stuff outside methods!
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    top_garages = models.JSONField(default=list)
    last_updated = models.DateTimeField(default=timezone.now)

    def update_dashboard(self):
        from parking.models import Reservation, Garage, User, Vehicle  # avoid circular import

        # Total income
        self.total_income = Reservation.objects.aggregate(
            total=Sum('total_cost')
        )['total'] or 0.00

        # Top garages based on number of reservations
        top_garages_qs = Garage.objects.annotate(
            reservation_count=Count('slots__reservations')
        ).order_by('-reservation_count')[:5]

        top_garages_data = []
        for garage in top_garages_qs:
            income = Reservation.objects.filter(parking_slot__garage=garage).aggregate(
                total=Sum('total_cost')
            )['total'] or 0.00

            top_garages_data.append({
                'name': garage.name,
                'location': garage.location,
                'reservation_count': garage.reservation_count,
                'income': income
            })

        self.top_garages = top_garages_data
        self.last_updated = timezone.now()
        self.save()

    def __str__(self):
        return f"Dashboard updated at {self.last_updated}"

