from time import timezone
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ParkingSpot, Reservation, ParkingLocation,Booking

@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('spot_number', 'is_available', 'reserved_by','location')
    list_editable = ('is_available','location')
    search_fields = ('spot_number','location')
    list_filter = ('is_available', 'location')
    actions = ['mark_as_available', 'mark_as_unavailable']

    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)
    mark_as_available.short_description = "เปลี่ยนสถานะเป็นว่าง"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    mark_as_unavailable.short_description = "เปลี่ยนสถานะเป็นไม่ว่าง"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'parking_spot', 'location', 'reservation_date', 'reservation_start_time', 'reservation_end_time', 'status')
    search_fields = ('user__username', 'parking_spot__spot_number', 'location__name')
    list_filter = ('status', 'reservation_date', 'created_at')
    actions = ['mark_completed', 'mark_cancelled']

    def mark_completed(self, request, queryset):
        """ ทำเครื่องหมายว่าการจองเสร็จสิ้นและย้ายไปที่ Reservation """
        for booking in queryset.filter(status='active'):
            booking.complete_booking()
        self.message_user(request, "Marked selected bookings as completed.")

    mark_completed.short_description = "Mark selected bookings as completed"

    def mark_cancelled(self, request, queryset):
        """ ทำเครื่องหมายว่าการจองถูกยกเลิก """
        queryset.filter(status='active').update(status='cancelled', cancelled_at=timezone.now())
        self.message_user(request, "Marked selected bookings as cancelled.")

    mark_cancelled.short_description = "Mark selected bookings as cancelled"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'parking_spot', 'location', 'reservation_date', 'completed_at', 'reservation_start_time', 'reservation_end_time')
    search_fields = ('user__username', 'parking_spot__spot_number', 'location__name', 'reservation_date')
    list_filter = ('reservation_date', 'completed_at')
    


@admin.register(ParkingLocation)
class ParkingLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'total_spots', 'available_spots']
    search_fields = ['name']
    list_filter = ['total_spots', 'available_spots']


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from .models import ROI

@admin.register(ROI)
class ROIAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "parking_spot", "x_position", "y_position", "width", "height", "updated_at")
    search_fields = ("name",)
    fieldsets = (
        (None, {
            'fields': ("name", "location", "parking_spot", "x_position", "y_position", "width", "height")
        }),
    )





