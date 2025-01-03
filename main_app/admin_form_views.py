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
        if class_name_id is None:
            return Subject.objects.none()

        # Retrieve the class object
        class_name = get_object_or_404(ClassList, pk=int(class_name_id))
        
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

        # Filter subjects by class_name if provided
        if class_name_id:
            period_qs = Period.objects.filter(class_name=class_name)
            subject_ids = period_qs.values_list('subject_id', flat=True)
            subject_qs = subject_qs.filter(id__in=subject_ids)

        # Exclude subjects that are already assigned to any staff
        subject_qs = subject_qs.exclude(id__in=exclude_subject_ids)
        
        # Print statement for debugging
        print('Filtered subjects:', subject_qs)

        # Filter periods for the specific class and subject
        periods = []
        for subject in subject_qs:
            period = Period.objects.filter(class_name=class_name, subject=subject).first()
            print(period)
            periods.append(period)
        print(periods)

        return periods
