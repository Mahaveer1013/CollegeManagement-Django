from openpyxl.styles import PatternFill
import openpyxl
from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
import csv
from django.views.decorators.http import require_GET
from .forms import *
from .models import *
import datetime
from django.utils import timezone


def admin_home(request):
    total_staff = Staff.objects.all().count()
    total_students = Student.objects.all().count()
    subjects = Subject.objects.all()
    total_subject = subjects.count()
    total_department = Department.objects.all().count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name[:7])
        attendance_list.append(attendance_count)

    # Total Subjects and students in Each Department
    department_all = Department.objects.all()
    department_name_list = []
    # subject_count_list = []
    student_count_list_in_department = []

    for department in department_all:
        # subjects = Subject.objects.filter(department_id=department.id).count()
        students = Student.objects.filter(department_id=department.id).count()
        department_name_list.append(department.name)
        # subject_count_list.append(subjects)
        student_count_list_in_department.append(students)

    subject_all = Subject.objects.all()
    subject_list = []
    student_count_list_in_subject = Subject.objects.count()
    for subject in subject_all:
        subject_list.append(subject.name)

    # For Students
    student_attendance_present_list = []
    student_attendance_leave_list = []
    student_name_list = []

    students = Student.objects.all()
    for student in students:

        attendance = AttendanceReport.objects.filter(
            student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(
            student_id=student.id, status=False).count()
        leave = LeaveReportStudent.objects.filter(
            student_id=student.id, status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leave+absent)
        student_name_list.append(student.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_students': total_students,
        'total_staff': total_staff,
        'total_department': total_department,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'student_attendance_present_list': student_attendance_present_list,
        'student_attendance_leave_list': student_attendance_leave_list,
        "student_name_list": student_name_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "student_count_list_in_department": student_count_list_in_department,
        "department_name_list": department_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)


def get_classes_by_department(request):
    department_id = request.GET.get('department_id')
    classes = ClassList.objects.filter(
        department_id=department_id).values('id', 'semester', 'section')
    return JsonResponse(list(classes), safe=False)


def admin_view_attendance(request):
    user = get_object_or_404(Admin, admin=request.user)
    form = AttendanceSelectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            date = form.cleaned_data.get('date')
            class_id = form.cleaned_data.get('class_name')
            students_id = Student.objects.filter(class_name=class_id)
            attendance_array = []
            if len(students_id) > 0:
                for student in students_id:
                    attendance = Attendance.objects.filter(
                        date=date, student=student)
                    if attendance:
                        one_student_attendance = []
                        one_student_attendance.append(
                            attendance[0].student.roll_number)
                        for period in range(1, 9):
                            student_attendance_status = Attendance.objects.filter(
                                student=student, date=date, period=period).first()
                            if student_attendance_status:
                                one_student_attendance.append(
                                    student_attendance_status.status)
                            else:
                                one_student_attendance.append(4)
                        attendance_array.append(one_student_attendance) if len(
                            one_student_attendance) > 0 else None
            else:
                messages.success(request, "No Attendance Records Found")
                return redirect(reverse('admin_view_attendance'))

            return render(request, "hod_template/attendance_view_page.html", {'attendance_list': attendance_array, 'class_name': str(class_id)})
        else:
            messages.error(request, "Invalid Data Provided")
    context = {'form': form, 'page_title': 'Select Attendance Details'}
    return render(request, "hod_template/admin_view_attendance.html", context)


def admin_view_overall_attendance(request):
    user = get_object_or_404(Admin, admin=request.user)
    form = OverallAttendanceSelectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')
            class_id = form.cleaned_data.get('class_name')
            students_id = Student.objects.filter(class_name=class_id)
            current_date = from_date
            overall_attendance = {}
            while current_date <= to_date:
                attendance_array = {}
                if len(students_id) > 0:
                    for student in students_id:
                        if Attendance.objects.filter(date = current_date, student=student, status=1).first():
                            attendance_array[student.roll_number] = 'Present'
                        elif  Attendance.objects.filter(date = current_date, student=student, status=2).first():
                            attendance_array[student.roll_number] = 'OD Internal'
                        elif  Attendance.objects.filter(date = current_date, student=student, status=3).first():
                            attendance_array[student.roll_number] = 'OD External'
                        elif  Attendance.objects.filter(date = current_date, student=student, status=0).first():
                            attendance_array[student.roll_number] = 'Absent'
                        elif  Attendance.objects.filter(date = current_date, student=student, status=4).first():
                            attendance_array[student.roll_number] = 'Pending'
                if len(attendance_array)>0:
                    overall_attendance[str(current_date)]=attendance_array
                current_date += datetime.timedelta(days=1)  
            dates = list(overall_attendance.keys())
            roll_numbers = list(overall_attendance[dates[0]]) if dates else []
            return render(request, "hod_template/overall_attendance_view_page.html", {'overall_attendance': overall_attendance, 'class_name': str(class_id), 'dates': dates, 'roll_numbers':roll_numbers})
        else:
            messages.error(request, "Invalid Data Provided")
    context = {'form': form, 'page_title': 'Select Attendance Details'}

    return render(request, "hod_template/admin_view_overall_attendance.html", context)


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)


