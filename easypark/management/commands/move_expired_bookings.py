from django.core.management.base import BaseCommand
from django.utils import timezone
from easypark.models import Booking

class Command(BaseCommand):
    help = "Move expired bookings to Reservation"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_bookings = Booking.objects.filter(status='active', reservation_end_time__lte=now)

        for booking in expired_bookings:
            booking.complete_booking()  # เรียกฟังก์ชันย้ายข้อมูลไป Reservation
            self.stdout.write(self.style.SUCCESS(f'Moved booking {booking.id} to Reservation'))

        if not expired_bookings.exists():
            self.stdout.write(self.style.WARNING("No expired bookings found"))
