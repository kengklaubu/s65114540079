from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from easypark.models import Booking

def move_expired_bookings():
    now = timezone.now()
    expired_bookings = Booking.objects.filter(status='active', reservation_end_time__lte=now)

    for booking in expired_bookings:
        booking.complete_booking()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(move_expired_bookings, 'interval', minutes=1)
    scheduler.start()
