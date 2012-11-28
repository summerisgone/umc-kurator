# -*- coding: utf-8 -*-
from models import Listener, Employee
from django.contrib import admin

class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    fields = ('username', 'first_name', 'last_name', 'password', 'patronymic', 'phone', 'department', 'groups')

class ListenerAdmin(admin.ModelAdmin):
    model = Listener
    fields = (
        'first_name', 'last_name', 'patronymic',
        'first_name_inflated', 'last_name_inflated', 'patronymic_inflated',
        'organization'
    )

admin.site.register(Listener, ListenerAdmin)
admin.site.register(Employee, EmployeeAdmin)
