from .models import AdminAccessLog
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import *
from .forms import *
from .admin_forms import *


class NonEmptyDetailsFilter(admin.SimpleListFilter):
    title = 'details'
    parameter_name = 'non_empty_details'

    def lookups(self, request, model_admin):
        return (
            ('NonEmpty', 'Details Not Empty'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'NonEmpty':
            return queryset.exclude(details='-').exclude(details=None)
        return queryset
    

class ActionLoggingMixin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Save the model instance first
        super().save_model(request, obj, form, change)
        model_name = obj.__class__.__name__
        # Log the action
        if change:
            ActionLog.objects.create(
                user=request.user,
                action=f'Updated {model_name} instance',
                details=f'Updated {obj}'
            )
        else:
            ActionLog.objects.create(
                user=request.user,
                action=f'Created {model_name} instance',
                details=f'Created {obj}'
            )

    def delete_model(self, request, obj):
        model_name = obj.__class__.__name__
        print(model_name)
        # Log the action before deleting
        ActionLog.objects.create(
            user=request.user,
            action=f'Deleted {model_name} instance',
            details=f'Deleted {obj}'
        )
        # Delete the model instance
        super().delete_model(request, obj)


@admin.register(TimeTable)
class TimeTableAdmin(ActionLoggingMixin, admin.ModelAdmin):
    form = TimeTableForm


@admin.register(Period)
class PeriodAdmin(ActionLoggingMixin, admin.ModelAdmin):
    form = PeriodForm
    list_display = ('subject', 'class_name', 'department', 'staff')


@admin.register(Staff)
class StaffAdmin(ActionLoggingMixin, admin.ModelAdmin):
    form = StaffForm
    list_display = ('faculty_id', 'user', 'department',
                    'phone_number', 'resume_link')
    list_per_page=50
    list_filter = ('faculty_id','department')

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank">View RESUME</a>', obj.resume.url)
        return "No RESUME"

    resume_link.short_description = 'RESUME'


@admin.register(Student)
class StudentAdmin(ActionLoggingMixin, admin.ModelAdmin):
    form = StudentForm
    list_display = ('user', 'class_name', 'roll_number',
                    'register_number', 'academic_year')
    list_filter = ('class_name','roll_number','department')
    list_per_page=50


@admin.register(AssignmentQuestion)
class AssignmentQuestionsAdmin(ActionLoggingMixin, admin.ModelAdmin):
    # Hide the 'uploaded_by' field in the admin form
    exclude = ('uploaded_by',)
    list_display = ('class_name', 'pdf_link', 'subject', 'uploaded_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (and not updated)
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        staff_member = Staff.objects.filter(user=request.user).first()
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

    def pdf_link(self, obj):
        if obj.pdf:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.pdf.url)
        return "No PDF"

    pdf_link.short_description = 'PDF'


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
        (None, {'fields': ('email', 'first_name', 'last_name',
         'user_type', 'gender', 'profile_pic', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'gender', 'profile_pic', 'address')}
         ),
    )


@admin.register(Question)
class QuestionAdmin(ActionLoggingMixin, admin.ModelAdmin):
    form = QuestionForm

    list_display = ('exam_detail', )

    exclude = [
        'bloom_level1', 'bloom_level2', 'bloom_level3', 'bloom_level4',
        'bloom_level5', 'bloom_level6', 'bloom_level7', 'bloom_level8',
        'bloom_level9', 'bloom_level10', 'bloom_level11', 'bloom_level12',
        'bloom_level13', 'bloom_level14', 'bloom_level15', 'bloom_level16',
        'bloom_level17', 'bloom_level18', 'bloom_level19', 'bloom_level20',
        'bloom_level21', 'bloom_level22'
    ]

    def save_model(self, request, obj, form, change):
        # Update Bloom levels based on question text
        if not change:  # If creating a new Question
            for i in range(1, 23):
                question_text = getattr(obj, f'question_text{i}')
                if question_text:
                    words = question_text.split()
                    bloom_level = None

                    for word in words:
                        word = word.strip()
                        if word:
                            bloom_keyword = BloomKeyword.objects.filter(
                                word__iexact=word).first()
                            print(bloom_keyword)
                            if bloom_keyword.bloom_level == 1:
                                bloom_level = 'Creating'
                                break
                            if bloom_keyword.bloom_level == 2:
                                bloom_level = 'Evaluate'
                                break
                            if bloom_keyword.bloom_level == 3:
                                bloom_level = 'Analyzing'
                                break
                            if bloom_keyword.bloom_level == 4:
                                bloom_level = 'Applying'
                                break
                            if bloom_keyword.bloom_level == 5:
                                bloom_level = 'Understanding'
                                break
                            if bloom_keyword.bloom_level == 6:
                                bloom_level = 'Remember'
                                break

                    setattr(obj, f'bloom_level{i}', bloom_level)

        super().save_model(request, obj, form, change)


@admin.register(Note)
class NotesAdmin(ActionLoggingMixin, admin.ModelAdmin):
    # Hide the 'uploaded_by' field in the admin form
    exclude = ('uploaded_by',)
    list_display = ('subject', 'department', 'pdf_link', 'title', 'uploaded_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (and not updated)
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def pdf_link(self, obj):
        if obj.pdf:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.pdf.url)
        return "No PDF"

    pdf_link.short_description = 'PDF'


@admin.register(AdminAccessLog)
class AdminAccessLogAdmin(ActionLoggingMixin, admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'accessed_at',)
    list_filter = ('accessed_at',)
    search_fields = ('user__username', 'ip_address',)
    list_per_page = 50


@admin.register(ExamDetail)
class ExamDetailAdmin(ActionLoggingMixin, admin.ModelAdmin):
    exclude = ('uploaded_by',)


    list_display = ('subject', 'department', 'exam_type',
                    'semester', 'academic_year')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (and not updated)
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Notice)
class NoticeAdmin(ActionLoggingMixin, admin.ModelAdmin):
    exclude = ('uploaded_by',)

    list_display = ('title', 'poster_link', 'uploaded_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (and not updated)
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def poster_link(self, obj):
        if obj.poster:
            return format_html('<a href="{}" target="_blank">View Poster</a>', obj.poster.url)
        return "No Poster"

    poster_link.short_description = 'POSTER'


@admin.register(ClassList)
class ClassListAdmin(ActionLoggingMixin, admin.ModelAdmin):
    list_display = ('department', 'semester', 'section')
    list_filter = ['department', 'semester']
    ordering = ('department',)


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'details')
    list_filter = ('timestamp', 'user',  NonEmptyDetailsFilter)
    list_per_page = 50


admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(AcademicYear)
# admin.site.register(ClassList)
