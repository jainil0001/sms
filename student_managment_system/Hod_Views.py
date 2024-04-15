from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Course, Session, CustomUser, Student, Staff, Subject, Staff_Notification, Staff_leave,Staff_Feedback, Student_Notification, Student_Feedback, Student_leave, Attendance, Attendance_Report
from django.contrib import messages


@login_required(login_url='/')
def home(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()

    context = {
        'student_count': student_count,
        'staff_count': staff_count,
        'course_count': course_count,
        'subject_count': subject_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
    }

    return render(request, 'Hod/home.html', context)

@login_required(login_url='/')
def add_student(request):
    course = Course.objects.all()
    session = Session.objects.all()
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        address = request.POST.get('address')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)
            session_year = Session.objects.get(id=session_id)

            student = Student(
                admin = user,
                address = address,
                session_id = session_year,
                course_id = course,
                gender = gender
            )

            student.save()
            messages.success(request, user.first_name + ' ' + user.last_name + ' has been added')
            return redirect('add_student')

    context = {
        'course': course,
        'session': session
    }
    return render(request, 'Hod/add_student.html', context)

@login_required(login_url='/')
def view_student(request):
    student = Student.objects.all()
    context = {
        'student': student
    }
    return render(request, 'Hod/view_student.html', context)

@login_required(login_url='/')
def edit_student(request,id):
    student = Student.objects.get(id=id)
    course = Course.objects.all()
    session = Session.objects.all()

    context = {
        'student': student,
        'course': course,
        'session': session
    }

    return render(request, 'Hod/edit_students.html', context)

@login_required(login_url='/')
def update_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        address = request.POST.get('address')

        user = CustomUser.objects.get(id=student_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password is not None and password != '':
            user.set_password(password)
        if profile_pic is not None and profile_pic != '':
            user.profile_pic = profile_pic

        user.save()

        student = Student.objects.get(admin=student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id=course_id)
        student.course_id = course

        session = Session.objects.get(id=session_id)
        student.session_id = session

        student.save()
        messages.success(request, user.first_name + ' ' + user.last_name + ' has been updated')

        return redirect('view_student')

    return render(request, 'Hod/edit_students.html')

@login_required(login_url='/')
def delete_student(request, id):
    student = CustomUser.objects.get(id=id)
    student.delete()
    messages.success(request, student.first_name + ' ' + student.last_name + ' has been deleted')
    return redirect('view_student')

@login_required(login_url='/')
def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')

        course = Course(
            name=course_name,
        )

        course.save()
        messages.success(request, course_name + ' has been added')
        return redirect('add_course')
    return render(request, 'Hod/add_course.html')

@login_required(login_url='/')
def view_course(request):
    course = Course.objects.all()
    context = {
        'course': course,
    }
    return render(request, 'Hod/view_course.html', context)

@login_required(login_url='/')
def edit_course(request, id):
    course = Course.objects.get(id=id)

    context = {
        'course': course,
    }
    return render(request, 'Hod/edit_course.html', context)

@login_required(login_url='/')
def update_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('name')

        course = Course.objects.get(id=course_id)
        course.name = course_name
        course.save()
        messages.success(request, course_name + ' has been updated')
        return redirect('view_course')
    return render(request, 'Hod/edit_course.html')

@login_required(login_url='/')
def delete_course(request,id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request, course.name + ' has been deleted')

    return redirect('view_course')

@login_required(login_url='/')
def add_staff(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists')
            return redirect('add_staff')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                profile_pic=profile_pic,
                user_type=2,
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin = user,
                address = address,
                gender = gender
            )

            staff.save()
            messages.success(request, user.first_name + ' ' + user.last_name + ' has been added')
            return redirect('add_staff')
    return render(request, 'Hod/add_staff.html')

@login_required(login_url='/')
def view_staff(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff
    }
    return render(request, 'Hod/view_staff.html',context)

@login_required(login_url='/')
def edit_staff(request, id):
    staff = Staff.objects.get(id=id)
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/edit_staff.html', context)

@login_required(login_url='/')
def update_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password is not None and password != '':
            user.set_password(password)
        if profile_pic is not None and profile_pic != '':
            user.profile_pic = profile_pic

        user.save()

        staff = Staff.objects.get(admin=staff_id)
        staff.address = address
        staff.gender = gender
        staff.save()

        messages.success(request, user.first_name + ' ' + user.last_name + ' has been updated')
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')

@login_required(login_url='/')
def delete_staff(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, staff.first_name + ' ' + staff.last_name + ' has been deleted')
    return redirect('view_staff')

@login_required(login_url='/')
def add_subject(request):
    course = Course.objects.all()
    staff = Staff.objects.all()
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        subject_id = request.POST.get('subject_id')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)
        subject = Subject(
            name=subject_name,
            subject_id=subject_id,
            course=course,
            staff=staff,
        )

        subject.save()
        messages.success(request, subject_name + ' has been added')
        return redirect('add_subject')

    context = {'course': course, 'staff': staff}
    return render(request, 'Hod/add_subject.html', context)

@login_required(login_url='/')
def view_subject(request):
    subject = Subject.objects.all()
    context = {
        'subject': subject,
    }
    return render(request, 'Hod/view_subject.html', context)

