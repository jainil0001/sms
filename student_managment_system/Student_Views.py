from django.shortcuts import render, redirect
from app.models import Student_Notification, Student, Student_Feedback, Student_leave, Subject, Attendance, Attendance_Report, StudentResult
from django.contrib import messages

def Home(request):
    return render(request, 'Student/home.html')


def student_notification(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        student_notification = Student_Notification.objects.filter(student_id = student_id)
        context = {
            'student_notification': student_notification,
        }
        return render(request, 'Student/student_notification.html', context)


def student_notification_mark_as_done(request, status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')


def student_feedback(request):
    student_id = Student.objects.get(admin = request.user.id)
    student_feedback_history = Student_Feedback.objects.filter(student_id = student_id)
    context = {
        'student_feedback_history': student_feedback_history,
    }
    return render(request, 'Student/student_feedback.html', context)

def student_feedback_save(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        student_id = Student.objects.get(admin=request.user.id)
        feedbacks = Student_Feedback(
            student_id = student_id,
            feedback = feedback,
            feedback_reply = ''
        )
        feedbacks.save()
        messages.success(request, feedback + ' has been saved')
        return redirect('student_feedback')


def student_leave(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        student_leave = Student_leave.objects.filter(student_id = student_id)
        context = {
            'student_leave': student_leave,
        }
        return render(request, 'Student/student_leave.html', context)


def student_leave_save(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        student_id = Student.objects.get(admin=request.user.id)
        student_leave = Student_leave(
            student_id = student_id,
            leave_date = leave_date,
            leave_reason = leave_message,
        )
        student_leave.save()
        messages.success(request, leave_message + ' has been saved')
        return redirect('student_leave')


def student_view_attendance(request):
    student = Student.objects.get(admin = request.user.id)
    subjects = Subject.objects.filter(course = student.course_id)
    action = request.GET.get('action')

    get_subject = None
    attendance_report = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)

            attendance_report = Attendance_Report.objects.filter(student_id = student, attendance_id__subject_id = subject_id)

    context = {
        'subjects': subjects,
        'action': action,
        'get_subject': get_subject,
        'attendance_report': attendance_report,
    }
    return render(request, 'Student/student_attendance.html', context)


def student_view_result(request):
    total_mark = None
    student = Student.objects.get(admin = request.user.id)
    result = StudentResult.objects.filter(student_id = student)
    for i in result:
        assignment_mark = i.assignment_mark
        exam_mark = i.exam_mark
        total_mark = assignment_mark + exam_mark
    context = {
        'result': result,
        'total_mark': total_mark,
    }
    return render(request, 'Student/student_result.html', context)