def admin_notify_staff(request):
    user = get_object_or_404(Admin, admin=request.user)
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Staff",
        'allStaff': staff
    }
    return render(request, "hod_template/staff_notification.html", context)


def admin_notify_student(request):
    user = get_object_or_404(Admin, admin=request.user)
    student = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Students",
        'students': student
    }
    return render(request, "hod_template/student_notification.html", context)


# def get_subjects(request):
#     department_id = request.GET.get('department')
#     subjects = Subject.objects.all()
#     return JsonResponse(list(subjects), safe=False)


def exam_filter_page(request):
    form = ExamDetailForm()
    context={
        'form':form,
        'page_title': 'Question Paper'
    }
    if request.method == 'POST':
        form = ExamDetailForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data['department']
            subject = form.cleaned_data['subject']
            semester = form.cleaned_data['semester']
            exam_type = form.cleaned_data['exam_type']
            print(department)
            print(subject)
            print(semester)
            print(exam_type)
            exam_detail = ExamDetail.objects.filter(subject=subject, department=department, semester=semester, exam_type=exam_type).first()
            print(exam_detail)
            q_paper = Question.objects.filter(exam_detail=exam_detail).first()

            if q_paper:
                print(q_paper)
                return render(request, "hod_template/question_paper_template.html", {'q_paper':q_paper})
            else:
                messages.error(request, 'No Question Paper Found.')
                
        else:
            messages.error(request, 'There was an error with your form submission.')
    
    return render(request, 'hod_template/exam_filter_page.html', {'form': form})


# @csrf_exempt
# def check_email_availability(request):
#     user = get_object_or_404(Admin, admin=request.user)
#     email = request.POST.get("email")
#     try:
#         user = CustomUser.objects.filter(email=email).exists()
#         if user:
#             return HttpResponse(True)
#         return HttpResponse(False)
#     except Exception as e:
#         return HttpResponse(False)


@csrf_exempt
def student_feedback_message(request):
    user = get_object_or_404(Admin, admin=request.user)
    if request.method != 'POST':
        feedbacks = FeedbackStudent.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Student Feedback Messages'
        }
        return render(request, 'hod_template/student_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStudent, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def staff_feedback_message(request):
    user = get_object_or_404(Admin, admin=request.user)
    if request.method != 'POST':
        feedbacks = FeedbackStaff.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Staff Feedback Messages'
        }
        return render(request, 'hod_template/staff_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStaff, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def view_staff_leave(request):
    user = get_object_or_404(Admin, admin=request.user)
    if request.method != 'POST':
        allLeave = LeaveReportStaff.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Staff'
        }
        return render(request, "hod_template/staff_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStaff, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_student_leave(request):
    user = get_object_or_404(Admin, admin=request.user)
    if request.method != 'POST':
        allLeave = LeaveReportStudent.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Students'
        }
        return render(request, "hod_template/student_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStudent, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


# @csrf_exempt
# def get_admin_attendance(request):
#     user = get_object_or_404(Admin, admin=request.user)
#     subject_id = request.POST.get('subject')
#     session_id = request.POST.get('session')
#     attendance_date_id = request.POST.get('attendance_date_id')
#     try:
#         subject = get_object_or_404(Subject, id=subject_id)
#         session = get_object_or_404(Session, id=session_id)
#         attendance = get_object_or_404(
#             Attendance, id=attendance_date_id, session=session)
#         attendance_reports = AttendanceReport.objects.filter(
#             attendance=attendance)
#         json_data = []
#         for report in attendance_reports:
#             data = {
#                 "status":  str(report.status),
#                 "name": str(report.student)
#             }
#             json_data.append(data)
#         return JsonResponse(json.dumps(json_data), safe=False)
#     except Exception as e:
#         return None


@csrf_exempt
def send_student_notification(request):
    user = get_object_or_404(Admin, admin=request.user)
    id = request.POST.get('id')
    message = request.POST.get('message')
    student = get_object_or_404(Student, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Management System",
                'body': message,
                'click_action': reverse('student_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': student.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStudent(student=student, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_staff_notification(request):
    user = get_object_or_404(Admin, admin=request.user)
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Management System",
                'body': message,
                'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': staff.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def download_student_template(request):
    user = get_object_or_404(Admin, admin=request.user)
    # Create the HTTP response object with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_template.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow([
        'email',
        'password',
        'gender',
        'address',
        'department',
        'class',
        'register_number',
        'roll_number'
    ])

    return response


def download_staff_template(request):
    user = get_object_or_404(Admin, admin=request.user)
    # Create the HTTP response object with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="staff_template.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow([
        'email',
        'password',
        'gender',
        'address',
        'department'
    ])

    return response


