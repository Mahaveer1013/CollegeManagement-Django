import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .forms import *
from .models import *
from django.db.models import Q


def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)
    total_students = Student.objects.filter(department=staff.department).count()
    total_leave = LeaveReportStaff.objects.filter(staff=staff).count()
    subjects = Subject.objects.filter(period__staff=staff).distinct()
    print(subjects, 'this is sthe stsaff\n\n\n')
    total_subject = subjects.count()
    # attendance_list = Attendance.objects.filter(subject__in=subjects)
    # total_attendance = attendance_list.count()
    # attendance_list = []
    subject_list = []
    for subject in subjects:
        # attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name)
        # attendance_list.append(attendance_count)
    context = {
        'page_title': 'Staff Panel - ' + str(staff.admin.last_name) + ' (' + str(staff.department) + ')',
        'total_students': total_students,
        'total_attendance': 10,
        'total_leave': total_leave,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': [1,2]
    }
    return render(request, 'staff_template/home_content.html', context)


def staff_take_attendance(request):
    periods = range(1, 9)

    context = {
        'page_title': 'Take Attendance',
        'form': DateSelectionForm(),
        'periods': periods
    }

    return render(request, 'staff_template/staff_take_attendance.html', context)

@csrf_exempt  # Temporarily exempt from CSRF validation for debugging
def fetch_students(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        period = request.POST.get('period')

        if not date or not period:
            return JsonResponse({'error': 'Date and period are required.'}, status=400)

        # Assuming `date` is a string, convert it to a datetime object if needed
        # Process date and period to filter timetable and students

        # Example to get weekday number from date string (assuming YYYY-MM-DD format)
        from datetime import datetime
        try:
            selected_date = datetime.strptime(date, '%Y-%m-%d')
            weekday = selected_date.weekday()
            print(weekday,'\n\n\n\n')
        except ValueError:
            return JsonResponse({'error': 'Invalid date format.'}, status=400)

        # Map weekday number to day names
        days_of_week = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday',
        }

        # Build the period attribute based on the selected period
        # week_number = datetime.date(2024, 2, 26).isocalendar()[1]
        if weekday!=5 and weekday!=6:
            period_attr = f'{days_of_week.get(weekday, "unknown")}_{period}'
        else:
            period_attr='Leave'
        

        # Filter timetables for the selected date, period
        if period_attr != 'Leave':
            timetables = TimeTable.objects.filter(**{f"{period_attr}__isnull": False})
            class_ids = timetables.values_list('class_name_id', flat=True)
            # print('class_ids', class_ids)
            students = Student.objects.filter(class_name_id__in=class_ids)
            if len(students)>0:
                student_data = []
                for student in students:
                    # print(student.admin.first_name)
                    student_data.append({
                        'id':student.id,
                        'name': student.admin.first_name+ ' '+ student.admin.last_name,
                        'roll_number': student.roll_number
                    })
                # print(student_data)
                return JsonResponse({'students': student_data,'date':date, 'period':period})
            return JsonResponse({'error': 'No students Found'}, status=404)
        else:
            return JsonResponse({'message': 'Its a Holiday'})

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def submit_attendance(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        period = request.POST.get('period')
        checked = request.POST.get('checked_students')
        unchecked = request.POST.get('unchecked_students')
        student_ids = request.POST.getlist('student_data')
        print('thlbcyudbsoduvbds\nm\n\n\n\n\n')
        print(date,period)
        print(checked)
        print(unchecked)

        # Process the data to mark attendance
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            # You can adjust how you store attendance records based on your model
            # For example, you might have an Attendance model to store this data
            attendance_record, created = Attendance.objects.get_or_create(
                student=student,
                date=date,
                period=period,
                defaults={'present': True}
            )
            if not created:
                attendance_record.present = True
                attendance_record.save()

        return redirect('staff_take_attendance')  # Redirect to a success page or the same page

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def add_assignment(request):
    print('this is my data \n',get_object_or_404(Staff, admin=request.user))
    if request.method == 'POST':
        if student_form.is_valid():
            deadline_date = student_form.cleaned_data.get('deadline_date')
            class_name = student_form.cleaned_data.get('class_name')
            pdf = request.FILES['pdf']
            fs = FileSystemStorage()
            filename = fs.save(pdf.name, pdf)
            pdf_url = fs.url(filename)
            try:
                user = CustomUser()
                user.uploaded_by=request.user
                user.deadline_date=deadline_date
                user.class_name=class_name
                user.pdf=pdf_url
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    student_form = AssignmentQuestionsForm(request.POST or None, request.FILES or None)
    context = {'form': student_form, 'page_title': 'Add Student'}
    return render(request, 'hod_template/add_student_template.html', context)


@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        students = Student.objects.filter(
            department_id=subject.department.id, session=session)
        student_data = []
        for student in students:
            data = {
                    "id": student.id,
                    "name": student.admin.last_name + " " + student.admin.first_name
                    }
            student_data.append(data)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def save_attendance(request):
    student_data = request.POST.get('student_ids')
    date = request.POST.get('date')
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    students = json.loads(student_data)
    try:
        session = get_object_or_404(Session, id=session_id)
        subject = get_object_or_404(Subject, id=subject_id)
        attendance = Attendance(session=session, subject=subject, date=date)
        attendance.save()

        for student_dict in students:
            student = get_object_or_404(Student, id=student_dict.get('id'))
            attendance_report = AttendanceReport(student=student, attendance=attendance, status=student_dict.get('status'))
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def staff_update_attendance(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff_id=staff)
    sessions = Session.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'Update Attendance'
    }

    return render(request, 'staff_template/staff_update_attendance.html', context)


