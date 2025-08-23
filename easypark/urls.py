from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('sc-parking/', views.sc_parking, name='sc_parking_default'),  # รองรับการเข้าถึงโดยไม่ระบุ location_id
    path('sc-parking/<int:location_id>/', views.sc_parking, name='sc_parking'),  # ระบุ location_id
    path('api/get_parking_status', views.get_parking_status, name='get_parking_status'),
    path('api/get_spot_details', views.get_spot_details, name='get_spot_details'),
    path('reserve_page/<int:spot_number>/', login_required(views.reserve_page), name='reserve_page'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('login/',(views.login_page), name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('profile/', login_required(views.profile), name='profile'),
    path('accounts/login/', LoginView.as_view(template_name='easypark/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('success_page/', views.success_page, name='success_page'),
    path('login/', views.login_page, name='login_page'),  
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  
    path('manager_dashboard/<int:location_id>/', views.manager_dashboard, name='manager_dashboard'),
    path('manager_add_location/', views.manager_add_location, name='manager_add_location'),
    path('manager_dashboard/<int:location_id>/add_spot/', views.add_parking_spot, name='add_parking_spot'),
    path('manager/reservation/cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('manager/locations/', views.manager_location_selection, name='manager_location_selection'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('get_parking_spots/<int:location_id>/', views.get_parking_spots, name='get_parking_spots'),
    path('suspend_parking_spot/<int:spot_id>/', views.suspend_parking_spot, name='suspend_parking_spot'),
    path('start_detection/', views.start_detection, name='start_detection'),
    path('live/<int:location_id>/',views.stream_video, name='live_video'),
    path('stream/<int:location_id>/',views.video_feed, name='video_feed'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path("update_parking_spot_position/", views.update_parking_spot_position, name="update_parking_spot_position"),
    path('delete_parking_spot/<int:spot_id>/', views.delete_parking_spot, name='delete_parking_spot'),
    path('user_management/', views.user_management, name='user_management'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path("delete_user/<int:user_id>/", views.delete_user, name="delete_user"),
    path("add_user/", views.add_user, name="add_user"),
    path("locations_management/", views.locations_management, name="locations_management"),
    path('dashboard/locations/edit/<int:location_id>/', views.admin_edit_location, name='admin_edit_location'),
    path('locations/add/', views.admin_add_location, name='admin_add_location'),
    path('locations/delete/<int:location_id>/', views.delete_location, name='delete_location'),  # ✅ ต้องมีเส้นทางนี้
    path('locations/get/<int:location_id>/', views.get_location, name='get_location'),
    path("update_roi_position/", views.update_roi_position, name="update_roi_position"),
    path('capture_frame/<int:location_id>/', views.capture_frame, name='capture_frame'),
    path('update_parking_image/<int:location_id>/', views.update_parking_image, name='update_parking_image'),
   
    path('password_reset/', views.password_reset, name='password_reset1221'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('locations/<slug:location_slug>/', views.parking_location, name='parking-location'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
