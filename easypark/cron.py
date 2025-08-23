from django_cron import CronJobBase, Schedule
from django.utils import timezone
from .models import Booking

class MoveExpiredBookingsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # ให้เช็คทุกๆ 1 นาที

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'easypark.move_expired_bookings'  # ชื่อโค้ดต้องไม่ซ้ำกันในระบบ

    def do(self):
        now = timezone.now()
        expired_bookings = Booking.objects.filter(status='active', reservation_end_time__lte=now)

        for booking in expired_bookings:
            booking.complete_booking()
