from django.shortcuts import render, redirect
from app.models import Staff, Staff_Notification, Staff_leave, Staff_Feedback, Subject, Session, Student, Attendance, Attendance_Report, StudentResult
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def home(request):
    return render(request, "Staff/home.html")


@login_required(login_url='/')
def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        staff_notification = Staff_Notification.objects.filter(staff_id=staff_id)
        context = {
            "staff_notification": staff_notification,
        }
        return render(request, "Staff/notifications.html", context)


@login_required(login_url='/')
def mark_as_done(request, status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect("notifications")


@login_required(login_url='/')
def staff_apply_leave(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_leave.objects.filter(staff_id=staff_id)
        context = {
            "staff_leave_history": staff_leave_history,
        }
        return render(request, "Staff/apply_leave.html", context)


@login_required(login_url='/')
def staff_apply_leave_save(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff = Staff.objects.get(admin=request.user.id)

        leave = Staff_leave(
            staff_id=staff,
            leave_date=leave_date,
            leave_reason=leave_message,
        )

        leave.save()
        messages.success(request, "Leave applied successfully")
        return redirect("staff_apply_leave")


@login_required(login_url='/')
def staff_feedback(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    staff_feedback_history = Staff_Feedback.objects.filter(staff_id=staff_id)
    context = {
        "staff_feedback_history": staff_feedback_history,
    }
    return render(request, "Staff/feedback.html", context)


@login_required(login_url='/')
def staff_feedback_save(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        staff = Staff.objects.get(admin=request.user.id)
        feedback = Staff_Feedback(
            staff_id=Staff.objects.get(admin=request.user.id),
            feedback=feedback,
            feedback_reply="",
        )
        feedback.save()
        messages.success(request, "Feedback saved successfully")
        return redirect("staff_feedback")


def staff_take_attendance(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff=staff_id)
    session = Session.objects.all()
    action = request.GET.get('action')

    get_session_year = None
    get_subject = None
    students = None
    if action is not None:
        if request.method == 'POST':
            session_year_id = request.POST.get('session_year_id')
            get_session_year = Session.objects.get(id=session_year_id)
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)

            subject = Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)

    context = {
        "subject": subject,
        "session": session,
        "action": action,
        "get_session_year": get_session_year,
        "get_subject": get_subject,
        "students": students,
    }
    return render(request, "Staff/take_attendance.html", context)


def staff_take_attendance_save(request):
    if request.method == 'POST':
        session_year_id = request.POST.get('session_year_id')
        subject_id = request.POST.get('subject_id')
        present_students_id = request.POST.getlist('present_students_id')
        attendance_date = request.POST.get('attendance_date')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session.objects.get(id=session_year_id)

        attendance = Attendance(
            session_year_id=get_session_year,
            subject_id=get_subject,
            attendance_date=attendance_date,
        )
        attendance.save()
        for i in present_students_id:
            stud_id = i
            int_stud = int(stud_id)

            p_students = Student.objects.get(id=int_stud)
            attendance_report = Attendance_Report(
                attendance_id=attendance,
                student_id=p_students,
            )
            attendance_report.save()
            messages.success(request, "Attendance saved successfully")
    return redirect("staff_take_attendance")


def staff_view_attendance(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff_id=staff_id)
    session = Session.objects.all()
    action = request.GET.get('action')

    get_session_year = None
    get_subject = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == 'POST':
            session_year_id = request.POST.get('session_year_id')
            get_session_year = Session.objects.get(id=session_year_id)
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)
            attendance_date = request.POST.get('attendance_date')

            attendance = Attendance.objects.filter(session_year_id=get_session_year, attendance_date=attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)

    context = {
        "subject": subject,
        "session": session,
        "action": action,
        "get_session_year": get_session_year,
        "get_subject": get_subject,
        "attendance_date": attendance_date,
        "attendance_report": attendance_report,
    }
    return render(request, "Staff/view_attendance.html", context)


def staff_add_result(request):
    staff = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff_id=staff)
    session_year = Session.objects.all()
    action = request.GET.get('action')

    get_session = None
    get_subject = None
    students = None
    if action is not None:
        if request.method == 'POST':
            session_year_id = request.POST.get('session_year_id')
            get_session = Session.objects.get(id=session_year_id)
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)

            subjects = Subject.objects.filter(id=subject_id)
            for i in subjects:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)

    context = {
        "subjects": subjects,
        "session_year": session_year,
        "action": action,
        "get_session": get_session,
        "get_subject": get_subject,
        "students": students,
    }
    return render(request, "Staff/add_result.html", context)


def staff_add_result_save(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        Exam_mark = request.POST.get('Exam_mark')

        get_student = Student.objects.get(admin=student_id)
        get_subject = Subject.objects.get(id=subject_id)

        check_exist = StudentResult.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=get_subject, student_id=get_student)
            result.assignment_mark = assignment_mark
            result.exam_mark = Exam_mark
            result.save()
            messages.success(request, "Successfully Updated Result")
            return redirect('staff_add_result')
        else:
            result = StudentResult(student_id=get_student, subject_id=get_subject, exam_mark=Exam_mark,
                                   assignment_mark=assignment_mark)
            result.save()
            messages.success(request, "Successfully Added Result")
            return redirect('staff_add_result')
