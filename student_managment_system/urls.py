from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views, Hod_Views, Staff_Views, Student_Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),

    # LOGIN
    path('', views.LOGIN, name='login'),
    path('dbLogin', views.dbLogin, name='dbLogin'),
    path('dologout', views.dologout, name='logout'),

    # profile Update
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),

    # This is hod panel
    path('Hod/home', Hod_Views.home, name='hod_home'),
    path('Hod/Student/Add', Hod_Views.add_student, name='add_student'),
    path('Hod/Student/View', Hod_Views.view_student, name='view_student'),
    path('Hod/Student/Edit/<str:id>', Hod_Views.edit_student, name='edit_student'),
    path('Hod/Student/Update', Hod_Views.update_student, name='update_student'),
    path('Hod/Student/Delete/<str:id>', Hod_Views.delete_student, name='delete_student'),

   #  Staff
    path('Hod/Staff/Add', Hod_Views.add_staff, name='add_staff'),
    path('Hod/Staff/View', Hod_Views.view_staff, name='view_staff'),
    path('Hod/Staff/Edit/<str:id>', Hod_Views.edit_staff, name='edit_staff'),
    path('Hod/Staff/Update', Hod_Views.update_staff, name='update_staff'),
    path('Hod/Staff/Delete/<str:admin>', Hod_Views.delete_staff, name='delete_staff'),

   # Course
    path('Hod/Course/Add', Hod_Views.add_course, name='add_course'),
    path('Hod/Course/View', Hod_Views.view_course, name='view_course'),
    path('Hod/Course/Edit/<str:id>', Hod_Views.edit_course, name='edit_course'),
    path('Hod/Course/Update', Hod_Views.update_course, name='update_course'),
    path('Hod/Course/Delete/<str:id>', Hod_Views.delete_course, name='delete_course'),

    # Subject
    path('Hod/Subject/Add', Hod_Views.add_subject, name='add_subject'),
    path('Hod/Subject/View', Hod_Views.view_subject, name='view_subject'),
    path('Hod/Subject/Edit/<str:id>', Hod_Views.edit_subject, name='edit_subject'),
    path('Hod/Subject/Update', Hod_Views.update_subject, name='update_subject'),
    path('Hod/Subject/Delete/<str:id>', Hod_Views.delete_subject, name='delete_subject'),

   # Session
    path('Hod/Session/Add', Hod_Views.add_session, name='add_session'),
    path('Hod/Session/View', Hod_Views.view_session, name='view_session'),
    path('Hod/Session/Edit/<str:id>', Hod_Views.edit_session, name='edit_session'),
    path('Hod/Session/Update', Hod_Views.update_session, name='update_session'),
    path('Hod/Session/Delete/<str:id>', Hod_Views.delete_session, name='delete_session'),

  # Notifications
    path('Hod/Staff/Staff_Notification', Hod_Views.staff_send_notification, name='staff_send_notification'),
    path('Hod/Student/Save_Notification', Hod_Views.staff_save_notification, name='staff_save_notification'),

   # hod staff leave view
    path('Hod/Staff/Leave_view', Hod_Views.staff_leave_view, name='staff_leave_view'),
    path('Hod/Staff/approve_leave/<str:id>', Hod_Views.staff_approve_leave, name='staff_approve_leave'),
    path('Hod/Staff/disapprove_leave/<str:id>', Hod_Views.staff_disapprove_leave, name='staff_disapprove_leave'),

   # hod student leave view
    path('Hod/Student/Leave_view', Hod_Views.student_leave_view, name='student_leave_view'),
    path('Hod/Student/approve_leave/<str:id>', Hod_Views.student_approve_leave, name='student_approve_leave'),
    path('Hod/Student/disapprove_leave/<str:id>', Hod_Views.student_disapprove_leave, name='student_disapprove_leave'),

   # hod staff feedback
    path('Hod/Staff/Feedback', Hod_Views.staff_feedback_reply, name='staff_feedback_reply'),
    path('Hod/Staff/Feedback/save', Hod_Views.staff_feedback_save_reply, name='staff_feedback_save_reply'),

   # Staff
    path('Staff/Home', Staff_Views.home, name='staff_home'),

   # Staff leave
    path('Staff/apply_leave', Staff_Views.staff_apply_leave, name='staff_apply_leave'),
    path('Staff/Apply_leave_save', Staff_Views.staff_apply_leave_save, name='staff_apply_leave_save'),


    # Staff Notification
    path('Staff/Notifications', Staff_Views.NOTIFICATIONS, name='notifications'),
    path('Staff/mark_as_done/<str:status>', Staff_Views.mark_as_done, name='mark_as_done'),

   # Staff Feedback
    path('Staff/Feedback', Staff_Views.staff_feedback, name='staff_feedback'),
    path('Staff/Feedback_save', Staff_Views.staff_feedback_save, name='staff_feedback_save'),

  # Student
    path('Student/Home', Student_Views.Home, name='student_home'),
    path('Student/Student_Notification', Student_Views.student_notification, name='student_notification'),
    path('Student/mark_as_done/<str:status>', Student_Views.student_notification_mark_as_done, name='student_notification_mark_as_done'),

 # Hod student send notification
    path('Hod/Student/student_send_Notification', Hod_Views.STUDENT_SEND_NOTIFICATION, name='student_send_notification'),
    path('Hod/Student/student_save_Notification', Hod_Views.STUDENT_SAVE_NOTIFICATION, name='save_student_notification'),

# Student feedback
    path('Student/Feedback', Student_Views.student_feedback, name='student_feedback'),
    path('Student/Feedback_save', Student_Views.student_feedback_save, name='student_feedback_save'),

# Hod student feedback
    path('Hod/Student/Feedback', Hod_Views.student_feedback, name='get_student_feedback'),
    path('Hod/Student/Feedback_reply', Hod_Views.student_feedback_reply, name='student_feedback_reply'),

# Student leave
    path('Student/apply_for_leave', Student_Views.student_leave, name='student_leave'),
    path('Student/apply_for_leave_save', Student_Views.student_leave_save, name='student_leave_save'),

# Staff take attendance
    path('Staff/take_attendance', Staff_Views.staff_take_attendance, name='staff_take_attendance'),
    path('Staff/take_attendance_save', Staff_Views.staff_take_attendance_save, name='staff_take_attendance_save'),

# Staff view attendance
    path('Staff/view_attendance', Staff_Views.staff_view_attendance, name='staff_view_attendance'),

# Student view attendance
    path('Student/view_attendance', Student_Views.student_view_attendance, name='student_view_attendance'),

# Hod view attendance
    path('Hod/View/Attendance', Hod_Views.hod_view_attendance, name='hod_view_attendance'),

# Staff Add Result
    path('Staff/Add/Result', Staff_Views.staff_add_result, name='staff_add_result'),
    path('Staff/Save/Result', Staff_Views.staff_add_result_save, name='staff_add_result_save'),

# Student View Result
    path('Student/View/Result', Student_Views.student_view_result, name='student_view_result'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
