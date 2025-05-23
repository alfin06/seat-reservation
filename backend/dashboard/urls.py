from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('admin/status/', AdminDashboardStatusView.as_view(), name='dashboard-stats'),
    path('admin/status/classroom/', AdminDashboardRoomsStats.as_view(), name='dashboard-room-stats'),
    path('admin/status/user/', AdminDashboardUserStats.as_view(), name='user-stats'),
    path('admin/seats/list/', SeatGetAll.as_view(), name='seat-get_all'),
    path('admin/seats/disable/', SeatDisableView.as_view(), name='seat-disable'),
    path('admin/seats/enable/', SeatEnableView.as_view(), name='seat-enable'),
    path('admin/seats/update/', SeatUpdateView.as_view(), name='seat-update'),
    path('admin/classroom/list/', ClassRoomGetAll.as_view(), name='classroom-get-all'),
    path('admin/classroom/insert/', ClassRoomCreateView.as_view(), name='classroom-create'),
    path('admin/classroom/disable/', ClassRoomDisableView.as_view(), name='classroom-disable'),
    path('admin/classroom/enable/', ClassRoomEnableView.as_view(), name='classroom-enable'),
    path('admin/setting-update/', ReservationSettingUpdateView.as_view(), name='update-setting'),
    path('admin/setting/', ReservationSettingView.as_view(), name='setting'),
    path('admin/classroom/update/', UpdateClassroomView.as_view(), name='update_classroom'),

    # API endpoints
    path('api/reservations/', ReservationCreateView.as_view(), name='reservation-create'),
    path('api/available/', AvailableRoomsSeatsView.as_view(), name='available-rooms-seats'),
    path('api/allseats/', AllRoomsSeatsView.as_view(), name='all-rooms-seats'),
    path('api/check-qr/', QRCodeCheckView.as_view(), name='check-qr'),
    path('api/qr-check/', QRCodeCheckView2.as_view(), name='qr-check'),
    path('api/instant-booking/', InstantBookingView.as_view(), name='instant-booking'),
    path('api/reservations/stats/', UserReservationStatsView.as_view(), name='reservation-stats'),
    path('api/reservations/active/', ActiveReservationsView.as_view(), name='active-reservations'),
    path('api/reservations/<int:reservation_id>/cancel/', CancelReservationView.as_view(), name='cancel_reservation'),
    path('api/reservations/history/', ReservationHistoryView.as_view(), name='reservation-history'),
]
