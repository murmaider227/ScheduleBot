# Generated by Django 3.2.7 on 2021-09-25 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0010_alter_student_major'),
    ]

    operations = [
        migrations.AlterField(
            model_name='major',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
