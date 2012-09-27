# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from schedule import enums


class ExtendedUser(User):
    class Meta:
        abstract = True

    patronymic = models.CharField(verbose_name=u'Отчество', max_length=255)
    phone = models.CharField(verbose_name=u'Телефон', max_length=50)

class Teacher(ExtendedUser):
    department = models.ForeignKey('core.Department')


class Listener(ExtendedUser):
    category = models.CharField(verbose_name=u'Категория', max_length=50, choices=enums.LISTENER_CATEGORIES)
    position = models.CharField(verbose_name=u'Должность', max_length=50, choices=enums.LISTENER_POSITIONS)
    profile = models.CharField(verbose_name=u'Специфика должности', max_length=50, choices=enums.LISTENER_PROFILES)

    first_name_inflated = models.CharField(verbose_name=u'Имя (дат. падеж)', max_length=50)
    last_name_inflated = models.CharField(verbose_name=u'Фамилия (дат. падеж)', max_length=50)
    patronymic_inflated = models.CharField(verbose_name=u'Отчество (дат. падеж)', max_length=50)