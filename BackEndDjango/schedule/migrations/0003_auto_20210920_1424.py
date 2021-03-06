# Generated by Django 3.2.7 on 2021-09-20 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20210920_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='week',
            name='odd',
        ),
        migrations.AddField(
            model_name='week',
            name='option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.option', verbose_name='Вариант'),
        ),
    ]
