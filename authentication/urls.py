from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),

    # dashboard urls : 
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/mark_attendance/<int:session_id>/', views.mark_attendance, name='mark_attendance'),
]