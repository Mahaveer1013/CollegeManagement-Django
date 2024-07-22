from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from dal import autocomplete
from .models import *
from .admin_models import *
from .forms import *
from .admin_forms import *

from django.contrib.auth.models import Permission

class CustomPermission(Permission):
    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.name}"

admin.site.register(CustomPermission)


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    form = TimeTableForm


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    form = PeriodForm


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    form = StaffForm


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm


@admin.register(AssignmentQuestions)
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


@admin.register(CustomUser)
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
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'gender', 'profile_pic', 'address')}
         ),
    )


admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(ClassList)
admin.site.register(BloomKeyword)
admin.site.register(QuestionPaper)
