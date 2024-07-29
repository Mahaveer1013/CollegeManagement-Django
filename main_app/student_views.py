import json
import math
from datetime import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from .forms import *
from .models import *


def student_home(request):
    student = get_object_or_404(Student, user=request.user)
    total_subject = Subject.objects.count()
    total_attendance = Attendance.objects.filter(student=student).count()
    total_present = Attendance.objects.filter(
        student=student, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    subject_name = []
    data_present = []
    data_absent = []
    subjects = Subject.objects.all()
    for subject in subjects:
        present_count = Attendance.objects.filter(student=student,subject=subject,status=1).count()
        absent_count = Attendance.objects.filter(student=student,subject=subject,status=0).count()
        subject_name.append(subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    context = {
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_subject': total_subject,
        'subjects': subjects,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': subject_name,
        'page_title': 'Student Homepage'

    }
    return render(request, 'student_template/home_content.html', context)


def student_profile(request):
    student=get_object_or_404(Student,user=request.user)
    return render(request, 'student_template/student_profile.html',{'student':student})

def student_view_timetable(request):
    student = get_object_or_404(Student, user=request.user)
    timetable = TimeTable.objects.filter(class_name=student.class_name).first()

    return render(request, 'student_template/student_timetable.html', {'timetable':timetable, 'class_name':str(timetable.class_name)})


def student_view_notice(request):
    user = get_object_or_404(Student, user=request.user)
    notices = Notice.objects.filter(department=user.department) | Notice.objects.filter(department__isnull=True)
    context = {
        'page_title': 'Notice List',
        'notices': notices
    }
    return render(request, 'student_template/view_notices.html', context)


def student_view_certificate(request):
    user = get_object_or_404(Student, user=request.user)
    certificates = Certificate.objects.filter(student=user)
    return render(request,'student_template/student_view_certificate.html',{'page_title': 'My Certificates','certificates':certificates})



def student_upload_certificate(request):
    user = get_object_or_404(Student, user=request.user)
    form = CertificateForm(request.POST or None, request.FILES or None)
    context={
        'form':form,
        'page_title': 'Upload Certificate'
    }
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            certificate = form.cleaned_data['certificate']
            certificate_data = Certificate()
            certificate_data.title = title 
            certificate_data.student=user
            certificate_data.description = description 
            certificate_data.certificate = certificate 
            certificate_data.save()
            return redirect('student_view_certificate')
        else:
            messages.error(request, 'There was an error with your form submission.')
    
    return render(request, 'student_template/student_upload_certificate.html', context)

def delete_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    if request.method == "POST":
        certificate.delete()
        messages.success(request, "Certificate deleted successfully.")
        return redirect(reverse('student_view_certificate'))
    return render(request, 'certificates.html', {'certificates': Certificate.objects.all()})


@ csrf_exempt
def student_view_attendance(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method != 'POST':
        department = get_object_or_404(Department, id=student.department.id)
        context = {
            'subjects': Subject.objects.filter(department=department),
            'page_title': 'View Attendance'
        }
        return render(request, 'student_template/student_view_attendance.html', context)
    else:
        subject_id = request.POST.get('subject')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            subject = get_object_or_404(Subject, id=subject_id)
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            attendance = Attendance.objects.filter(
                date__range=(start_date, end_date), subject=subject)
            attendance_reports = AttendanceReport.objects.filter(
                attendance__in=attendance, student=student)
            json_data = []
            for report in attendance_reports:
                data = {
                    "date":  str(report.attendance.date),
                    "status": report.status
                }
                json_data.append(data)
            return JsonResponse(json.dumps(json_data), safe=False)
        except Exception as e:
            return None


def student_apply_leave(request):
    form = LeaveReportStudentForm(request.POST or None, request.FILES or None)
    student = get_object_or_404(Student, user_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportStudent.objects.filter(student=student),
        'page_title': 'Apply for leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.instance
                obj.student = student
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('student_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            print(form.errors, 'fbrt fng') 
            messages.error(request, "Form has errors!")
    return render(request, "student_template/student_apply_leave.html", context)


def student_feedback(request):
    form = FeedbackStudentForm(request.POST or None)
    student = get_object_or_404(Student, user_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStudent.objects.filter(student=student),
        'page_title': 'Student Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.student = student
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('student_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "student_template/student_feedback.html", context)


def student_disciplinary_action(request):
    student= get_object_or_404(Student,user=request.user)
    actions = DisciplinaryAction.objects.filter(student=student)
    return render(request,'student_template/student_disciplinary_action.html',{'actions':actions,'student':student})


def student_view_profile(request):
    student = get_object_or_404(Student, user=request.user)
    form = StudentEditForm(request.POST or None, request.FILES or None,
                           instance=student)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                user = student.user
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    # passport_url = fs.url(filename)
                    user.profile_pic = filename
                user.first_name = first_name
                user.last_name = last_name
                user.address = address
                user.gender = gender
                user.save()
                student.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('student_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))

    return render(request, "student_template/student_view_profile.html", context)


def student_view_assignment(request):
    student = get_object_or_404(Student, user=request.user)
    
    if request.method == 'POST':
        try:
            assignment_id = request.POST.get('assignment_id')
            assignment = get_object_or_404(AssignmentQuestion, id=assignment_id)
            form = AssignmentAnswersForm(request.POST, request.FILES, prefix=str(assignment.id))
            if form.is_valid():
                pdf_file = form.cleaned_data['pdf']
                AssignmentAnswers.objects.update_or_create(
                    student=student,
                    assignment_question=assignment,
                    defaults={'pdf': pdf_file}
                )
                messages.success(request, f"Answer submitted for assignment {assignment.subject}.")
            else:
                messages.error(request, f"Error submitting answer for assignment {assignment.subject}.")
        except Exception as e:
            messages.error(request, "Error Occurred Uploading Answer " + str(e))
    
    assignments = AssignmentQuestion.objects.filter(class_name=student.class_name)
    
    # Initialize the context with assignments and forms
    context = {
        'assignments': assignments,
        'forms': {},
        'page_title': 'View Assignments',
        'button_text': 'Submit',
        'answer_urls': {}
    }
    
    for assignment in assignments:
        # Check if an answer already exists for this student and assignment
        existing_answer = AssignmentAnswers.objects.filter(
            student=student,
            assignment_question=assignment
        ).first()

        # Create the form with the appropriate prefix
        form = AssignmentAnswersForm(prefix=str(assignment.id))
        
        # Add the form and existing answer to the context
        context['forms'][assignment.id] = form
        if existing_answer and existing_answer.pdf:
            context['answer_urls'][assignment.id] = existing_answer.pdf.url
        else:
            context['answer_urls'][assignment.id] = None

    return render(request, 'student_template/student_view_assignment.html', context)


def student_view_note(request):
    student = get_object_or_404(Student, user=request.user)
    all_student_periods = Period.objects.filter(class_name=student.class_name).values_list('subject', flat=True)
    print(all_student_periods)
    notes = Note.objects.filter(department=student.department, subject__in=all_student_periods).annotate(
    str_representation=Concat(
        'department__name',  # Assuming the Department model has a 'name' field
        Value(' - '),
        'subject__name',     # Assuming the Subject model has a 'name' field
        Value(' - '),
        'title',
        output_field=CharField()
    )
).order_by('str_representation')
    return render(request, 'student_template/student_notes.html', {'notes':notes})


@csrf_exempt
def student_fcmtoken(request):
    token = request.POST.get('token')
    student_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        student_user.fcm_token = token
        student_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def student_view_notification(request):
    student = get_object_or_404(Student, user=request.user)
    notifications = NotificationStudent.objects.filter(student=student)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "student_template/student_view_notification.html", context)


def student_view_result(request):
    student = get_object_or_404(Student, user=request.user)
    results = StudentResult.objects.filter(student=student)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "student_template/student_view_result.html", context)
