# Generated by Django 3.1.1 on 2024-07-20 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20240720_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentanswers',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='assignments/answers'),
        ),
        migrations.AlterField(
            model_name='assignmentquestions',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='assignments/questions'),
        ),
        migrations.AlterField(
            model_name='assignmentquestions',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('1', 'HOD'), ('2', 'Staff'), ('3', 'Student')], default=1, max_length=1),
        ),
    ]
