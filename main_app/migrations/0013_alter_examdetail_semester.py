# Generated by Django 5.0.7 on 2024-07-25 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_academicyear_remove_examdetail_academic_year_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examdetail',
            name='semester',
            field=models.CharField(choices=[('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th'), ('7th', '7th'), ('8th', '8th')], max_length=3),
        ),
    ]