# @require_GET
# def download_single_day_attendance(request):
#     attendance_list_str = request.GET.get('attendance_list')
#     if attendance_list_str:
#         try:
#             attendance_list = json.loads(attendance_list_str)
#         except json.JSONDecodeError:
#             attendance_list = []
#     else:
#         attendance_list = []

#     # Create the HTTP response object with CSV content type
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

#     # Create a CSV writer object
#     writer = csv.writer(response)

#     # Write the header row
#     writer.writerow([
#         'Student',
#         'Period 1',
#         'Period 2',
#         'Period 3',
#         'Period 4',
#         'Period 5',
#         'Period 6',
#         'Period 7',
#         'Period 8'
#     ])

#     if len(attendance_list) > 0:
#         for atten in attendance_list:
#             if atten:
#                     print(atten)
#                     writer.writerow([
#                         check_atten_with_number(atten[0]),
#                         check_atten_with_number(atten[1]),
#                         check_atten_with_number(atten[2]),
#                         check_atten_with_number(atten[3]),
#                         check_atten_with_number(atten[4]),
#                         check_atten_with_number(atten[5]),
#                         check_atten_with_number(atten[6]),
#                         check_atten_with_number(atten[7]),
#                         check_atten_with_number(atten[8]),
#                     ])
#     return response


@require_GET
def download_single_day_attendance(request):
    user = get_object_or_404(Admin, admin=request.user)
    attendance_list_str = request.GET.get('attendance_list')
    if attendance_list_str:
        try:
            attendance_list = json.loads(attendance_list_str)
        except json.JSONDecodeError:
            attendance_list = []
    else:
        attendance_list = []
    roll_num_of_one_student = attendance_list[0][0]
    student = get_object_or_404(Student, roll_number=roll_num_of_one_student)

    # Create a workbook and select the active worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = str(student.class_name)+" - Attendance"

    # Define fill colors
    # Orange background for Absent
    absent_fill = PatternFill(start_color="FF4400",
                              end_color="FF4400", fill_type="solid")
    # Yellow background for OD Internal and External
    od_internal_external_fill = PatternFill(
        start_color="FFCC33", end_color="FFCC33", fill_type="solid")
    pending_fill = PatternFill(
        start_color="00555E", end_color="00555E", fill_type="solid")
    text_color_white = openpyxl.styles.Font(color="FFFFFF")  # White text color
    text_color_black = openpyxl.styles.Font(color="000000")  # Black text color

    # Write the header row
    headers = [
        'Roll Number',
        'Period 1',
        'Period 2',
        'Period 3',
        'Period 4',
        'Period 5',
        'Period 6',
        'Period 7',
        'Period 8'
    ]
    for col_num, header in enumerate(headers, 1):
        cell = worksheet.cell(row=1, column=col_num, value=header)
        # Yellow background for headers
        # cell.fill = PatternFill(start_color="FFFF00",
        #                         end_color="FFFF00", fill_type="solid")

    # Write the data rows with conditional formatting
    for row_num, atten in enumerate(attendance_list, 2):
        for col_num, value in enumerate(atten, 1):
            cell = worksheet.cell(
                row=row_num, column=col_num, value=check_atten_with_number(value))
            if value == 0:
                cell.fill = absent_fill
                cell.font = text_color_white
            elif value in [2, 3]:
                cell.fill = od_internal_external_fill
                cell.font = text_color_black
            elif value == 4:
                cell.fill = pending_fill
                cell.font = text_color_white

    # Create the HTTP response object with Excel content type
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{str(student.class_name)} -attendance.xlsx"'

    # Save the workbook to the response object
    workbook.save(response)

    return response


def check_atten_with_number(atten):
    if atten != 0 and atten != 1 and atten != 2 and atten != 3 and atten != 4:
        return atten
    elif atten == 0:
        return 'Absent'
    elif atten == 1:
        return 'Present'
    elif atten == 2:
        return 'On Duty Internal'
    elif atten == 3:
        return 'On Duty External'
    elif atten == 4:
        return 'Pending'


@require_GET
def download_overall_day_attendance(request):
    print('frbtdg\n\n\n')
    user = get_object_or_404(Admin, admin=request.user)
    overall_attendance = json.loads(request.GET.get('overall_attendance', '{}'))

    # Add headers
    dates = list(overall_attendance.keys())
    roll_numbers = list(next(iter(overall_attendance.values())).keys())
    student = get_object_or_404(Student, roll_number=roll_numbers[0])
    # Create an Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f'Attendance of {student.class_name}'


    header = ['Roll Number'] + dates
    sheet.append(header)

    # Add data
    for reg in roll_numbers:
        row = [reg]
        for date in dates:
            row.append(overall_attendance[date].get(reg, ''))
        sheet.append(row)

    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename={student.class_name}_overall_attendance.xlsx'

    # Save workbook to response
    workbook.save(response)
    return response