# Generated by Django 3.2.7 on 2021-09-25 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_alter_student_major'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='major',
            field=models.ManyToManyField(blank=True, to='schedule.Week'),
        ),
    ]