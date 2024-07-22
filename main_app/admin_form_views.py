from dal import autocomplete
from .models import *
from django.db.models import Q
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)

class DepToClass(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ClassList.objects.none()

        class_list = ClassList.objects.all()

        department_id = self.forwarded.get('department', None)

        if department_id:
            class_list = class_list.filter(department_id=department_id)

        return class_list 
    
class TimetableDepToClass(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ClassList.objects.none()

        # Get all classes
        class_list = ClassList.objects.all()

        # Filter by department if provided
        department_id = self.forwarded.get('department', None)
        if department_id:
            class_list = class_list.filter(department_id=department_id)

        # Exclude classes that are already linked with a timetable
        timetable_classes = TimeTable.objects.values_list('class_name_id', flat=True)
        class_list = class_list.exclude(id__in=timetable_classes)

        return class_list
    

class ClassToSub(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Subject.objects.none()

        # Get class_name_id from the forwarded data
        class_name_id = self.forwarded.get('class_name', None)
        
        # Get all timetables
        timetables = TimeTable.objects.all()

        # Get all periods assigned to staff and the corresponding subjects
        exclude_subject_ids = set()
        for timetable in timetables:
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
                for period_number in range(1, 9):
                    period_attr = f'{day}_{period_number}'
                    period = getattr(timetable, period_attr, None)
                    if period:
                        exclude_subject_ids.add(period.subject.id)

        # Get all subjects initially
        subject_qs = Subject.objects.all()

        # Filter subjects by class_name_id if provided
        if class_name_id:
            period_qs = Period.objects.filter(class_name_id=class_name_id)
            subject_ids = period_qs.values_list('subject_id', flat=True)
            subject_qs = subject_qs.filter(id__in=subject_ids)

        # Exclude subjects that are already assigned to any staff
        subject_qs = subject_qs.exclude(id__in=exclude_subject_ids)

        return subject_qs

        if not self.request.user.is_authenticated:
            return Period.objects.none()

        # Get all periods initially
        period_qs = Period.objects.all()

        # Get class_name_id from the forwarded data
        class_name_id = self.forwarded.get('class_name', None)
        
        # Filter periods by class_name_id if provided
        if class_name_id:
            period_qs = period_qs.filter(class_name_id=class_name_id)
        
        # Get all timetables
        timetables = TimeTable.objects.all()
        
        # Get periods to exclude
        exclude_periods_ids = set()
        for timetable in timetables:
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
                for period_number in range(1, 9):
                    period_attr = f'{day}_{period_number}'
                    period = getattr(timetable, period_attr, None)
                    if period and period.staff:
                        exclude_periods_ids.add(period.id)
        
        # Exclude periods that are already assigned to any staff
        period_qs = period_qs.exclude(id__in=exclude_periods_ids)

        return period_qs