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
    organization = models.ForeignKey('core.Organization', verbose_name=u'Организация')
    category = models.CharField(verbose_name=u'Категория', max_length=50, choices=enums.LISTENER_CATEGORIES)
    position = models.CharField(verbose_name=u'Должность', max_length=50, choices=enums.LISTENER_POSITIONS)
    profile = models.CharField(verbose_name=u'Специфика должности', max_length=50, choices=enums.LISTENER_PROFILES)

    first_name_inflated = models.CharField(verbose_name=u'Имя (дат. падеж)', max_length=50)
    last_name_inflated = models.CharField(verbose_name=u'Фамилия (дат. падеж)', max_length=50)
    patronymic_inflated = models.CharField(verbose_name=u'Отчество (дат. падеж)', max_length=50)

    def normalize_name(self, morph):
        from pymorphy.contrib import lastnames_ru
        # имя
        if not self.first_name:
            first_name = morph.normalize(self.first_name_inflated.upper()).pop()
            self.first_name = first_name[0].upper() + first_name[1:].lower()
        sex = morph.get_graminfo(self.first_name_inflated.upper())[0]['info'].split(',', 1)[0]
        # отчество
        if not self.patronymic:
            patronymic = morph.inflect_ru(self.patronymic_inflated.upper(), u'им')
            self.patronymic = patronymic[0].upper() + patronymic[1:].lower()

        # фамилия
        if not self.last_name:
            last_name = lastnames_ru.normalize(morph, self.last_name_inflated.upper(), sex)
            self.last_name = last_name[0].upper() + last_name[1:].lower()


        self.save()