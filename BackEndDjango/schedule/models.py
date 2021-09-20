from django.db import models


class Day(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Year(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)


class Option(models.Model):
    option = models.IntegerField()

    def __str__(self):
        return str(self.option)


class Week(models.Model):
    major = models.ForeignKey('Major', on_delete=models.CASCADE, verbose_name='Специальность')
    year = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name='Курс', null=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, verbose_name='Вариант', null=True)
    subject1_name = models.CharField(max_length=40, blank=True)
    subject1_teacher = models.CharField(max_length=40, blank=True)
    subject2_name = models.CharField(max_length=40, blank=True)
    subject2_teacher = models.CharField(max_length=40, blank=True)
    subject3_name = models.CharField(max_length=40, blank=True)
    subject3_teacher = models.CharField(max_length=40, blank=True)
    subject4_name = models.CharField(max_length=40, blank=True)
    subject4_teacher = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return str(self.major) + ' | ' + str(self.year) + ' | ' + str(self.day)


class Student(models.Model):
    username = models.CharField(max_length=60)
    telegram_id = models.BigIntegerField()
    major = models.ForeignKey('Major', on_delete=models.CASCADE)


class Faculty(models.Model):
    name = models.CharField(max_length=40) 

    def __str__(self):
        return self.name


class Major(models.Model):
    name = models.CharField(max_length=40)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



