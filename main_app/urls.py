"""college_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

# from main_app.EditResultView import EditResultView

from . import hod_views, staff_views, student_views, views, admin_form_views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
#     path("staff/add", hod_views.add_staff, name='add_staff'),
#     path("department/add", hod_views.add_department, name='add_department'),
    path("send_student_notification/", hod_views.send_student_notification, name='send_student_notification'),
    path("send_staff_notification/", hod_views.send_staff_notification, name='send_staff_notification'),
    path("admin_notify_student", hod_views.admin_notify_student, name='admin_notify_student'),
    path("admin_notify_staff", hod_views.admin_notify_staff, name='admin_notify_staff'),
    path("admin_view_profile", hod_views.admin_view_profile, name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability, name="check_email_availability"),
    path("student/view/feedback/", hod_views.student_feedback_message, name="student_feedback_message",),
    path("staff/view/feedback/", hod_views.staff_feedback_message, name="staff_feedback_message",),
    path("student/view/leave/", hod_views.view_student_leave, name="view_student_leave",),
    path("staff/view/leave/", hod_views.view_staff_leave, name="view_staff_leave",),
    path("attendance/view/", hod_views.admin_view_attendance, name="admin_view_attendance",),
    # path("attendance/view_multi/", hod_views.student_view_multi_attendance, name="student_view_multi_attendance",),
    path("attendance/fetch/", hod_views.get_admin_attendance, name='get_admin_attendance'),
    path('admin/get_classes_by_department/', hod_views.get_classes_by_department, name='get_classes_by_department'),
    path('fetch-students/', staff_views.fetch_students, name='fetch_students'),
#     path("student/add/", hod_views.add_student, name='add_student'),
#     path("subject/add/", hod_views.add_subject, name='add_subject'),
#     path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
#     path("student/manage/", hod_views.manage_student, name='manage_student'),
#     path("department/manage/", hod_views.manage_department, name='manage_department'),
#     path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
#     path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
#     path("staff/delete/<int:staff_id>", hod_views.delete_staff, name='delete_staff'),
#     path("department/delete/<int:department_id>", hod_views.delete_department, name='delete_department'),
#     path("subject/delete/<int:subject_id>", hod_views.delete_subject, name='delete_subject'),
    path('dep-to-class-autocomplete/', admin_form_views.DepToClass.as_view(), name='dep-to-class-autocomplete'),
    path('timetable-dep-to-class-autocomplete/', admin_form_views.TimetableDepToClass.as_view(), name='timetable-dep-to-class-autocomplete'),
    path('class-to-sub-autocomplete/', admin_form_views.ClassToSub.as_view(), name='class-to-sub-autocomplete'),

#     path("student/delete/<int:student_id>", hod_views.delete_student, name='delete_student'),
#     path("student/edit/<int:student_id>", hod_views.edit_student, name='edit_student'),
#     path("department/edit/<int:department_id>", hod_views.edit_department, name='edit_department'),
#     path("subject/edit/<int:subject_id>", hod_views.edit_subject, name='edit_subject'),
#     path("timetable/add", hod_views.add_timetable, name='add_timetable'),
     # path('class/add', hod_views.add_class, name='add_class'),
     # path('class/manage', hod_views.manage_class, name='manage_class'),
     # path('class/edit/<int:class_id>', hod_views.edit_class, name='edit_class'),
     # path('class/delete/<int:class_id>', hod_views.delete_class, name='delete_class'),
     path('download/student-template/', hod_views.download_student_template, name='download_student_template'),
     path('download/staff-template/', hod_views.download_staff_template, name='download_staff_template'),
     path('download/download-day-attendance/', hod_views.download_single_day_attendance, name='download_single_day_attendance'),



    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'),
    path("staff/apply/leave/", staff_views.staff_apply_leave, name='staff_apply_leave'),
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    path("staff/view/profile/", staff_views.staff_view_profile, name='staff_view_profile'),
    path("staff/attendance/take/", staff_views.staff_take_attendance, name='staff_take_attendance'),
    path("staff/attendance/submit_attendance/", staff_views.submit_attendance, name='submit_attendance'),
    path("staff/attendance/update/", staff_views.staff_update_attendance, name='staff_update_attendance'),
    path("staff/add_assignment/", staff_views.add_assignment, name='add_assignment'),
    path("staff/view_assignment/", staff_views.view_assignment, name='view_assignment'),
    path("staff/get_students/", staff_views.get_students, name='get_students'),
    path("staff/attendance/fetch/", staff_views.get_student_attendance, name='get_student_attendance'),
    path("staff/attendance/save/", staff_views.save_attendance, name='save_attendance'),
    path("staff/attendance/update/", staff_views.update_attendance, name='update_attendance'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification, name="staff_view_notification"),
    path("staff/result/add/", staff_views.staff_add_result, name='staff_add_result'),
    path('staff/result/fetch/', staff_views.fetch_student_result, name='fetch_student_result'),
    path('staff/timetable/', staff_views.staff_timetable_view, name='staff_timetable_view'),

#     path("staff/result/edit/", EditResultView.as_view(), name='edit_student_result'),


    # Student
    path("student/home/", student_views.student_home, name='student_home'),
    path("student/view/attendance/", student_views.student_view_attendance, name='student_view_attendance'),
    path("student/apply/leave/", student_views.student_apply_leave, name='student_apply_leave'),
    path("student/feedback/", student_views.student_feedback, name='student_feedback'),
    path("student/view/profile/", student_views.student_view_profile, name='student_view_profile'),
    path("student/fcmtoken/", student_views.student_fcmtoken, name='student_fcmtoken'),
    path("student/view/notification/", student_views.student_view_notification, name="student_view_notification"),
    path('student/view/result/', student_views.student_view_result, name='student_view_result'),
    path('student/view/assignment/', student_views.student_view_assignment, name='student_view_assignment'),
    path('student/view/timetable/', student_views.student_view_timetable, name='student_view_timetable'),

]
