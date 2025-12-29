from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import admin_required, teacher_required, student_required
from .forms import CreateUserForm

from config.models import AbsencePresence, Student, Seance


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'auth/login.html')




from .forms import CreateUserForm

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'dashboards/admin.html', {
        'user': request.user
    })

@login_required
@admin_required
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully")
            return redirect('admin_dashboard')
    else:
        form = CreateUserForm()

    return render(request, 'dashboards/create_user.html', {
        'form': form
    })



# @login_required
# @admin_required
# def admin_dashboard(request):
#     if request.method == 'POST':
#         form = ClassForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = ClassForm()
#     return render(request, 'dashboards/admin.html', {
#         'user': request.user,
#         'form': form,
#     })

@login_required
@teacher_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    seances = Seance.objects.filter(classmodule__teacher=teacher)

    return render(request, 'dashboards/teacher.html', {
        'user': request.user,
        'seances': seances,
    })






from config.models import AbsencePresence

@login_required
@student_required
def student_dashboard(request):
    student = request.user.student

    attendance_qs = AbsencePresence.objects.filter(student=student)

    total_sessions = attendance_qs.count()
    present_count = attendance_qs.filter(status='present').count()
    absent_count = attendance_qs.filter(status='absent').count()

    attendance_rate = round((present_count / total_sessions) * 100, 2) if total_sessions > 0 else 0

    return render(request, 'dashboards/student.html', {
        'user': request.user,
        'attendance': attendance_qs,
        'total_sessions': total_sessions,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_rate': attendance_rate,
    })










@login_required
@teacher_required
def mark_attendance(request, session_id):
    session = get_object_or_404(
        Seance,
        id=session_id,
        classmodule__teacher=request.user.teacher
    )

    students = Student.objects.filter(
        class_obj=session.classmodule.class_obj
    )

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            AbsencePresence.objects.update_or_create(
                student=student,
                session=session,
                defaults={'status': status}
            )
        return redirect('teacher_dashboard')

    return render(request, 'dashboards/mark_attendance.html', {
        'session': session,
        'students': students,
    })




