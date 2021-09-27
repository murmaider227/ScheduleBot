from django.contrib import admin
from .models import *


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    search_fields=('day__name','group__major__name','group__year')


admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(Group)
