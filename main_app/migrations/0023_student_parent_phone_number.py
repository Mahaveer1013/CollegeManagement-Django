# Generated by Django 5.0.7 on 2024-07-26 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_student_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='parent_phone_number',
            field=models.IntegerField(default=9962526764, max_length=10),
        ),
    ]