@login_required(login_url='/')
def edit_subject(request, id):
    subject = Subject.objects.get(id=id)
    course = Course.objects.all()
    staff = Staff.objects.all()

    context = {
        'subject': subject,
        'course': course,
        'staff': staff,
    }

    return render(request, 'Hod/edit_subject.html', context)

@login_required(login_url='/')
def update_subject(request):
    if request.method == 'POST':
        subjectId = request.POST.get('subjectId')
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject (
            id = subjectId,
            subject_id = subject_id,
            name = subject_name,
            course = course,
            staff = staff,
        )

        subject.save()
        messages.success(request, subject_name + ' has been updated')
        return redirect('view_subject')
    return render(request, 'Hod/edit_subject.html')

@login_required(login_url='/')
def delete_subject(request, id):
    subject = Subject.objects.get(id=id)
    subject.delete()
    messages.success(request, subject.name + ' has been deleted')
    return redirect('view_subject')

@login_required(login_url='/')
def add_session(request):
    if request.method == 'POST':
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session(
            session_start = session_year_start,
            session_end = session_year_end,
        )

        session.save()
        messages.success(request, session_year_start + ' to ' + session_year_end + ' has been added')
        return redirect('add_session')
    return render(request, 'Hod/add_session.html')

@login_required(login_url='/')
def view_session(request):
    session = Session.objects.all()
    context = {
        'session': session
    }
    return render(request, 'Hod/view_session.html', context)

@login_required(login_url='/')
def edit_session(request, id):
    session = Session.objects.filter(id=id)
    context = {
        'session': session,
    }
    return render(request, 'Hod/edit_session.html', context)

@login_required(login_url='/')
def update_session(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session (
            id = session_id,
            session_start = session_year_start,
            session_end = session_year_end,
        )

        session.save()
        messages.success(request, session_year_start + ' to ' + session_year_end + ' has been updated')

        return redirect('view_session')

@login_required(login_url='/')
def delete_session(request,id):
    session = Session.objects.get(id=id)
    session.delete()
    messages.success(request, session.session_start + ' to ' + session.session_end + ' has been deleted')
    return redirect('view_session')

@login_required(login_url='/')
def staff_send_notification(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'staff': staff,
        'see_notification': see_notification
    }
    return render(request, 'Hod/staff_send_notification.html', context)

@login_required(login_url='/')
def staff_save_notification(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin=staff_id)

        notification = Staff_Notification(
            staff_id = staff,
            message = message
        )

        notification.save()
        messages.success(request, message + ' has been sent successfully')
        return redirect('staff_send_notification')

@login_required(login_url='/')
def staff_leave_view(request):
    staff_leave = Staff_leave.objects.all()
    context = {
        'staff_leave': staff_leave
    }
    return render(request, 'Hod/staff_leave_view.html', context)

@login_required(login_url='/')
def staff_approve_leave(request, id):
    leave = Staff_leave.objects.get(id = id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='/')
def staff_disapprove_leave(request, id):
    leave = Staff_leave.objects.get(id = id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='/')
def staff_feedback_reply(request):
    feedback = Staff_Feedback.objects.all()
    feedback_reply_history = Staff_Feedback.objects.all().order_by('-id')[0:5]
    context = {
        'feedback': feedback,
        'feedback_reply_history': feedback_reply_history
    }
    return render(request, 'Hod/staff_feedback.html', context)

@login_required(login_url='/')
def staff_feedback_save_reply(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        messages.success(request, feedback_reply + ' has been saved')
        return redirect('staff_feedback_reply')


def STUDENT_SEND_NOTIFICATION(request):
    student = Student.objects.all()
    see_notification = Student_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'student': student,
        'see_notification': see_notification
    }
    return render(request, 'Hod/student_send_notification.html', context)


def STUDENT_SAVE_NOTIFICATION(request):
    if request.method == 'POST':
        student_id = request.POST.get('Student_id')
        message = request.POST.get('message')

        student = Student.objects.get(admin=student_id)

        stud_notification = Student_Notification(
            student_id = student,
            message = message
        )

        stud_notification.save()
        messages.success(request, message + ' has been sent successfully')
        return redirect('student_send_notification')


def student_feedback(request):
    feedback = Student_Feedback.objects.all()
    feedback_history = Student_Feedback.objects.all().order_by('-id')[0:5]
    context = {
        'feedback': feedback,
        'feedback_history': feedback_history
    }
    return render(request, 'Hod/student_feedback.html', context)


def student_feedback_reply(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Student_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        messages.success(request, feedback_reply + ' has been saved')
        return redirect('get_student_feedback')


def student_leave_view(request):
    student_leave = Student_leave.objects.all()
    context = {
        'student_leave': student_leave
    }
    return render(request, 'Hod/student_leave_view.html', context)


def student_approve_leave(request, id):
    leave = Student_leave.objects.get(id=id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_disapprove_leave(request, id):
    leave = Student_leave.objects.get(id=id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def hod_view_attendance(request):
    subject = Subject.objects.all()
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
    return render(request, 'Hod/hod_view_attendance.html', context)