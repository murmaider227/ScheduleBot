# Generated by Django 3.2.7 on 2021-09-25 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0013_auto_20210925_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='major',
            field=models.ManyToManyField(blank=True, to='schedule.Group'),
        ),
    ]
