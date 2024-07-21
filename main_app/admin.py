from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import *
from .admin_models import *
from dal import autocomplete
from .forms import *


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name',
                  'user_type', 'gender', 'profile_pic', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.pk:  # If the user is being created (not updated)
            # Set the email as the password
            user.password = make_password(user.email)
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    add_form = CustomUserForm
    model = CustomUser

    list_display = ['email', 'first_name', 'last_name', 'user_type', 'gender']
    list_filter = ['user_type', 'gender']
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'user_type', 'gender', 'profile_pic', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'gender', 'profile_pic', 'address', 'password1', 'password2')}
         ),
    )
class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = '__all__'
        widgets = {
            'class_name': autocomplete.ModelSelect2(url='dep-to-class-autocomplete', forward=['department'])
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        linked_student_users = Student.objects.values_list(
            'admin_id', flat=True)
        linked_staff_users = Staff.objects.values_list('admin_id', flat=True)
        # Combine both sets of linked users
        linked_users = set(linked_student_users).union(set(linked_staff_users))
        # Exclude those users from the options in the admin field
        self.fields['admin'].queryset = CustomUser.objects.exclude(
            id__in=linked_users
        ).exclude(user_type='3').exclude(user_type='1')
        if self.instance.pk:
            self.fields['admin'].disabled = True


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'class_name': autocomplete.ModelSelect2(url='dep-to-class-autocomplete', forward=['department']),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        linked_student_users = Student.objects.values_list(
            'admin_id', flat=True)
        linked_staff_users = Staff.objects.values_list('admin_id', flat=True)
        # Combine both sets of linked users
        linked_users = set(linked_student_users).union(set(linked_staff_users))
        # Exclude those users from the options in the admin field
        self.fields['admin'].queryset = CustomUser.objects.exclude(
            id__in=linked_users).exclude(user_type='2').exclude(user_type='1')
        if self.instance.pk:
            self.fields['admin'].disabled = True


class StaffAdmin(admin.ModelAdmin):
    form = StaffForm


class StudentAdmin(admin.ModelAdmin):
    form = StudentForm


class PeriodAdmin(admin.ModelAdmin):
    form = PeriodForm


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    form = TimeTableForm


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    form = PeriodForm


class AssignmentQuestionsAdmin(admin.ModelAdmin):
    # Hide the 'uploaded_by' field in the admin form
    exclude = ('uploaded_by',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (and not updated)
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        staff_member = Staff.objects.filter(admin=request.user).first()
        if staff_member:
            # Filter class_name to show only the classes where the staff is a subject teacher
            periods = Period.objects.filter(staff=staff_member).values_list(
                'class_name', flat=True).distinct()
            form.base_fields['class_name'].queryset = ClassList.objects.filter(
                id__in=periods)
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(uploaded_by=request.user)


admin.site.register(AssignmentQuestions, AssignmentQuestionsAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ClassList)
admin.site.register(BloomKeyword)
admin.site.register(QuestionPaper)
