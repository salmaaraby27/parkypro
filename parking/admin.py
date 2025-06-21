from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'national_id', 'subscription_type')
    list_filter = ('is_staff', 'is_active', 'subscription_type', 'nationality')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'national_id', 'profile_picture', 'phone_number', 'DOB', 'gender', 'nationality')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Subscription', {'fields': ('subscription_type', 'license_id')}),
        ('Important dates', {'fields': ('Registration_Date',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'first_name', 'last_name')
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, CustomUserAdmin)


# Garage Admin
@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'total_capacity', 'available_capacity', 'opening_hours', 'closing_hours', 'no_of_floors', 'price_per_hour', 'price_per_month', 'rating')
    search_fields = ('name', 'location')


# ParkingSlot Admin
@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'garage', 'is_occupied', 'is_reserved')
    list_filter = ('is_occupied', 'is_reserved')
    search_fields = ('slot_number', 'garage__name')


# Vehicle Admin
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vehicle_type', 'user', 'car_model', 'vehicle_color')
    search_fields = ('license_plate', 'vehicle_type', 'car_model')


# Reservation Admin
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'parking_slot', 'start_time', 'end_time', 'status', 'total_cost')
    list_filter = ('status', 'parking_slot__garage')
    search_fields = ('user__email', 'vehicle__license_plate', 'parking_slot__slot_number')


# Card Admin
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'cardholder_name', 'card_number', 'expiry_date')
    search_fields = ('user__email', 'card_number')


# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_time', 'type', 'card')
    list_filter = ('type', 'payment_time')
    search_fields = ('user__email', 'amount')


# Message Admin
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('type', 'message')
    search_fields = ('message',)


# ParkingNotification Admin
@admin.register(ParkingNotification)
class ParkingNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'notification_time', 'read')
    list_filter = ('read',)
    search_fields = ('user__email', 'message__type')


# # FamilyCommunity Admin
# @admin.register(FamilyCommunity)
# class FamilyCommunityAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_by', 'created_at')
#     search_fields = ('name', 'created_by__email')


# # FamilyMember Admin
# @admin.register(FamilyMember)
# class FamilyMemberAdmin(admin.ModelAdmin):
#     list_display = ('user', 'family', 'role', 'joined_at')
#     list_filter = ('role',)
#     search_fields = ('user__email', 'family__name')


# # FamilyInvitation Admin
# @admin.register(FamilyInvitation)
# class FamilyInvitationAdmin(admin.ModelAdmin):
#     list_display = ('inviter', 'invitee', 'family', 'accepted', 'created_at')
#     list_filter = ('accepted',)
#     search_fields = ('inviter__email', 'invitee__email', 'family__name')


# FavoriteGarage Admin
@admin.register(FavoriteGarage)
class FavoriteGarageAdmin(admin.ModelAdmin):
    list_display = ('user', 'garage')
    search_fields = ('user__email', 'garage__name')


# ParkingSubscription Admin
@admin.register(ParkingSubscription)
class ParkingSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'parking_slot', 'start_date', 'end_date', 'subscription_type', 'active')
    list_filter = ('subscription_type', 'active')
    search_fields = ('user__email', 'parking_slot__slot_number')


# ParkingSensor Admin
@admin.register(ParkingSensor)
class ParkingSensorAdmin(admin.ModelAdmin):
    list_display = ('parking_slot', 'sensor_status', 'last_maintenance', 'last_check')
    list_filter = ('sensor_status',)
    search_fields = ('parking_slot__slot_number',)


# Dashboard Admin
@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('total_income', 'last_updated')
    search_fields = ('last_updated',)