@csrf_exempt
def get_student_attendance(request):
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        date = get_object_or_404(Attendance, id=attendance_date_id)
        attendance_data = AttendanceReport.objects.filter(attendance=date)
        student_data = []
        for attendance in attendance_data:
            data = {"id": attendance.student.admin.id,
                    "name": attendance.student.admin.last_name + " " + attendance.student.admin.first_name,
                    "status": attendance.status}
            student_data.append(data)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def update_attendance(request):
    student_data = request.POST.get('student_ids')
    date = request.POST.get('date')
    students = json.loads(student_data)
    try:
        attendance = get_object_or_404(Attendance, id=date)

        for student_dict in students:
            student = get_object_or_404(
                Student, admin_id=student_dict.get('id'))
            attendance_report = get_object_or_404(AttendanceReport, student=student, attendance=attendance)
            attendance_report.status = student_dict.get('status')
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def staff_apply_leave(request):
    form = LeaveReportStaffForm(request.POST or None)
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportStaff.objects.filter(staff=staff),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.staff = staff
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('staff_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/staff_apply_leave.html", context)


def view_assignment(request):
    # Get all assignments posted by the staff (user)
    assignments = AssignmentQuestions.objects.filter(uploaded_by=request.user)
    print(assignments, '\n\n\n\n')
    # Retrieve all answers for the assignments posted by the staff
    assignment_answers = AssignmentAnswers.objects.filter(assignment_question__in=assignments)
    
    # Create a dictionary to map assignments to their answers
    assignment_answers_dict = {}
    for assignment in assignments:
        assignment_answers_dict[assignment.id] = assignment_answers.filter(assignment_question=assignment)
    
    context = {
        'assignments': assignments,
        'assignment_answers': assignment_answers_dict
    }
    
    return render(request, 'staff_template/staff_view_assignment.html', context)


def staff_feedback(request):
    form = FeedbackStaffForm(request.POST or None)
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStaff.objects.filter(staff=staff),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.staff = staff
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('staff_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/staff_feedback.html", context)


def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = StaffEditForm(request.POST or None, request.FILES or None,instance=staff)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = staff.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                staff.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('staff_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "staff_template/staff_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "staff_template/staff_view_profile.html", context)

    return render(request, "staff_template/staff_view_profile.html", context)


@csrf_exempt
def staff_fcmtoken(request):
    token = request.POST.get('token')
    try:
        staff_user = get_object_or_404(CustomUser, id=request.user.id)
        staff_user.fcm_token = token
        staff_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def staff_view_notification(request):
    staff = get_object_or_404(Staff, admin=request.user)
    notifications = NotificationStaff.objects.filter(staff=staff)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "staff_template/staff_view_notification.html", context)


def staff_add_result(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff)
    sessions = Session.objects.all()
    context = {
        'page_title': 'Result Upload',
        'subjects': subjects,
        'sessions': sessions
    }
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student_list')
            subject_id = request.POST.get('subject')
            test = request.POST.get('test')
            exam = request.POST.get('exam')
            student = get_object_or_404(Student, id=student_id)
            subject = get_object_or_404(Subject, id=subject_id)
            try:
                data = StudentResult.objects.get(
                    student=student, subject=subject)
                data.exam = exam
                data.test = test
                data.save()
                messages.success(request, "Scores Updated")
            except:
                result = StudentResult(student=student, subject=subject, test=test, exam=exam)
                result.save()
                messages.success(request, "Scores Saved")
        except Exception as e:
            messages.warning(request, "Error Occured While Processing Form")
    return render(request, "staff_template/staff_add_result.html", context)


@csrf_exempt
def fetch_student_result(request):
    try:
        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)
        result = StudentResult.objects.get(student=student, subject=subject)
        result_data = {
            'exam': result.exam,
            'test': result.test
        }
        return HttpResponse(json.dumps(result_data))
    except Exception as e:
        return HttpResponse('False')

