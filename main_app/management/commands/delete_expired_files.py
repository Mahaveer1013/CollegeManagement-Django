# myapp/management/commands/delete_expired_files.py
from django.core.management.base import BaseCommand
from main_app.models import Note
from django.utils import timezone
import os

class Command(BaseCommand):
    help = 'Delete expired notes'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_notes = Note.objects.filter(deadline_date__lt=now)
        for note in expired_notes:
            # Delete the file
            if note.pdf and os.path.isfile(note.pdf.path):
                os.remove(note.pdf.path)
            
            # Delete the database record
            note.delete()
            
        self.stdout.write(self.style.SUCCESS('Successfully deleted expired notes.'))
