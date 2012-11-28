# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin
from models import Listener, Employee


class UserAdmin(admin.ModelAdmin):

    def save_form(self, request, form, change=False):
        instance = super(UserAdmin, self).save_form(request, form, change)
        # hack for Django
        if not change:
            instance.set_password(instance.password)
        return instance


class EmployeeAdmin(UserAdmin):
    model = Employee
    add_form = UserCreationForm
    fields = ('username', 'password', 'first_name', 'last_name', 'patronymic', 'phone', 'department', 'groups')


class ListenerAdmin(UserAdmin):
    model = Listener
    add_form = UserCreationForm
    fields = (
        'first_name', 'last_name', 'patronymic',
        'first_name_inflated', 'last_name_inflated', 'patronymic_inflated',
        'organization'
    )

admin.site.register(Listener, ListenerAdmin)
admin.site.register(Employee, EmployeeAdmin)
