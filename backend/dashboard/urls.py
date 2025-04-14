from django.urls import path
from dashboard.views import *

from django.urls import path

urlpatterns = [
    path('admin/status/', AdminDashboardStatusView.as_view(), name='dashboard-stats'),
    path('admin/status/classroom/', AdminDashboardRoomsStats.as_view(), name='dashboard-room-stats'),
    path('admin/status/user/', AdminDashboardUserStats.as_view(), name='user-stats'),
    path('admin/seats/insert/', SeatCreateView.as_view(), name='seat-create'),
    path('admin/seats/disable/', SeatDisableView.as_view(), name='seat-disable'),
    path('admin/seats/enable/', SeatEnableView.as_view(), name='seat-enable'),
    path('admin/classroom/insert/', ClassRoomCreateView.as_view(), name='classroom-create'),
    path('admin/classroom/disable/', ClassRoomDisableView.as_view(), name='classroom-disable'),
    path('admin/classroom/enable/', ClassRoomEnableView.as_view(), name='classroom-enable'),
]