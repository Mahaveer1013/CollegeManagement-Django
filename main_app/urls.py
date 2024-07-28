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
    # path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("admin/exam/filter", hod_views.exam_filter_page, name='exam_filter_page'),
    path("send_student_notification/", hod_views.send_student_notification,
         name='send_student_notification'),
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("admin_notify_student", hod_views.admin_notify_student,
         name='admin_notify_student'),
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("student/view/feedback/", hod_views.student_feedback_message,
         name="student_feedback_message",),
    path("staff/view/feedback/", hod_views.staff_feedback_message,
         name="staff_feedback_message",),
    path("student/view/leave/", hod_views.view_student_leave,
         name="view_student_leave",),
    path("staff/view/leave/", hod_views.view_staff_leave, name="view_staff_leave",),
    path("hod_staff_timetable", hod_views.hod_staff_timetable, name="hod_staff_timetable",),
    path("hod_class_timetable", hod_views.hod_class_timetable, name="hod_class_timetable",),
    path("timetable/overall/", hod_views.overall_timetable, name="overall_timetable",),
    path("attendance/view/", hod_views.admin_view_attendance,
         name="admin_view_attendance"),
    path('admin/get_classes_by_department/',
         hod_views.get_classes_by_department, name='get_classes_by_department'),
    path('fetch-students/', staff_views.fetch_students, name='fetch_students'),
    path('dep-to-class-autocomplete/', admin_form_views.DepToClass.as_view(),
         name='dep-to-class-autocomplete'),
    path('timetable-dep-to-class-autocomplete/', admin_form_views.TimetableDepToClass.as_view(),
         name='timetable-dep-to-class-autocomplete'),
    path('class-to-sub-autocomplete/', admin_form_views.ClassToSub.as_view(),
         name='class-to-sub-autocomplete'),
    path("attendance/view-overall/", hod_views.admin_view_overall_attendance,
         name="admin_view_overall_attendance",),

    path('download/student-template/', hod_views.download_student_template,
         name='download_student_template'),
    path('download/staff-template/', hod_views.download_staff_template,
         name='download_staff_template'),
    path('download/download-day-attendance/',
         hod_views.download_single_day_attendance, name='download_single_day_attendance'),
    path('download/download-overall-attendance/',
         hod_views.download_overall_day_attendance, name='download_overall_day_attendance'),
    path('get_classes_by_department/', views.get_classes_by_department, name='get_classes_by_department'),
    path('get_students_by_class/', views.get_students_by_class, name='get_students_by_class'),



    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'),
#     path("notice/view", staff_views.view_notice, name='view_notice'),
     path("staff/profile/", staff_views.staff_profile, name='staff_profile'),
    path("staff/apply/leave/", staff_views.staff_apply_leave,
         name='staff_apply_leave'),
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
    path("staff/attendance/take/", staff_views.staff_take_attendance,
         name='staff_take_attendance'),
    path("staff/attendance/submit_attendance/",
         staff_views.submit_attendance, name='submit_attendance'),
#     path("staff/attendance/update/", staff_views.staff_update_attendance,
#          name='staff_update_attendance'),
    path("staff/notes/", staff_views.staff_view_note, name='staff_view_note'),
    path("staff/add_assignment/", staff_views.add_assignment, name='add_assignment'),
    path("staff/view_assignment/",
         staff_views.view_assignment, name='view_assignment'),
     path("staff/notice/", staff_views.staff_view_notice, name='staff_view_notice'),
#     path("staff/get_students/", staff_views.get_students, name='get_students'),
#     path("staff/attendance/fetch/", staff_views.get_student_attendance,
#          name='get_student_attendance'),
#     path("staff/attendance/save/",
#          staff_views.save_attendance, name='save_attendance'),
#     path("staff/attendance/update/",
#          staff_views.update_attendance, name='update_attendance'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification,
         name="staff_view_notification"),
    path("staff/result/add/", staff_views.staff_add_result, name='staff_add_result'),
    path('staff/result/fetch/', staff_views.fetch_student_result,
         name='fetch_student_result'),
    path('staff/timetable/', staff_views.staff_view_timetable,
         name='staff_view_timetable'),



    # Student
    path("student/home/", student_views.student_home, name='student_home'),
    path("student/notes/", student_views.student_view_note, name='student_view_note'),
    path("student/profile/", student_views.student_profile, name='student_profile'),
    path("student/notice/", student_views.student_view_notice, name='student_view_notice'),
    path("student/view/attendance/", student_views.student_view_attendance,
         name='student_view_attendance'),
    path("student/apply/leave/", student_views.student_apply_leave,
         name='student_apply_leave'),
    path("student/feedback/", student_views.student_feedback,
         name='student_feedback'),
    path("student/view/profile/", student_views.student_view_profile,
         name='student_view_profile'),
    path("student/fcmtoken/", student_views.student_fcmtoken,
         name='student_fcmtoken'),
    path("student/view/notification/", student_views.student_view_notification,
         name="student_view_notification"),
    path('student/view/result/', student_views.student_view_result,
         name='student_view_result'),
    path('student/view/assignment/', student_views.student_view_assignment,
         name='student_view_assignment'),
    path('student/view/timetable/', student_views.student_view_timetable,
         name='student_view_timetable'),

]
