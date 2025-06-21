from django.core.management.base import BaseCommand
from faker import Faker
import random  # Add this import statement

from django.utils import timezone
from parking.models import *
class Command(BaseCommand):
    help = 'Generate fake data for the parking system'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generate fake data for Users
        for _ in range(10):  # Adjust the number as needed
            email = fake.email()
            username = fake.user_name()
            phone_number = fake.phone_number()[:15]
            password = fake.password()
            national_id = fake.random_number(digits=14)
            DOB = fake.date_of_birth()
            gender = fake.random_element(elements=('Male', 'Female'))
            nationality = fake.random_element(elements=('EGY', 'USA', 'CAN', 'UK', 'IN', 'AU', 'DE', 'FR', 'OT'))

            user = User.objects.create(
                email=email,
                username=username,
                phone_number=phone_number,
                password=password,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                DOB=DOB,
                gender=gender,
                national_id=national_id,
                nationality=nationality,
                license_id=fake.image_url(),
                Registration_Date=timezone.now(),
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))

        # Generate fake data for Garages
        for _ in range(3):
            garage_name = fake.company()
            garage_location = fake.address()
            total_capacity = fake.random_int(min=50, max=200)
            available_capacity = fake.random_int(min=1, max=total_capacity)
            opening_hours = fake.time()
            closing_hours = fake.time()

            garage = Garage.objects.create(
                name=garage_name,
                location=garage_location,
                total_capacity=total_capacity,
                available_capacity=available_capacity,
                opening_hours=opening_hours,
                closing_hours=closing_hours,
                no_of_floors=fake.random_int(min=1, max=10),
                price_per_hour='80',
                price_per_month='800',
                rating='5'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created garage: {garage.name}'))

        # Generate fake data for ParkingSlots
        for _ in range(5):
            garage = Garage.objects.order_by('?').first()  # Pick a random garage
            slot_number = fake.random_int(min=1, max=100)

            parking_slot = ParkingSlot.objects.create(
                garage=garage,
                slot_number=slot_number,
                is_occupied=False,
                is_reserved=False
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created parking slot: {parking_slot.slot_number}'))

        # Generate fake data for Vehicles
        for _ in range(5):
            user = User.objects.order_by('?').first()  # Pick a random user
            vehicle_type = fake.random_element(elements=('Car', 'Bike', 'Truck'))
            vehicle = Vehicle.objects.create(
                license_plate=fake.license_plate(),
                vehicle_type=vehicle_type,
                user=user,
                car_model=fake.word(),
                vehicle_color=fake.color_name(),
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created vehicle: {vehicle.license_plate}'))

        # Generate fake data for Reservations
        for _ in range(5):
            user = User.objects.order_by('?').first()  # Pick a random user
            vehicle = Vehicle.objects.order_by('?').first()  # Pick a random vehicle
            parking_slot = ParkingSlot.objects.order_by('?').first()  # Pick a random parking slot
            start_time = fake.date_this_year()
            end_time = fake.date_this_year()

            reservation = Reservation.objects.create(
                user=user,
                vehicle=vehicle,
                parking_slot=parking_slot,
                start_time=start_time,
                end_time=end_time,
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created reservation for vehicle: {reservation.vehicle.license_plate}'))

        # Generate fake data for Cards
        for _ in range(5):
            user = User.objects.order_by('?').first()  # Pick a random user
            card = Card.objects.create(
                user=user,
                cardholder_name=fake.name(),
                card_number=fake.credit_card_number(card_type='mastercard'),
                expiry_date=fake.date_this_century(),
                cvv=fake.random_number(digits=3),
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created card for user: {card.user.username}'))

        # Generate fake data for Transactions
        for _ in range(5):
            user = User.objects.order_by('?').first()  # Pick a random user
            card = Card.objects.order_by('?').first()  # Pick a random card
            amount = fake.random_int(min=10, max=500)
            transaction = Transaction.objects.create(
                user=user,
                amount=amount,
                type=fake.random_element(elements=('charge', 'spend')),
                card=card,
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created transaction: {transaction.amount}'))

        # Generate fake data for FamilyCommunity
        for _ in range(2):
            creator = User.objects.order_by('?').first()  # Pick a random user
            family = FamilyCommunity.objects.create(
                name=fake.word(),
                created_by=creator
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created family community: {family.name}'))

        # Generate fake data for FamilyMember
        for _ in range(5):
            family = FamilyCommunity.objects.order_by('?').first()  # Pick a random family
            user = User.objects.order_by('?').first()  # Pick a random user
            role = fake.random_element(elements=('Admin', 'Member'))

            family_member = FamilyMember.objects.create(
                family=family,
                user=user,
                role=role
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully added family member: {family_member.user.username} to {family_member.family.name}'))

        # Generate fake data for Dashboard (update every time)
        dashboard = Dashboard.objects.create()
        dashboard.update_dashboard()
        self.stdout.write(self.style.SUCCESS(f'Dashboard updated at {dashboard.last_updated}'))

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data for all models!'))


    def generate_parking_sensor_data():
        # Generate a ParkingSensor for each ParkingSlot
        for slot in ParkingSlot.objects.all():
            sensor_status = random.choice(['Active', 'Inactive'])
            ParkingSensor.objects.create(
                parking_slot=slot,
                sensor_status=sensor_status,
                last_maintenance=timezone.now() - timedelta(days=random.randint(1, 365)),  # Random last maintenance within the past year
            )

    def generate_parking_subscription_data():
        # Generate a ParkingSubscription for each User
        for user in User.objects.all():
            # Get a random ParkingSlot for the user
            parking_slot = random.choice(ParkingSlot.objects.all())

            # Generate a random subscription type
            subscription_type = random.choice(['Monthly', 'Yearly'])

            # Set random start and end dates for subscription
            start_date = timezone.now()
            end_date = start_date + timedelta(days=random.randint(30, 365))  # Random duration between 1 month and 1 year

            ParkingSubscription.objects.create(
                user=user,
                parking_slot=parking_slot,
                start_date=start_date,
                end_date=end_date,
                subscription_type=subscription_type,
            )

    # Call the functions to generate data
    generate_parking_sensor_data()
    generate_parking_subscription_data()